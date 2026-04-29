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
    pgs_witness_kind_t kind;
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
    {0, NULL, PGS_WITNESS_FACTOR},
};

static const witness_entry_t FAKE_1E1233_WITNESSES[] = {
    {81, "3", PGS_WITNESS_FACTOR},
    {97, "3", PGS_WITNESS_FACTOR},
    {159, "3", PGS_WITNESS_FACTOR},
    {217, "3", PGS_WITNESS_FACTOR},
    {247, "3", PGS_WITNESS_FACTOR},
    {259, "3", PGS_WITNESS_FACTOR},
    {307, "3", PGS_WITNESS_FACTOR},
    {423, "3", PGS_WITNESS_FACTOR},
    {471, "3", PGS_WITNESS_FACTOR},
    {487, "3", PGS_WITNESS_FACTOR},
    {511, "3", PGS_WITNESS_FACTOR},
    {523, "3", PGS_WITNESS_FACTOR},
    {531, "3", PGS_WITNESS_FACTOR},
    {601, "3", PGS_WITNESS_FACTOR},
    {669, "3", PGS_WITNESS_FACTOR},
    {679, "3", PGS_WITNESS_FACTOR},
    {769, "3", PGS_WITNESS_FACTOR},
    {783, "3", PGS_WITNESS_FACTOR},
    {819, "3", PGS_WITNESS_FACTOR},
    {877, "3", PGS_WITNESS_FACTOR},
    {907, "3", PGS_WITNESS_FACTOR},
    {921, "3", PGS_WITNESS_FACTOR},
    {931, "3", PGS_WITNESS_FACTOR},
    {957, "3", PGS_WITNESS_FACTOR},
    {987, "3", PGS_WITNESS_FACTOR},
    {997, "3", PGS_WITNESS_FACTOR},
    {1021, "3", PGS_WITNESS_FACTOR},
    {1047, "3", PGS_WITNESS_FACTOR},
    {1053, "3", PGS_WITNESS_FACTOR},
    {1083, "3", PGS_WITNESS_FACTOR},
    {1087, "3", PGS_WITNESS_FACTOR},
    {1243, "3", PGS_WITNESS_FACTOR},
};

static const witness_entry_t PARTIAL_1E1233_WITNESSES[] = {
    {97, "13485985878505098653087", PGS_WITNESS_FACTOR},
    {259, "1596877157", PGS_WITNESS_FACTOR},
    {423, "263935673443192995592639", PGS_WITNESS_FACTOR},
    {511, "42743185439", PGS_WITNESS_FACTOR},
    {523, "223502401", PGS_WITNESS_FACTOR},
    {531, "459525377", PGS_WITNESS_FACTOR},
    {601, "800678377553", PGS_WITNESS_FACTOR},
    {669, "356386241", PGS_WITNESS_FACTOR},
    {679, "930815410363", PGS_WITNESS_FACTOR},
    {769, "4113839410693", PGS_WITNESS_FACTOR},
    {783, "155034584533", PGS_WITNESS_FACTOR},
    {819, "71209726858447", PGS_WITNESS_FACTOR},
    {877, "90961441396431761", PGS_WITNESS_FACTOR},
    {907, "1271987883619", PGS_WITNESS_FACTOR},
    {921, "1337865161465878931", PGS_WITNESS_FACTOR},
    {931, "425597759", PGS_WITNESS_FACTOR},
    {957, "5141226043043", PGS_WITNESS_FACTOR},
    {987, "24541232753", PGS_WITNESS_FACTOR},
    {997, "5950437168328181", PGS_WITNESS_FACTOR},
    {1021, "255164921827", PGS_WITNESS_FACTOR},
    {1047, "29218369049", PGS_WITNESS_FACTOR},
    {1083, "2146982215818165508117211", PGS_WITNESS_FACTOR},
    {1087, "212495643561138799", PGS_WITNESS_FACTOR},
    {1243, "12828853937981", PGS_WITNESS_FACTOR},
};

