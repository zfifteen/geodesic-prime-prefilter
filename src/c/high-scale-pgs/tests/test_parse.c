#include "../include/pgs_high_scale.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int expect_parse(const char* input, const char* expected) {
    mpz_t value;
    mpz_init(value);

    int status = pgs_parse_scale(value, input);
    char* actual = status == PGS_OK ? mpz_get_str(NULL, 10, value) : NULL;
    int passed = status == PGS_OK && actual != NULL && strcmp(actual, expected) == 0;

    if (!passed) {
        printf("FAIL parse %s\n", input);
        printf("  status:   %d\n", status);
        printf("  actual:   %s\n", actual ? actual : "(null)");
        printf("  expected: %s\n", expected);
    }

    free(actual);
    mpz_clear(value);
    return passed;
}

static int expect_status(const char* input, int expected_status) {
    mpz_t value;
    mpz_init(value);

    int status = pgs_parse_scale(value, input);
    int passed = status == expected_status;

    if (!passed) {
        printf("FAIL status %s\n", input ? input : "(null)");
        printf("  actual:   %d\n", status);
        printf("  expected: %d\n", expected_status);
    }

    mpz_clear(value);
    return passed;
}

static int expect_power10_digit_count(const char* input, size_t expected_digits) {
    mpz_t value;
    mpz_init(value);

    int status = pgs_parse_scale(value, input);
    char* actual = status == PGS_OK ? mpz_get_str(NULL, 10, value) : NULL;
    size_t actual_digits = actual == NULL ? 0 : strlen(actual);
    int passed = status == PGS_OK && actual != NULL &&
        actual_digits == expected_digits &&
        actual[0] == '1' &&
        actual[expected_digits - 1] == '0';

    if (!passed) {
        printf("FAIL digit count %s\n", input);
        printf("  status:          %d\n", status);
        printf("  actual_digits:   %lu\n", (unsigned long)actual_digits);
        printf("  expected_digits: %lu\n", (unsigned long)expected_digits);
    }

    free(actual);
    mpz_clear(value);
    return passed;
}

int main(void) {
    int total = 0;
    int passed = 0;

    total++; passed += expect_parse("12345", "12345");
    total++; passed += expect_parse("10^0", "1");
    total++; passed += expect_parse("10^3", "1000");
    total++; passed += expect_parse("2^16", "65536");
    total++; passed += expect_power10_digit_count("10^1233", 1234);
    total++; passed += expect_status("", PGS_ERR_INVALID_SCALE);
    total++; passed += expect_status("0", PGS_ERR_NONPOSITIVE_SCALE);
    total++; passed += expect_status("-1", PGS_ERR_INVALID_SCALE);
    total++; passed += expect_status("+1", PGS_ERR_INVALID_SCALE);
    total++; passed += expect_status(" 1", PGS_ERR_INVALID_SCALE);
    total++; passed += expect_status("1 ", PGS_ERR_INVALID_SCALE);
    total++; passed += expect_status("^123", PGS_ERR_INVALID_SCALE);
    total++; passed += expect_status("10^", PGS_ERR_INVALID_SCALE);
    total++; passed += expect_status("10^-1", PGS_ERR_INVALID_SCALE);
    total++; passed += expect_status("10^+1", PGS_ERR_INVALID_SCALE);
    total++; passed += expect_status("10^3^2", PGS_ERR_INVALID_SCALE);

    printf("PGS scale parser tests: %d/%d passed\n", passed, total);
    return passed == total ? 0 : 1;
}
