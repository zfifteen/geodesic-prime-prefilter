#include "../include/pgs_high_scale.h"

#include <errno.h>
#include <stdlib.h>
#include <string.h>

const char* pgs_get_version(void) {
    return PGS_HIGH_SCALE_VERSION;
}

static int all_decimal_digits(const char* s) {
    if (s == NULL || *s == '\0') {
        return 0;
    }
    for (const char* cursor = s; *cursor != '\0'; cursor++) {
        if (*cursor < '0' || *cursor > '9') {
            return 0;
        }
    }
    return 1;
}

static int parse_decimal_positive(mpz_t out, const char* s) {
    if (!all_decimal_digits(s)) {
        return PGS_ERR_INVALID_SCALE;
    }
    if (mpz_set_str(out, s, 10) != 0) {
        return PGS_ERR_INVALID_SCALE;
    }
    if (mpz_sgn(out) <= 0) {
        return PGS_ERR_NONPOSITIVE_SCALE;
    }
    return PGS_OK;
}

static int parse_exponent(unsigned long* out, const char* s) {
    char* end = NULL;

    if (!all_decimal_digits(s)) {
        return PGS_ERR_INVALID_SCALE;
    }

    errno = 0;
    unsigned long value = strtoul(s, &end, 10);
    if (errno != 0 || end == s || *end != '\0') {
        return PGS_ERR_INVALID_SCALE;
    }
    if (value > PGS_SCALE_MAX_EXPONENT) {
        return PGS_ERR_INVALID_SCALE;
    }

    *out = value;
    return PGS_OK;
}

int pgs_parse_scale(mpz_t out, const char* arg) {
    if (arg == NULL || *arg == '\0') {
        return PGS_ERR_INVALID_SCALE;
    }

    const char* caret = strchr(arg, '^');
    if (caret == NULL) {
        return parse_decimal_positive(out, arg);
    }

    if (strchr(caret + 1, '^') != NULL || caret == arg) {
        return PGS_ERR_INVALID_SCALE;
    }

    size_t base_len = (size_t)(caret - arg);
    char* base_str = (char*)malloc(base_len + 1);
    if (base_str == NULL) {
        return PGS_ERR_INVALID_SCALE;
    }

    memcpy(base_str, arg, base_len);
    base_str[base_len] = '\0';

    mpz_t base;
    mpz_init(base);
    int status = parse_decimal_positive(base, base_str);
    free(base_str);
    if (status != PGS_OK) {
        mpz_clear(base);
        return status;
    }

    unsigned long exponent = 0;
    status = parse_exponent(&exponent, caret + 1);
    if (status == PGS_OK) {
        mpz_pow_ui(out, base, exponent);
    }

    mpz_clear(base);
    return status;
}
