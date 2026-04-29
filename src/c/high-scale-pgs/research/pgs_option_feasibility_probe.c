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
    size_t q_gap;
    size_t candidate_bound;
    unsigned long factor_bound;
    size_t prime_count;
    size_t wheel_open_count;
    size_t pre_q_wheel_open_count;
    size_t pre_q_closed_count;
    size_t pre_q_unresolved_count;
    size_t all_unresolved_count;
    size_t q_closed;
    size_t first_wheel_open_offset;
    size_t first_wheel_unresolved_offset;
    size_t exact_count;
    size_t pre_q_exact_count;
    size_t full_certificate_entries;
    size_t hybrid_certificate_entries;
    int horizon_rule_succeeds;
    double nextprime_seconds;
    double strip_seconds;
    double total_seconds;
} feasibility_row_t;

typedef struct {
    size_t* values;
    size_t count;
    size_t capacity;
} offset_list_t;

static double monotonic_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + ((double)ts.tv_nsec / 1000000000.0);
}

static int parse_size_arg(size_t* out, const char* raw) {
    char* end = NULL;
    errno = 0;
    unsigned long value = strtoul(raw, &end, 10);
    if (errno != 0 || end == raw || *end != '\0' || value == 0UL) {
        return PGS_ERR_INVALID_BOUND;
    }
    *out = (size_t)value;
    return PGS_OK;
}

