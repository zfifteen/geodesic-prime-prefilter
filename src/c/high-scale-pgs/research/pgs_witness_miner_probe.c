#include "../include/pgs_high_scale.h"

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct {
    size_t offset;
    int solved;
    char* witness_decimal;
    const char* method;
    double seconds;
} target_t;

static const size_t DEFAULT_OFFSETS[] = {
    81, 97, 159, 217, 247, 259, 307, 423,
    471, 487, 511, 601, 679, 769, 783, 819,
    877, 907, 921, 957, 987, 997, 1021, 1047,
    1053, 1083, 1087, 1243,
};

static double monotonic_seconds(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + ((double)ts.tv_nsec / 1000000000.0);
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

static int build_base_primes(unsigned int** out, size_t* count_out, unsigned long limit) {
    unsigned char* composite = (unsigned char*)calloc((size_t)limit + 1UL, 1UL);
    if (composite == NULL) {
        return PGS_ERR_OUTPUT;
    }

    size_t capacity = 1024UL;
    size_t count = 0;
    unsigned int* primes = (unsigned int*)malloc(capacity * sizeof(unsigned int));
    if (primes == NULL) {
        free(composite);
        return PGS_ERR_OUTPUT;
    }

    for (unsigned long value = 2UL; value <= limit; value++) {
        if (composite[value]) {
            continue;
        }
        if (count == capacity) {
            capacity *= 2UL;
            unsigned int* next = (unsigned int*)realloc(primes, capacity * sizeof(unsigned int));
            if (next == NULL) {
                free(primes);
                free(composite);
                return PGS_ERR_OUTPUT;
            }
            primes = next;
        }
        primes[count++] = (unsigned int)value;
        if (value <= limit / value) {
            for (unsigned long multiple = value * value; multiple <= limit; multiple += value) {
                composite[multiple] = 1U;
            }
        }
    }

    free(composite);
    *out = primes;
    *count_out = count;
    return PGS_OK;
}

static unsigned long integer_sqrt_ul(unsigned long value) {
    unsigned long root = 1UL;
    while (root <= value / root) {
        root *= 2UL;
    }
    unsigned long low = root / 2UL;
    unsigned long high = root;
    while (low + 1UL < high) {
        unsigned long mid = low + ((high - low) / 2UL);
        if (mid <= value / mid) {
            low = mid;
        } else {
            high = mid;
        }
    }
    return low;
}

static char* duplicate_cstr(const char* value) {
    size_t length = strlen(value) + 1UL;
    char* copy = (char*)malloc(length);
    if (copy == NULL) {
        return NULL;
    }
    memcpy(copy, value, length);
    return copy;
}

static int set_witness(target_t* target, unsigned long witness, const char* method, double started) {
    char buffer[64];
    snprintf(buffer, sizeof(buffer), "%lu", witness);
    target->witness_decimal = duplicate_cstr(buffer);
    if (target->witness_decimal == NULL) {
        return PGS_ERR_OUTPUT;
    }
    target->method = method;
    target->seconds = started > 0.0 ? monotonic_seconds() - started : 0.0;
    target->solved = 1;
    return PGS_OK;
}

static size_t unsolved_count(const target_t* targets, size_t target_count) {
    size_t count = 0;
    for (size_t index = 0; index < target_count; index++) {
        if (!targets[index].solved) {
            count++;
        }
    }
    return count;
}

static int segmented_prime_scan(
    target_t* targets,
    size_t target_count,
    const mpz_t n,
    unsigned long start,
    unsigned long stop,
    unsigned long segment_size
) {
    if (stop < start) {
        return PGS_OK;
    }
    unsigned int* base_primes = NULL;
    size_t base_count = 0;
    int status = build_base_primes(&base_primes, &base_count, integer_sqrt_ul(stop) + 1UL);
    if (status != PGS_OK) {
        return status;
    }

    if (segment_size < 32768UL) {
        segment_size = 32768UL;
    }

    unsigned char* composite = (unsigned char*)malloc(segment_size);
    if (composite == NULL) {
        free(base_primes);
        return PGS_ERR_OUTPUT;
    }

    for (unsigned long low = start; low <= stop && unsolved_count(targets, target_count) > 0UL;) {
        unsigned long high = low + segment_size - 1UL;
        if (high < low || high > stop) {
            high = stop;
        }
        size_t span = (size_t)(high - low + 1UL);
        memset(composite, 0, span);

        for (size_t index = 0; index < base_count; index++) {
            unsigned long prime = base_primes[index];
            if (prime > high / prime) {
                break;
            }
            unsigned long first = prime * prime;
            if (first < low) {
                unsigned long rem = low % prime;
                first = rem == 0UL ? low : low + (prime - rem);
            }
            for (unsigned long value = first; value <= high; value += prime) {
                composite[value - low] = 1U;
            }
        }

        for (unsigned long value = low; value <= high; value++) {
            if (value < 2UL || composite[value - low]) {
                continue;
            }
            unsigned long remainder = mpz_fdiv_ui(n, value);
            for (size_t target_index = 0; target_index < target_count; target_index++) {
                target_t* target = &targets[target_index];
                if (target->solved) {
                    continue;
                }
                if ((remainder + (unsigned long)(target->offset % value)) % value == 0UL) {
                    int witness_status = set_witness(target, value, "segmented_prime_scan", 0.0);
                    if (witness_status != PGS_OK) {
                        free(composite);
                        free(base_primes);
                        return witness_status;
                    }
                }
            }
        }

        if (high == stop) {
            break;
        }
        low = high + 1UL;
    }

    free(composite);
    free(base_primes);
    return PGS_OK;
}

static int full_prime_scan(
    target_t* targets,
    size_t target_count,
    const mpz_t n,
    unsigned long limit
) {
    size_t max_offset = 0;
    for (size_t index = 0; index < target_count; index++) {
        if (targets[index].offset > max_offset) {
            max_offset = targets[index].offset;
        }
    }
    size_t* offset_to_target = (size_t*)malloc((max_offset + 1UL) * sizeof(size_t));
    if (offset_to_target == NULL) {
        return PGS_ERR_OUTPUT;
    }
    for (size_t index = 0; index <= max_offset; index++) {
        offset_to_target[index] = target_count;
    }
    for (size_t index = 0; index < target_count; index++) {
        offset_to_target[targets[index].offset] = index;
    }

    unsigned char* composite = (unsigned char*)calloc((size_t)limit + 1UL, 1UL);
    if (composite == NULL) {
        free(offset_to_target);
        return PGS_ERR_OUTPUT;
    }

    size_t remaining = unsolved_count(targets, target_count);
    for (unsigned long value = 2UL; value <= limit; value++) {
        if (composite[value]) {
            continue;
        }
        unsigned long remainder = mpz_fdiv_ui(n, value);
        unsigned long first_offset = (remainder == 0UL) ? value : value - remainder;
        if (first_offset <= max_offset) {
            size_t target_index = offset_to_target[first_offset];
            if (target_index < target_count && !targets[target_index].solved) {
                target_t* target = &targets[target_index];
                int witness_status = set_witness(target, value, "full_prime_scan", 0.0);
                if (witness_status != PGS_OK) {
                    free(composite);
                    free(offset_to_target);
                    return witness_status;
                }
                remaining--;
            }
        }
        if (value <= limit / value) {
            for (unsigned long multiple = value * value; multiple <= limit; multiple += value) {
                composite[multiple] = 1U;
            }
        }
        if (remaining == 0UL) {
            break;
        }
    }

    free(composite);
    free(offset_to_target);
    return PGS_OK;
}

static int pollard_rho_one(mpz_t factor, const mpz_t value, unsigned long c, unsigned long limit) {
    mpz_t x, y, d, diff, cc;
    mpz_init_set_ui(x, 2UL);
    mpz_init_set_ui(y, 2UL);
    mpz_init(d);
    mpz_init(diff);
    mpz_init_set_ui(cc, c);

    for (unsigned long iteration = 0; iteration < limit; iteration++) {
        mpz_mul(x, x, x);
        mpz_add(x, x, cc);
        mpz_mod(x, x, value);

        mpz_mul(y, y, y);
        mpz_add(y, y, cc);
        mpz_mod(y, y, value);
        mpz_mul(y, y, y);
        mpz_add(y, y, cc);
        mpz_mod(y, y, value);

        if (mpz_cmp(x, y) >= 0) {
            mpz_sub(diff, x, y);
        } else {
            mpz_sub(diff, y, x);
        }
        mpz_gcd(d, diff, value);
        if (mpz_cmp_ui(d, 1UL) > 0 && mpz_cmp(d, value) < 0) {
            mpz_set(factor, d);
            mpz_clear(cc);
            mpz_clear(diff);
            mpz_clear(d);
            mpz_clear(y);
            mpz_clear(x);
            return PGS_OK;
        }
    }

    mpz_clear(cc);
    mpz_clear(diff);
    mpz_clear(d);
    mpz_clear(y);
    mpz_clear(x);
    return PGS_ERR_UNRESOLVED;
}

static int pminus_one_scan(target_t* targets, size_t target_count, const mpz_t n, unsigned long bound) {
    unsigned int* primes = NULL;
    size_t prime_count = 0;
    int status = build_base_primes(&primes, &prime_count, bound);
    if (status != PGS_OK) {
        return status;
    }

    mpz_t exponent;
    mpz_init_set_ui(exponent, 1UL);
    for (size_t index = 0; index < prime_count; index++) {
        unsigned long power = primes[index];
        while (power <= bound / primes[index]) {
            power *= primes[index];
        }
        mpz_mul_ui(exponent, exponent, power);
    }

    mpz_t candidate, residue, factor;
    mpz_init(candidate);
    mpz_init(residue);
    mpz_init(factor);

    for (size_t target_index = 0; target_index < target_count; target_index++) {
        target_t* target = &targets[target_index];
        if (target->solved) {
            continue;
        }
        double started = monotonic_seconds();
        mpz_add_ui(candidate, n, (unsigned long)target->offset);
        mpz_set_ui(residue, 2UL);
        mpz_powm(residue, residue, exponent, candidate);
        mpz_sub_ui(residue, residue, 1UL);
        mpz_gcd(factor, residue, candidate);
        if (mpz_cmp_ui(factor, 1UL) > 0 && mpz_cmp(factor, candidate) < 0) {
            target->witness_decimal = mpz_get_str(NULL, 10, factor);
            target->method = "deterministic_pminus1";
            target->seconds = monotonic_seconds() - started;
            target->solved = 1;
        }
    }

    mpz_clear(factor);
    mpz_clear(residue);
    mpz_clear(candidate);
    mpz_clear(exponent);
    free(primes);
    return PGS_OK;
}

static int rho_scan(target_t* targets, size_t target_count, const mpz_t n) {
    static const unsigned long C_VALUES[] = {
        1UL, 2UL, 3UL, 5UL, 7UL, 11UL, 13UL, 17UL, 19UL, 23UL, 29UL, 31UL,
    };
    static const unsigned long LIMITS[] = {
        1000UL, 10000UL,
    };

    mpz_t candidate, factor;
    mpz_init(candidate);
    mpz_init(factor);

    for (size_t target_index = 0; target_index < target_count; target_index++) {
        target_t* target = &targets[target_index];
        if (target->solved) {
            continue;
        }
        double started = monotonic_seconds();
        mpz_add_ui(candidate, n, (unsigned long)target->offset);
        for (size_t limit_index = 0; limit_index < sizeof(LIMITS) / sizeof(LIMITS[0]); limit_index++) {
            for (size_t c_index = 0; c_index < sizeof(C_VALUES) / sizeof(C_VALUES[0]); c_index++) {
                int status = pollard_rho_one(
                    factor,
                    candidate,
                    C_VALUES[c_index],
                    LIMITS[limit_index]
                );
                if (status == PGS_OK) {
                    target->witness_decimal = mpz_get_str(NULL, 10, factor);
                    target->method = "deterministic_rho";
                    target->seconds = monotonic_seconds() - started;
                    target->solved = 1;
                    break;
                }
            }
            if (target->solved) {
                break;
            }
        }
    }

    mpz_clear(factor);
    mpz_clear(candidate);
    return PGS_OK;
}

static void print_header(void) {
    printf("offset,solved,method,witness,seconds\n");
}

static void print_rows(target_t* targets, size_t target_count) {
    for (size_t index = 0; index < target_count; index++) {
        printf(
            "%zu,%d,%s,%s,%.6f\n",
            targets[index].offset,
            targets[index].solved,
            targets[index].method == NULL ? "" : targets[index].method,
            targets[index].witness_decimal == NULL ? "" : targets[index].witness_decimal,
            targets[index].seconds
        );
    }
}

int main(int argc, char** argv) {
    const char* scale_arg = "10^1233";
    unsigned long scan_start = 750000001UL;
    unsigned long scan_stop = 5000000000UL;
    unsigned long segment_size = 1048576UL;

    if (argc != 1 && argc != 5) {
        fprintf(stderr, "usage: %s [scale scan_start scan_stop segment_size]\n", argv[0]);
        return 2;
    }
    if (argc == 5) {
        scale_arg = argv[1];
        if (
            parse_ulong_arg(&scan_start, argv[2]) != PGS_OK ||
            parse_ulong_arg(&scan_stop, argv[3]) != PGS_OK ||
            parse_ulong_arg(&segment_size, argv[4]) != PGS_OK
        ) {
            fprintf(stderr, "invalid numeric argument\n");
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

    size_t target_count = sizeof(DEFAULT_OFFSETS) / sizeof(DEFAULT_OFFSETS[0]);
    target_t* targets = (target_t*)calloc(target_count, sizeof(target_t));
    if (targets == NULL) {
        mpz_clear(n);
        return 1;
    }
    for (size_t index = 0; index < target_count; index++) {
        targets[index].offset = DEFAULT_OFFSETS[index];
    }

    if (scan_start <= 2UL) {
        status = full_prime_scan(targets, target_count, n, scan_stop);
    } else {
        status = segmented_prime_scan(targets, target_count, n, scan_start, scan_stop, segment_size);
    }
    if (status == PGS_OK && scan_start > scan_stop && unsolved_count(targets, target_count) > 0UL) {
        status = pminus_one_scan(targets, target_count, n, segment_size);
    }

    print_header();
    print_rows(targets, target_count);

    void (*freefunc)(void*, size_t);
    mp_get_memory_functions(NULL, NULL, &freefunc);
    for (size_t index = 0; index < target_count; index++) {
        if (targets[index].witness_decimal != NULL) {
            if (strcmp(targets[index].method, "deterministic_rho") == 0) {
                freefunc(
                    targets[index].witness_decimal,
                    strlen(targets[index].witness_decimal) + 1UL
                );
            } else {
                free(targets[index].witness_decimal);
            }
        }
    }
    free(targets);
    mpz_clear(n);
    return status == PGS_OK ? 0 : 1;
}