static const witness_entry_t COMPLETE_1E1233_WITNESSES[] = {
    {81, "2", PGS_WITNESS_COMPOSITE_POWER},
    {97, "13485985878505098653087", PGS_WITNESS_FACTOR},
    {159, "2", PGS_WITNESS_COMPOSITE_POWER},
    {217, "2", PGS_WITNESS_COMPOSITE_POWER},
    {247, "2", PGS_WITNESS_COMPOSITE_POWER},
    {259, "1596877157", PGS_WITNESS_FACTOR},
    {307, "2", PGS_WITNESS_COMPOSITE_POWER},
    {423, "263935673443192995592639", PGS_WITNESS_FACTOR},
    {471, "2", PGS_WITNESS_COMPOSITE_POWER},
    {487, "2", PGS_WITNESS_COMPOSITE_POWER},
    {511, "42743185439", PGS_WITNESS_FACTOR},
    {523, "223502401", PGS_WITNESS_FACTOR},
    {531, "459525377", PGS_WITNESS_FACTOR},
    {601, "800678377553", PGS_WITNESS_FACTOR},
    {669, "356386241", PGS_WITNESS_FACTOR},
    {679, "930815410363", PGS_WITNESS_FACTOR},
    {769, "4113839410693", PGS_WITNESS_FACTOR},
    {783, "155034584533", PGS_WITNESS_FACTOR},
    {819, "71209726858447", PGS_WITNESS_FACTOR},
    {877, "90961441396431761", PGS_WITNESS_FACTOR},
    {907, "1271987883619", PGS_WITNESS_FACTOR},
    {921, "1337865161465878931", PGS_WITNESS_FACTOR},
    {931, "425597759", PGS_WITNESS_FACTOR},
    {957, "5141226043043", PGS_WITNESS_FACTOR},
    {987, "24541232753", PGS_WITNESS_FACTOR},
    {997, "5950437168328181", PGS_WITNESS_FACTOR},
    {1021, "255164921827", PGS_WITNESS_FACTOR},
    {1047, "29218369049", PGS_WITNESS_FACTOR},
    {1053, "2", PGS_WITNESS_COMPOSITE_POWER},
    {1083, "2146982215818165508117211", PGS_WITNESS_FACTOR},
    {1087, "212495643561138799", PGS_WITNESS_FACTOR},
    {1243, "12828853937981", PGS_WITNESS_FACTOR},
};

static const witness_entry_t HYBRID_1E12_WITNESSES[] = {
    {1, "73", PGS_WITNESS_FACTOR},
    {3, "61", PGS_WITNESS_FACTOR},
    {7, "34519", PGS_WITNESS_FACTOR},
    {9, "29", PGS_WITNESS_FACTOR},
    {19, "1601", PGS_WITNESS_FACTOR},
    {21, "11", PGS_WITNESS_FACTOR},
    {31, "19", PGS_WITNESS_FACTOR},
    {33, "23", PGS_WITNESS_FACTOR},
    {37, "53", PGS_WITNESS_FACTOR},
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
    {
        "partial_certificate_10^1233",
        "10^1233",
        4096,
        1269,
        200000000UL,
        PARTIAL_1E1233_WITNESSES,
        sizeof(PARTIAL_1E1233_WITNESSES) / sizeof(PARTIAL_1E1233_WITNESSES[0]),
        0,
    },
    {
        "complete_certificate_10^1233",
        "10^1233",
        4096,
        1269,
        200000000UL,
        COMPLETE_1E1233_WITNESSES,
        sizeof(COMPLETE_1E1233_WITNESSES) / sizeof(COMPLETE_1E1233_WITNESSES[0]),
        1,
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

static int factor_witness_valid(const mpz_t candidate, const char* witness_decimal) {
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

static int composite_power_witness_valid(const mpz_t candidate, const char* witness_decimal) {
    mpz_t base, common, exponent, residue;
    mpz_init(base);
    mpz_init(common);
    mpz_init(exponent);
    mpz_init(residue);
    int valid = 0;

    if (mpz_set_str(base, witness_decimal, 10) == 0 &&
        mpz_cmp_ui(base, 1UL) > 0 &&
        mpz_cmp(base, candidate) < 0) {
        mpz_gcd(common, base, candidate);
        if (mpz_cmp_ui(common, 1UL) > 0 && mpz_cmp(common, candidate) < 0) {
            valid = 1;
        } else {
            mpz_sub_ui(exponent, candidate, 1UL);
            mpz_powm(residue, base, exponent, candidate);
            valid = mpz_cmp_ui(residue, 1UL) != 0;
        }
    }

    mpz_clear(residue);
    mpz_clear(exponent);
    mpz_clear(common);
    mpz_clear(base);
    return valid;
}

static int witness_valid(const mpz_t candidate, const witness_entry_t* witness) {
    if (witness->kind == PGS_WITNESS_FACTOR) {
        return factor_witness_valid(candidate, witness->witness_decimal);
    }
    if (witness->kind == PGS_WITNESS_COMPOSITE_POWER) {
        return composite_power_witness_valid(candidate, witness->witness_decimal);
    }
    return 0;
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
        if (witness_valid(candidates[offset], &test_case->witnesses[index])) {
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
