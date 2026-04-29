#include "../include/pgs_high_scale.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct {
    unsigned long* values;
    size_t count;
    size_t capacity;
} prime_list_t;

typedef struct {
    size_t offset;
    const char* witness_decimal;
} witness_entry_t;

typedef struct {
    const char* label;
    const char* scale;
    size_t candidate_bound;
    size_t q_gap;
    unsigned long factor_bound;
    const witness_entry_t* witnesses;
    size_t witness_count;
    int expected_accept;
} verifier_case_t;

typedef struct {
    size_t pre_q_wheel_open_count;
    size_t runtime_closed_count;
    size_t certificate_closed_count;
    size_t missing_count;
    size_t invalid_witness_count;
    size_t q_closed;
    int accepted;
    double seconds;
} verifier_result_t;

static const witness_entry_t NO_WITNESSES[] = {
    {0, NULL},
};

static const witness_entry_t FAKE_1E1233_WITNESSES[] = {
    {81, "3"}, {97, "3"}, {159, "3"}, {217, "3"},
    {247, "3"}, {259, "3"}, {307, "3"}, {423, "3"},
    {471, "3"}, {487, "3"}, {511, "3"}, {523, "3"},
    {531, "3"}, {601, "3"}, {669, "3"}, {679, "3"},
    {769, "3"}, {783, "3"}, {819, "3"}, {877, "3"},
    {907, "3"}, {921, "3"}, {931, "3"}, {957, "3"},
    {987, "3"}, {997, "3"}, {1021, "3"}, {1047, "3"},
    {1053, "3"}, {1083, "3"}, {1087, "3"}, {1243, "3"},
};

static const witness_entry_t HYBRID_1E12_WITNESSES[] = {
    {1, "73"},
    {3, "61"},
    {7, "34519"},
    {9, "29"},
    {19, "1601"},
    {21, "11"},
    {31, "19"},
    {33, "23"},
    {37, "53"},
};

static const verifier_case_t CASES[] = {
    {
        "hybrid_complete_10^12",
        "10^12",
        128,
        39,
        10UL,
        HYBRID_1E12_WITNESSES,
        sizeof(HYBRID_1E12_WITNESSES) / sizeof(HYBRID_1E12_WITNESSES[0]),
        1,
    },
    {
        "runtime_complete_10^16",
        "10^16",
        4096,
        61,
        70000000UL,
        NO_WITNESSES,
        0,
        1,
    },
    {
        "incomplete_certificate_10^1233",
        "10^1233",
        4096,
        1269,
        200000000UL,
        NO_WITNESSES,
        0,
        0,
    },
    {
        "tampered_certificate_10^1233",
        "10^1233",
        4096,
        1269,
        200000000UL,
        FAKE_1E1233_WITNESSES,
        sizeof(FAKE_1E1233_WITNESSES) / sizeof(FAKE_1E1233_WITNESSES[0]),
        0,
    },
};

static double monotonic_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + ((double)ts.tv_nsec / 1000000000.0);
}

static int append_prime(prime_list_t* list, unsigned long value) {
    if (list->count == list->capacity) {
        size_t next_capacity = list->capacity == 0UL ? 1024UL : list->capacity * 2UL;
        unsigned long* next = (unsigned long*)realloc(
            list->values,
            next_capacity * sizeof(unsigned long)
        );
        if (next == NULL) {
            return PGS_ERR_OUTPUT;
        }
        list->values = next;
        list->capacity = next_capacity;
    }
    list->values[list->count++] = value;
    return PGS_OK;
}

static int build_prime_list(prime_list_t* list, unsigned long limit) {
    list->values = NULL;
    list->count = 0;
    list->capacity = 0;

    unsigned char* composite = (unsigned char*)calloc((size_t)limit + 1UL, 1UL);
    if (composite == NULL) {
        return PGS_ERR_OUTPUT;
    }

    for (unsigned long value = 2UL; value <= limit; value++) {
        if (composite[value]) {
            continue;
        }
        int status = append_prime(list, value);
        if (status != PGS_OK) {
            free(composite);
            return status;
        }
        if (value <= limit / value) {
            for (unsigned long multiple = value * value; multiple <= limit; multiple += value) {
                composite[multiple] = 1U;
            }
        }
    }

    free(composite);
    return PGS_OK;
}

static void clear_candidates(mpz_t* candidates, size_t candidate_bound) {
    if (candidates == NULL) {
        return;
    }
    for (size_t offset = 0; offset <= candidate_bound; offset++) {
        mpz_clear(candidates[offset]);
    }
    free(candidates);
}

static int init_candidates(mpz_t** out, const mpz_t n, size_t candidate_bound) {
    mpz_t* candidates = (mpz_t*)malloc((candidate_bound + 1UL) * sizeof(mpz_t));
    if (candidates == NULL) {
        return PGS_ERR_OUTPUT;
    }
    for (size_t offset = 0; offset <= candidate_bound; offset++) {
        mpz_init(candidates[offset]);
        mpz_add_ui(candidates[offset], n, (unsigned long)offset);
    }
    *out = candidates;
    return PGS_OK;
}

