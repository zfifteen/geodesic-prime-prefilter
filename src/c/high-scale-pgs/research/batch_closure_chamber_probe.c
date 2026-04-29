#include "../include/pgs_high_scale.h"

#include <errno.h>
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    const char* label;
    unsigned long exponent;
    size_t expected_gap;
} audit_case_t;

typedef struct {
    size_t candidate_bound;
    unsigned long factor_bound;
    size_t wheel_open_count;
    size_t closed_count;
    size_t open_count;
    size_t first_open_offset;
    size_t expected_gap;
    size_t pre_expected_open_count;
    int expected_closed;
    int first_open_matches_expected;
} closure_result_t;

static const audit_case_t AUDIT_CASES[] = {
    {"10^3", 3UL, 9UL},
    {"10^4", 4UL, 7UL},
    {"10^5", 5UL, 3UL},
    {"10^6", 6UL, 3UL},
    {"10^7", 7UL, 19UL},
    {"10^8", 8UL, 7UL},
    {"10^9", 9UL, 7UL},
    {"10^10", 10UL, 19UL},
    {"10^11", 11UL, 3UL},
    {"10^12", 12UL, 39UL},
    {"10^13", 13UL, 37UL},
    {"10^14", 14UL, 31UL},
    {"10^15", 15UL, 37UL},
    {"10^16", 16UL, 61UL},
    {"10^17", 17UL, 3UL},
    {"10^18", 18UL, 3UL},
};

static int parse_size_arg(size_t* out, const char* raw) {
    char* end = NULL;
    errno = 0;
    unsigned long value = strtoul(raw, &end, 10);
    if (errno != 0 || end == raw || *end != '\0') {
        return PGS_ERR_INVALID_BOUND;
    }
    *out = (size_t)value;
    return PGS_OK;
}

static int parse_ulong_arg(unsigned long* out, const char* raw) {
    char* end = NULL;
    errno = 0;
    unsigned long value = strtoul(raw, &end, 10);
    if (errno != 0 || end == raw || *end != '\0') {
        return PGS_ERR_INVALID_BOUND;
    }
    *out = value;
    return PGS_OK;
}

static int proper_divisor(const mpz_t n, size_t offset, unsigned long factor, mpz_t scratch) {
    if (mpz_cmp_ui(n, factor) > 0) {
        return 1;
    }
    mpz_add_ui(scratch, n, (unsigned long)offset);
    return mpz_cmp_ui(scratch, factor) > 0;
}

static int run_closure_probe(
    closure_result_t* result,
    const mpz_t n,
    size_t candidate_bound,
    unsigned long factor_bound,
    size_t expected_gap
) {
    if (candidate_bound < 1 || candidate_bound > PGS_MAX_CANDIDATE_BOUND) {
        return PGS_ERR_INVALID_BOUND;
    }
    if (factor_bound < 2UL) {
        return PGS_ERR_INVALID_BOUND;
    }

    unsigned char* wheel_open = (unsigned char*)calloc(candidate_bound + 1UL, 1UL);
    unsigned char* closed = (unsigned char*)calloc(candidate_bound + 1UL, 1UL);
    if (wheel_open == NULL || closed == NULL) {
        free(wheel_open);
        free(closed);
        return PGS_ERR_OUTPUT;
    }

    unsigned long n_mod_30 = mpz_fdiv_ui(n, 30UL);
    size_t wheel_open_count = 0;
    for (size_t offset = 1; offset <= candidate_bound; offset++) {
        unsigned long residue = (n_mod_30 + (unsigned long)(offset % 30UL)) % 30UL;
        if (pgs_wheel_is_open_residue(residue)) {
            wheel_open[offset] = 1U;
            wheel_open_count++;
        }
    }

    mpz_t scratch;
    mpz_init(scratch);
    size_t closed_count = 0;
    for (unsigned long factor = 2UL; factor <= factor_bound; factor++) {
        unsigned long remainder = mpz_fdiv_ui(n, factor);
        unsigned long first_offset = (remainder == 0UL) ? factor : factor - remainder;
        if (first_offset == 0UL) {
            first_offset = factor;
        }
        for (
            size_t offset = (size_t)first_offset;
            offset <= candidate_bound;
            offset += (size_t)factor
        ) {
            if (!wheel_open[offset] || closed[offset]) {
                continue;
            }
            if (!proper_divisor(n, offset, factor, scratch)) {
                continue;
            }
            closed[offset] = 1U;
            closed_count++;
        }
    }
    mpz_clear(scratch);

    size_t first_open_offset = 0;
    size_t open_count = 0;
    for (size_t offset = 1; offset <= candidate_bound; offset++) {
        if (!wheel_open[offset] || closed[offset]) {
            continue;
        }
        if (first_open_offset == 0UL) {
            first_open_offset = offset;
        }
        open_count++;
    }

    size_t pre_expected_open_count = 0;
    int expected_closed = 0;
    int first_open_matches_expected = 0;
    if (expected_gap > 0UL && expected_gap <= candidate_bound) {
        for (size_t offset = 1; offset < expected_gap; offset++) {
            if (wheel_open[offset] && !closed[offset]) {
                pre_expected_open_count++;
            }
        }
        expected_closed = closed[expected_gap] ? 1 : 0;
        first_open_matches_expected = first_open_offset == expected_gap;
    }

    result->candidate_bound = candidate_bound;
    result->factor_bound = factor_bound;
    result->wheel_open_count = wheel_open_count;
    result->closed_count = closed_count;
    result->open_count = open_count;
    result->first_open_offset = first_open_offset;
    result->expected_gap = expected_gap;
    result->pre_expected_open_count = pre_expected_open_count;
    result->expected_closed = expected_closed;
    result->first_open_matches_expected = first_open_matches_expected;

    free(wheel_open);
    free(closed);
    return PGS_OK;
}

