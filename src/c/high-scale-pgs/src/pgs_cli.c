#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../include/pgs_high_scale.h"

static void print_usage(const char* prog_name) {
    printf("High-Scale PGS Prime Generator v%s\n", pgs_get_version());
    printf("Usage: %s [--candidate-bound N] <SCALE>\n", prog_name);
    printf("\nArguments:\n");
    printf("  <SCALE>    Positive decimal integer or exponent expression such as 10^1233\n");
    printf("\nOptions:\n");
    printf("  --candidate-bound N    Search bound, default %lu\n", PGS_DEFAULT_CANDIDATE_BOUND);
}

static int parse_candidate_bound(size_t* out, const char* raw) {
    char* end = NULL;
    unsigned long value = strtoul(raw, &end, 10);
    if (end == raw || *end != '\0' || value < 1UL || value > PGS_MAX_CANDIDATE_BOUND) {
        return PGS_ERR_INVALID_BOUND;
    }
    *out = (size_t)value;
    return PGS_OK;
}

static int parse_args(int argc, char** argv, const char** scale_arg, size_t* candidate_bound) {
    *scale_arg = NULL;
    *candidate_bound = PGS_DEFAULT_CANDIDATE_BOUND;

    for (int index = 1; index < argc; index++) {
        if (strcmp(argv[index], "-h") == 0 || strcmp(argv[index], "--help") == 0) {
            return 1;
        }
        if (strcmp(argv[index], "--candidate-bound") == 0) {
            if (index + 1 >= argc) {
                return PGS_ERR_INVALID_BOUND;
            }
            int status = parse_candidate_bound(candidate_bound, argv[++index]);
            if (status != PGS_OK) {
                return status;
            }
            continue;
        }
        if (argv[index][0] == '-') {
            return PGS_ERR_INVALID_SCALE;
        }
        if (*scale_arg != NULL) {
            return PGS_ERR_INVALID_SCALE;
        }
        *scale_arg = argv[index];
    }

    return *scale_arg == NULL ? PGS_ERR_INVALID_SCALE : PGS_OK;
}

static int exit_code_for_status(int status) {
    if (status == PGS_OK) {
        return 0;
    }
    if (status == PGS_ERR_INVALID_SCALE || status == PGS_ERR_NONPOSITIVE_SCALE ||
        status == PGS_ERR_INVALID_BOUND) {
        return 1;
    }
    return 2;
}

int main(int argc, char** argv) {
    const char* scale_arg = NULL;
    size_t candidate_bound = PGS_DEFAULT_CANDIDATE_BOUND;

    int status = parse_args(argc, argv, &scale_arg, &candidate_bound);
    if (status == 1) {
        print_usage(argv[0]);
        return 0;
    }
    if (status != PGS_OK) {
        fprintf(stderr, "Error: %s\n", pgs_status_message(status));
        return exit_code_for_status(status);
    }

    mpz_t scale;
    mpz_init(scale);

    status = pgs_parse_scale(scale, scale_arg);
    if (status != PGS_OK) {
        fprintf(stderr, "Error: %s\n", pgs_status_message(status));
        mpz_clear(scale);
        return exit_code_for_status(status);
    }

    mpz_t q;
    mpz_init(q);

    pgs_certificate_t certificate;
    status = pgs_resolve_from_integer(q, &certificate, scale, candidate_bound);
    if (status == PGS_OK) {
        status = pgs_emit_integer_record(stdout, scale, q);
    }

    if (status != PGS_OK) {
        fprintf(stderr, "Error: %s\n", pgs_status_message(status));
    }

    mpz_clear(q);
    mpz_clear(scale);
    return exit_code_for_status(status);
}
