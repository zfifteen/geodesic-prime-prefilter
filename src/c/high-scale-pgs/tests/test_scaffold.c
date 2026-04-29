#include <stdio.h>

#include "../include/pgs_high_scale.h"

static int expect_status(const char* label, int actual, int expected) {
    if (actual == expected) {
        return 1;
    }
    printf("FAIL %s: actual=%d expected=%d\n", label, actual, expected);
    return 0;
}

int main(void) {
    int total = 0;
    int passed = 0;

    mpz_t scale, q;
    mpz_init_set_ui(scale, 1000UL);
    mpz_init(q);

    pgs_certificate_t certificate;

    total++;
    passed += expect_status(
        "wheel offset invalid bound",
        pgs_collect_wheel_offsets(NULL, 0, NULL, scale, PGS_DEFAULT_CANDIDATE_BOUND),
        PGS_OK
    );

    total++;
    passed += expect_status(
        "integer chamber below supported start",
        pgs_resolve_from_integer(q, &certificate, scale, 8),
        PGS_ERR_UNRESOLVED
    );

    total++;
    passed += expect_status(
        "diagnostics scaffold",
        pgs_write_diagnostics(stdout, scale, scale, &certificate),
        PGS_ERR_UNIMPLEMENTED
    );

    mpz_clear(scale);
    mpz_clear(q);

    printf("PGS scaffold tests: %d/%d passed\n", passed, total);
    return passed == total ? 0 : 1;
}
