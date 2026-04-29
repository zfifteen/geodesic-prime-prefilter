#include <stdio.h>

#include "../include/pgs_high_scale.h"

int main(void) {
    mpz_t n, q;
    mpz_init_set_ui(n, 10UL);
    mpz_init_set_ui(q, 13UL);

    int status = pgs_emit_integer_record(stdout, n, q);

    mpz_clear(n);
    mpz_clear(q);

    if (status != PGS_OK) {
        printf("PGS emitter failed: %d\n", status);
        return 1;
    }
    return 0;
}
