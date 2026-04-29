#include "../include/pgs_high_scale.h"

int pgs_write_diagnostics(
    FILE* out,
    const mpz_t scale,
    const mpz_t p,
    const pgs_certificate_t* certificate
) {
    (void)scale;
    (void)p;
    (void)certificate;
    if (out == NULL) {
        return PGS_ERR_OUTPUT;
    }
    return PGS_ERR_UNIMPLEMENTED;
}
