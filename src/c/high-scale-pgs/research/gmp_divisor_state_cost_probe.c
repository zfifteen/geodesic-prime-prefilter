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
    double sieve_seconds;
    double init_seconds;
    double strip_seconds;
    double classify_seconds;
    double total_seconds;
    size_t candidate_bound;
    unsigned long factor_bound;
    size_t prime_count;
    size_t factor_touch_count;
    size_t factor_power_count;
    size_t exact_count;
    size_t certified_composite_count;
    size_t unresolved_no_factor_count;
    size_t wheel_open_count;
    size_t wheel_open_certified_count;
    size_t wheel_open_unresolved_count;
    size_t first_wheel_unresolved_offset;
} cost_result_t;

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

static int run_cost_probe(
    cost_result_t* result,
    const mpz_t n,
    size_t candidate_bound,
    unsigned long factor_bound
) {
    memset(result, 0, sizeof(*result));
    result->candidate_bound = candidate_bound;
    result->factor_bound = factor_bound;

    double total_start = monotonic_seconds();

    prime_list_t primes;
    double sieve_start = monotonic_seconds();
    int status = build_prime_list(&primes, factor_bound);
    result->sieve_seconds = monotonic_seconds() - sieve_start;
    if (status != PGS_OK) {
        return status;
    }
    result->prime_count = primes.count;

    mpz_t* residuals = NULL;
    double init_start = monotonic_seconds();
    status = init_residuals(&residuals, n, candidate_bound);
    result->init_seconds = monotonic_seconds() - init_start;
    if (status != PGS_OK) {
        free(primes.values);
        return status;
    }

    unsigned char* saw_factor = (unsigned char*)calloc(candidate_bound + 1UL, 1UL);
    unsigned long* divisor_lower = (unsigned long*)calloc(
        candidate_bound + 1UL,
        sizeof(unsigned long)
    );
    if (saw_factor == NULL || divisor_lower == NULL) {
        free(saw_factor);
        free(divisor_lower);
        clear_residuals(residuals, candidate_bound);
        free(primes.values);
        return PGS_ERR_OUTPUT;
    }
    for (size_t offset = 1; offset <= candidate_bound; offset++) {
        divisor_lower[offset] = 1UL;
    }

    double strip_start = monotonic_seconds();
    for (size_t prime_index = 0; prime_index < primes.count; prime_index++) {
        unsigned long prime = primes.values[prime_index];
        unsigned long remainder = mpz_fdiv_ui(n, prime);
        unsigned long first_offset = (remainder == 0UL) ? prime : prime - remainder;
        if (first_offset == 0UL) {
            first_offset = prime;
        }
        if ((size_t)first_offset > candidate_bound) {
            continue;
        }
        for (
            size_t offset = (size_t)first_offset;
            offset <= candidate_bound;
            offset += (size_t)prime
        ) {
            unsigned long exponent = 0UL;
            while (mpz_divisible_ui_p(residuals[offset], prime)) {
                mpz_divexact_ui(residuals[offset], residuals[offset], prime);
                exponent++;
                result->factor_power_count++;
            }
            if (exponent != 0UL) {
                saw_factor[offset] = 1U;
                divisor_lower[offset] *= exponent + 1UL;
                result->factor_touch_count++;
            }
        }
    }
    result->strip_seconds = monotonic_seconds() - strip_start;

    double classify_start = monotonic_seconds();
    unsigned long n_mod_30 = mpz_fdiv_ui(n, 30UL);
    for (size_t offset = 1; offset <= candidate_bound; offset++) {
        int exact = mpz_cmp_ui(residuals[offset], 1UL) == 0;
        int certified = saw_factor[offset] != 0U;
        unsigned long residue = (n_mod_30 + (unsigned long)(offset % 30UL)) % 30UL;
        int wheel_open = pgs_wheel_is_open_residue(residue);

        if (exact) {
            result->exact_count++;
        }
        if (certified) {
            result->certified_composite_count++;
        } else {
            result->unresolved_no_factor_count++;
        }
        if (wheel_open) {
            result->wheel_open_count++;
            if (certified) {
                result->wheel_open_certified_count++;
            } else {
                result->wheel_open_unresolved_count++;
                if (result->first_wheel_unresolved_offset == 0UL) {
                    result->first_wheel_unresolved_offset = offset;
                }
            }
        }
    }
    result->classify_seconds = monotonic_seconds() - classify_start;
    result->total_seconds = monotonic_seconds() - total_start;

    free(saw_factor);
    free(divisor_lower);
    clear_residuals(residuals, candidate_bound);
    free(primes.values);
    return PGS_OK;
}

static void print_header(void) {
    printf(
        "scale_digits,candidate_bound,factor_bound,prime_count,"
        "candidate_count,exact_count,certified_composite_count,"
        "unresolved_no_factor_count,wheel_open_count,wheel_open_certified_count,"
        "wheel_open_unresolved_count,first_wheel_unresolved_offset,"
        "factor_touch_count,factor_power_count,sieve_seconds,init_seconds,"
        "strip_seconds,classify_seconds,total_seconds\n"
    );
}

static void print_result(const mpz_t n, const cost_result_t* result) {
    printf(
        "%zu,%zu,%lu,%zu,%zu,%zu,%zu,%zu,%zu,%zu,%zu,%zu,%zu,%zu,"
        "%.6f,%.6f,%.6f,%.6f,%.6f\n",
        mpz_sizeinbase(n, 10),
        result->candidate_bound,
        result->factor_bound,
        result->prime_count,
        result->candidate_bound,
        result->exact_count,
        result->certified_composite_count,
        result->unresolved_no_factor_count,
        result->wheel_open_count,
        result->wheel_open_certified_count,
        result->wheel_open_unresolved_count,
        result->first_wheel_unresolved_offset,
        result->factor_touch_count,
        result->factor_power_count,
        result->sieve_seconds,
        result->init_seconds,
        result->strip_seconds,
        result->classify_seconds,
        result->total_seconds
    );
}

int main(int argc, char** argv) {
    const char* scale_arg = "10^1233";
    size_t candidate_bound = 4096UL;
    unsigned long factor_bound = 1000000UL;

    if (argc != 1 && argc != 4) {
        fprintf(stderr, "usage: %s [scale candidate_bound factor_bound]\n", argv[0]);
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

    cost_result_t result;
    status = run_cost_probe(&result, n, candidate_bound, factor_bound);
    if (status != PGS_OK) {
        fprintf(stderr, "%s\n", pgs_status_message(status));
        mpz_clear(n);
        return 1;
    }

    print_header();
    print_result(n, &result);
    mpz_clear(n);
    return 0;
}