static int apply_runtime_closure(
    unsigned char* closed,
    const mpz_t n,
    size_t candidate_bound,
    unsigned long factor_bound
) {
    prime_list_t primes;
    int status = build_prime_list(&primes, factor_bound);
    if (status != PGS_OK) {
        return status;
    }

    for (size_t prime_index = 0; prime_index < primes.count; prime_index++) {
        unsigned long prime = primes.values[prime_index];
        unsigned long remainder = mpz_fdiv_ui(n, prime);
        unsigned long first_offset = (remainder == 0UL) ? prime : prime - remainder;
        if (first_offset == 0UL) {
            first_offset = prime;
        }
        for (
            size_t offset = (size_t)first_offset;
            offset <= candidate_bound;
            offset += (size_t)prime
        ) {
            closed[offset] = 1U;
        }
    }

    free(primes.values);
    return PGS_OK;
}

static int witness_valid(const mpz_t candidate, const char* witness_decimal) {
    mpz_t witness, remainder;
    mpz_init(witness);
    mpz_init(remainder);
    int valid = 0;

    if (mpz_set_str(witness, witness_decimal, 10) == 0 &&
        mpz_cmp_ui(witness, 1UL) > 0 &&
        mpz_cmp(witness, candidate) < 0) {
        mpz_mod(remainder, candidate, witness);
        valid = mpz_cmp_ui(remainder, 0UL) == 0;
    }

    mpz_clear(remainder);
    mpz_clear(witness);
    return valid;
}

static int run_case(verifier_result_t* result, const verifier_case_t* test_case) {
    memset(result, 0, sizeof(*result));
    double start = monotonic_seconds();

    mpz_t n;
    mpz_init(n);
    int status = pgs_parse_scale(n, test_case->scale);
    if (status != PGS_OK) {
        mpz_clear(n);
        return status;
    }

    mpz_t* candidates = NULL;
    status = init_candidates(&candidates, n, test_case->candidate_bound);
    if (status != PGS_OK) {
        mpz_clear(n);
        return status;
    }

    unsigned char* closed = (unsigned char*)calloc(test_case->candidate_bound + 1UL, 1UL);
    if (closed == NULL) {
        clear_candidates(candidates, test_case->candidate_bound);
        mpz_clear(n);
        return PGS_ERR_OUTPUT;
    }

    status = apply_runtime_closure(
        closed,
        n,
        test_case->candidate_bound,
        test_case->factor_bound
    );
    if (status != PGS_OK) {
        free(closed);
        clear_candidates(candidates, test_case->candidate_bound);
        mpz_clear(n);
        return status;
    }

    for (size_t index = 0; index < test_case->witness_count; index++) {
        size_t offset = test_case->witnesses[index].offset;
        if (offset == 0UL || offset > test_case->candidate_bound) {
            result->invalid_witness_count++;
            continue;
        }
        if (witness_valid(candidates[offset], test_case->witnesses[index].witness_decimal)) {
            if (!closed[offset]) {
                result->certificate_closed_count++;
            }
            closed[offset] = 1U;
        } else {
            result->invalid_witness_count++;
        }
    }

    unsigned long n_mod_30 = mpz_fdiv_ui(n, 30UL);
    for (size_t offset = 1; offset < test_case->q_gap; offset++) {
        unsigned long residue = (n_mod_30 + (unsigned long)(offset % 30UL)) % 30UL;
        if (!pgs_wheel_is_open_residue(residue)) {
            continue;
        }
        result->pre_q_wheel_open_count++;
        if (closed[offset]) {
            result->runtime_closed_count++;
        } else {
            result->missing_count++;
        }
    }
    result->q_closed = closed[test_case->q_gap] ? 1UL : 0UL;
    result->accepted =
        result->missing_count == 0UL &&
        result->invalid_witness_count == 0UL &&
        result->q_closed == 0UL;
    result->seconds = monotonic_seconds() - start;

    free(closed);
    clear_candidates(candidates, test_case->candidate_bound);
    mpz_clear(n);
    return PGS_OK;
}

static void print_header(void) {
    printf(
        "case,scale,candidate_bound,q_gap,factor_bound,witness_count,"
        "pre_q_wheel_open,final_closed,certificate_closed,missing,"
        "invalid_witness,q_closed,accepted,expected_accept,seconds\n"
    );
}

static void print_row(const verifier_case_t* test_case, const verifier_result_t* result) {
    printf(
        "%s,%s,%zu,%zu,%lu,%zu,%zu,%zu,%zu,%zu,%zu,%zu,%d,%d,%.6f\n",
        test_case->label,
        test_case->scale,
        test_case->candidate_bound,
        test_case->q_gap,
        test_case->factor_bound,
        test_case->witness_count,
        result->pre_q_wheel_open_count,
        result->runtime_closed_count,
        result->certificate_closed_count,
        result->missing_count,
        result->invalid_witness_count,
        result->q_closed,
        result->accepted,
        test_case->expected_accept,
        result->seconds
    );
}

int main(void) {
    print_header();
    int all_expected = 1;
    size_t case_count = sizeof(CASES) / sizeof(CASES[0]);
    for (size_t index = 0; index < case_count; index++) {
        verifier_result_t result;
        int status = run_case(&result, &CASES[index]);
        if (status != PGS_OK) {
            fprintf(stderr, "%s: %s\n", CASES[index].label, pgs_status_message(status));
            return 1;
        }
        print_row(&CASES[index], &result);
        if (result.accepted != CASES[index].expected_accept) {
            all_expected = 0;
        }
    }
    return all_expected ? 0 : 1;
}