static void print_header(void) {
    printf(
        "label,digits,candidate_bound,factor_bound,wheel_open,closed,open,"
        "closure_rate,first_open_offset,expected_gap,pre_expected_open,"
        "expected_closed,first_open_matches_expected\n"
    );
}

static void print_row(const char* label, const mpz_t n, const closure_result_t* row) {
    double closure_rate = 0.0;
    if (row->wheel_open_count != 0UL) {
        closure_rate = (double)row->closed_count / (double)row->wheel_open_count;
    }
    printf(
        "%s,%zu,%zu,%lu,%zu,%zu,%zu,%.12f,%zu,%zu,%zu,%d,%d\n",
        label,
        mpz_sizeinbase(n, 10),
        row->candidate_bound,
        row->factor_bound,
        row->wheel_open_count,
        row->closed_count,
        row->open_count,
        closure_rate,
        row->first_open_offset,
        row->expected_gap,
        row->pre_expected_open_count,
        row->expected_closed,
        row->first_open_matches_expected
    );
}

static int run_one(
    const char* label,
    const mpz_t n,
    size_t candidate_bound,
    unsigned long factor_bound,
    size_t expected_gap
) {
    closure_result_t row;
    int status = run_closure_probe(&row, n, candidate_bound, factor_bound, expected_gap);
    if (status != PGS_OK) {
        return status;
    }
    print_row(label, n, &row);
    return PGS_OK;
}

static int run_default_suite(size_t candidate_bound, unsigned long factor_bound) {
    print_header();

    mpz_t n;
    mpz_init(n);
    int status = PGS_OK;

    size_t audit_count = sizeof(AUDIT_CASES) / sizeof(AUDIT_CASES[0]);
    for (size_t index = 0; index < audit_count; index++) {
        mpz_ui_pow_ui(n, 10UL, AUDIT_CASES[index].exponent);
        status = run_one(
            AUDIT_CASES[index].label,
            n,
            candidate_bound,
            factor_bound,
            AUDIT_CASES[index].expected_gap
        );
        if (status != PGS_OK) {
            mpz_clear(n);
            return status;
        }
    }

    mpz_ui_pow_ui(n, 10UL, 1233UL);
    status = run_one("10^1233", n, candidate_bound, factor_bound, 0UL);
    mpz_clear(n);
    return status;
}

static int run_single(const char* scale, size_t candidate_bound, unsigned long factor_bound) {
    mpz_t n;
    mpz_init(n);
    int status = pgs_parse_scale(n, scale);
    if (status != PGS_OK) {
        mpz_clear(n);
        return status;
    }
    print_header();
    status = run_one("single", n, candidate_bound, factor_bound, 0UL);
    mpz_clear(n);
    return status;
}

int main(int argc, char** argv) {
    size_t candidate_bound = 4096UL;
    unsigned long factor_bound = 50000UL;

    if (argc != 1 && argc != 3 && argc != 4) {
        fprintf(
            stderr,
            "usage: %s [candidate_bound factor_bound] | [scale candidate_bound factor_bound]\n",
            argv[0]
        );
        return 2;
    }

    if (argc == 3) {
        int status = parse_size_arg(&candidate_bound, argv[1]);
        if (status != PGS_OK) {
            fprintf(stderr, "invalid candidate_bound\n");
            return 2;
        }
        status = parse_ulong_arg(&factor_bound, argv[2]);
        if (status != PGS_OK) {
            fprintf(stderr, "invalid factor_bound\n");
            return 2;
        }
        status = run_default_suite(candidate_bound, factor_bound);
        if (status != PGS_OK) {
            fprintf(stderr, "%s\n", pgs_status_message(status));
            return 1;
        }
        return 0;
    }

    if (argc == 4) {
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
        status = run_single(argv[1], candidate_bound, factor_bound);
        if (status != PGS_OK) {
            fprintf(stderr, "%s\n", pgs_status_message(status));
            return 1;
        }
        return 0;
    }

    int status = run_default_suite(candidate_bound, factor_bound);
    if (status != PGS_OK) {
        fprintf(stderr, "%s\n", pgs_status_message(status));
        return 1;
    }
    return 0;
}