static int parse_ulong_arg(unsigned long* out, const char* raw) {
    char* end = NULL;
    errno = 0;
    unsigned long value = strtoul(raw, &end, 10);
    if (errno != 0 || end == raw || *end != '\0' || value < 2UL) {
        return PGS_ERR_INVALID_BOUND;
    }
    *out = value;
    return PGS_OK;
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

static int append_offset(offset_list_t* list, size_t value) {
    if (list->count == list->capacity) {
        size_t next_capacity = list->capacity == 0UL ? 32UL : list->capacity * 2UL;
        size_t* next = (size_t*)realloc(list->values, next_capacity * sizeof(size_t));
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

static void clear_residuals(mpz_t* residuals, size_t count) {
    if (residuals == NULL) {
        return;
    }
    for (size_t index = 0; index <= count; index++) {
        mpz_clear(residuals[index]);
    }
    free(residuals);
}

static int init_residuals(mpz_t** out, const mpz_t n, size_t candidate_bound) {
    mpz_t* residuals = (mpz_t*)malloc((candidate_bound + 1UL) * sizeof(mpz_t));
    if (residuals == NULL) {
        return PGS_ERR_OUTPUT;
    }
    for (size_t offset = 0; offset <= candidate_bound; offset++) {
        mpz_init(residuals[offset]);
        if (offset == 0UL) {
            mpz_set(residuals[offset], n);
        } else {
            mpz_add_ui(residuals[offset], n, (unsigned long)offset);
        }
    }
    *out = residuals;
    return PGS_OK;
}

static int compute_q_gap(size_t* gap_out, double* elapsed_out, const mpz_t n) {
    mpz_t q, gap;
    mpz_init(q);
    mpz_init(gap);

    double start = monotonic_seconds();
    mpz_nextprime(q, n);
    *elapsed_out = monotonic_seconds() - start;
    mpz_sub(gap, q, n);

    if (!mpz_fits_ulong_p(gap)) {
        mpz_clear(gap);
        mpz_clear(q);
        return PGS_ERR_UNRESOLVED;
    }

    *gap_out = (size_t)mpz_get_ui(gap);
    mpz_clear(gap);
    mpz_clear(q);
    return PGS_OK;
}

static int run_probe(
    feasibility_row_t* row,
    offset_list_t* unresolved_offsets,
    const mpz_t n,
    size_t candidate_bound,
    unsigned long factor_bound
) {
    memset(row, 0, sizeof(*row));
    double total_start = monotonic_seconds();
    row->candidate_bound = candidate_bound;
    row->factor_bound = factor_bound;
    if (unresolved_offsets != NULL) {
        unresolved_offsets->values = NULL;
        unresolved_offsets->count = 0;
        unresolved_offsets->capacity = 0;
    }

    int status = compute_q_gap(&row->q_gap, &row->nextprime_seconds, n);
    if (status != PGS_OK) {
        return status;
    }
    if (row->q_gap > candidate_bound) {
        return PGS_ERR_INVALID_BOUND;
    }

    prime_list_t primes;
    status = build_prime_list(&primes, factor_bound);
    if (status != PGS_OK) {
        return status;
    }
    row->prime_count = primes.count;

    mpz_t* residuals = NULL;
    status = init_residuals(&residuals, n, candidate_bound);
    if (status != PGS_OK) {
        free(primes.values);
        return status;
    }

    unsigned char* saw_factor = (unsigned char*)calloc(candidate_bound + 1UL, 1UL);
    if (saw_factor == NULL) {
        clear_residuals(residuals, candidate_bound);
        free(primes.values);
        return PGS_ERR_OUTPUT;
    }

    double strip_start = monotonic_seconds();
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
            int touched = 0;
            while (mpz_divisible_ui_p(residuals[offset], prime)) {
                mpz_divexact_ui(residuals[offset], residuals[offset], prime);
                touched = 1;
            }
            if (touched) {
                saw_factor[offset] = 1U;
            }
        }
    }
    row->strip_seconds = monotonic_seconds() - strip_start;

    unsigned long n_mod_30 = mpz_fdiv_ui(n, 30UL);
    for (size_t offset = 1; offset <= candidate_bound; offset++) {
        unsigned long residue = (n_mod_30 + (unsigned long)(offset % 30UL)) % 30UL;
        int wheel_open = pgs_wheel_is_open_residue(residue);
        int exact = mpz_cmp_ui(residuals[offset], 1UL) == 0;

        if (exact) {
            row->exact_count++;
            if (offset < row->q_gap && wheel_open) {
                row->pre_q_exact_count++;
            }
        }
        if (!wheel_open) {
            continue;
        }
        row->wheel_open_count++;
        if (row->first_wheel_open_offset == 0UL) {
            row->first_wheel_open_offset = offset;
        }
        if (offset < row->q_gap) {
            row->pre_q_wheel_open_count++;
            if (saw_factor[offset]) {
                row->pre_q_closed_count++;
            } else {
                row->pre_q_unresolved_count++;
            }
        } else if (offset == row->q_gap) {
            row->q_closed = saw_factor[offset] ? 1UL : 0UL;
        }
        if (!saw_factor[offset] && row->first_wheel_unresolved_offset == 0UL) {
            row->first_wheel_unresolved_offset = offset;
        }
        if (!saw_factor[offset]) {
            row->all_unresolved_count++;
            if (unresolved_offsets != NULL) {
                status = append_offset(unresolved_offsets, offset);
                if (status != PGS_OK) {
                    free(saw_factor);
                    clear_residuals(residuals, candidate_bound);
                    free(primes.values);
                    return status;
                }
            }
        }
    }

    row->full_certificate_entries = row->pre_q_wheel_open_count;
    row->hybrid_certificate_entries = row->pre_q_unresolved_count;
    row->horizon_rule_succeeds =
        row->pre_q_unresolved_count == 0UL &&
        row->q_closed == 0UL &&
        row->first_wheel_unresolved_offset == row->q_gap;
    row->total_seconds = monotonic_seconds() - total_start;

    free(saw_factor);
    clear_residuals(residuals, candidate_bound);
    free(primes.values);
    return PGS_OK;
}

static void print_header(void) {
    printf(
        "scale_digits,candidate_bound,factor_bound,q_gap,prime_count,"
        "wheel_open_count,pre_q_wheel_open_count,pre_q_closed_count,"
        "pre_q_unresolved_count,all_unresolved_count,q_closed,first_wheel_unresolved_offset,"
        "full_certificate_entries,hybrid_certificate_entries,horizon_rule_succeeds,"
        "exact_count,pre_q_exact_count,nextprime_seconds,strip_seconds,total_seconds\n"
    );
}

static void print_row(const mpz_t n, const feasibility_row_t* row) {
    printf(
        "%zu,%zu,%lu,%zu,%zu,%zu,%zu,%zu,%zu,%zu,%zu,%zu,%zu,%zu,%d,%zu,%zu,"
        "%.6f,%.6f,%.6f\n",
        mpz_sizeinbase(n, 10),
        row->candidate_bound,
        row->factor_bound,
        row->q_gap,
        row->prime_count,
        row->wheel_open_count,
        row->pre_q_wheel_open_count,
        row->pre_q_closed_count,
        row->pre_q_unresolved_count,
        row->all_unresolved_count,
        row->q_closed,
        row->first_wheel_unresolved_offset,
        row->full_certificate_entries,
        row->hybrid_certificate_entries,
        row->horizon_rule_succeeds,
        row->exact_count,
        row->pre_q_exact_count,
        row->nextprime_seconds,
        row->strip_seconds,
        row->total_seconds
    );
}

int main(int argc, char** argv) {
    const char* scale_arg = "10^1233";
    size_t candidate_bound = 4096UL;
    unsigned long factor_bound = 70000000UL;
    int print_offsets = 0;

    if (argc > 1 && strcmp(argv[1], "--offsets") == 0) {
        print_offsets = 1;
        argc--;
        argv++;
    }

    if (argc != 1 && argc != 4) {
        fprintf(stderr, "usage: %s [--offsets] [scale candidate_bound factor_bound]\n", argv[0]);
        return 2;
    }
    if (argc == 4) {
        scale_arg = argv[1];
        int status = parse_size_arg(&candidate_bound, argv[2]);
        if (status != PGS_OK) {
            fprintf(stderr, "invalid candidate_bound\n");
            return 2;
        }
        status = parse_ulong_arg(&factor_bound, argv[3]);
        if (status != PGS_OK) {
            fprintf(stderr, "invalid factor_bound\n");
            return 2;
        }
    }

    mpz_t n;
    mpz_init(n);
    int status = pgs_parse_scale(n, scale_arg);
    if (status != PGS_OK) {
        fprintf(stderr, "%s\n", pgs_status_message(status));
        mpz_clear(n);
        return 2;
    }

    feasibility_row_t row;
    offset_list_t unresolved_offsets;
    status = run_probe(&row, print_offsets ? &unresolved_offsets : NULL, n, candidate_bound, factor_bound);
    if (status != PGS_OK) {
        fprintf(stderr, "%s\n", pgs_status_message(status));
        mpz_clear(n);
        return 1;
    }
    print_header();
    print_row(n, &row);
    if (print_offsets) {
        printf("pre_q_unresolved_offsets");
        for (size_t index = 0; index < unresolved_offsets.count; index++) {
            printf(",%zu", unresolved_offsets.values[index]);
        }
        printf("\n");
        free(unresolved_offsets.values);
    }
    mpz_clear(n);
    return 0;
}
