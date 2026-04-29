#include <stdio.h>

#include "../include/pgs_high_scale.h"

static int expect_offsets(unsigned long p_value, size_t bound, const size_t* expected, size_t expected_count) {
    mpz_t p;
    mpz_init_set_ui(p, p_value);

    size_t offsets[32];
    size_t count = 0;
    int status = pgs_collect_wheel_offsets(offsets, 32, &count, p, bound);

    int passed = status == PGS_OK && count == expected_count;
    for (size_t index = 0; passed && index < expected_count; index++) {
        if (offsets[index] != expected[index]) {
            passed = 0;
        }
    }

    if (!passed) {
        printf("FAIL wheel p=%lu bound=%lu status=%d count=%lu expected=%lu\n",
            p_value,
            (unsigned long)bound,
            status,
            (unsigned long)count,
            (unsigned long)expected_count);
    }

    mpz_clear(p);
    return passed;
}

static int expect_count_only(unsigned long p_value, size_t bound, size_t expected_count) {
    mpz_t p;
    mpz_init_set_ui(p, p_value);

    size_t count = 0;
    int status = pgs_collect_wheel_offsets(NULL, 0, &count, p, bound);
    int passed = status == PGS_OK && count == expected_count;

    if (!passed) {
        printf("FAIL wheel count p=%lu bound=%lu status=%d count=%lu expected=%lu\n",
            p_value,
            (unsigned long)bound,
            status,
            (unsigned long)count,
            (unsigned long)expected_count);
    }

    mpz_clear(p);
    return passed;
}

int main(void) {
    int total = 0;
    int passed = 0;

    const size_t p11_expected[] = {2, 6, 8};
    total++; passed += expect_offsets(11UL, 10, p11_expected, 3);

    const size_t p23_expected[] = {6, 8};
    total++; passed += expect_offsets(23UL, 8, p23_expected, 2);

    total++; passed += expect_count_only(11UL, 128, 35);

    printf("PGS wheel tests: %d/%d passed\n", passed, total);
    return passed == total ? 0 : 1;
}
