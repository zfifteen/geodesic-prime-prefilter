#include "../include/pgs_high_scale.h"

int pgs_emit_integer_record(FILE* out, const mpz_t n, const mpz_t q) {
    if (out == NULL) {
        return PGS_ERR_OUTPUT;
    }
    if (gmp_fprintf(out, "{\"n\":\"%Zd\",\"q\":\"%Zd\"}\n", n, q) < 0) {
        return PGS_ERR_OUTPUT;
    }
    return PGS_OK;
}
