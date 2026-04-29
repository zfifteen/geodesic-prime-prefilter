#include <stdio.h>
#include <string.h>

#include "../include/pgs_high_scale.h"

static int expect_q(unsigned long n_value, size_t candidate_bound, const char* expected_q) {
    mpz_t n, q;
    mpz_init_set_ui(n, n_value);
    mpz_init(q);

    pgs_certificate_t certificate;
    int status = pgs_resolve_from_integer(q, &certificate, n, candidate_bound);
    char* actual = status == PGS_OK ? mpz_get_str(NULL, 10, q) : NULL;
    int passed = status == PGS_OK && actual != NULL && strcmp(actual, expected_q) == 0;

    if (!passed) {
        printf("FAIL integer chamber n=%lu bound=%lu status=%d actual=%s expected=%s\n",
            n_value,
            (unsigned long)candidate_bound,
            status,
            actual ? actual : "(null)",
            expected_q);
    }

    void (*freefunc)(void*, size_t);
    mp_get_memory_functions(NULL, NULL, &freefunc);
    if (actual != NULL) {
        freefunc(actual, strlen(actual) + 1);
    }
    mpz_clear(q);
    mpz_clear(n);
    return passed;
}

static int expect_q_str(const char* n_value, size_t candidate_bound, const char* expected_q) {
    mpz_t n, q;
    mpz_init(n);
    mpz_init(q);
    mpz_set_str(n, n_value, 10);

    pgs_certificate_t certificate;
    int status = pgs_resolve_from_integer(q, &certificate, n, candidate_bound);
    char* actual = status == PGS_OK ? mpz_get_str(NULL, 10, q) : NULL;
    int passed = status == PGS_OK && actual != NULL && strcmp(actual, expected_q) == 0;

    if (!passed) {
        printf("FAIL integer chamber n=%s bound=%lu status=%d actual=%s expected=%s\n",
            n_value,
            (unsigned long)candidate_bound,
            status,
            actual ? actual : "(null)",
            expected_q);
    }

    void (*freefunc)(void*, size_t);
    mp_get_memory_functions(NULL, NULL, &freefunc);
    if (actual != NULL) {
        freefunc(actual, strlen(actual) + 1);
    }
    mpz_clear(q);
    mpz_clear(n);
    return passed;
}

static int expect_certificate(
    const char* n_value,
    size_t candidate_bound,
    const char* expected_q,
    size_t expected_offset,
    int require_tail
) {
    mpz_t n, q;
    mpz_init(n);
    mpz_init(q);
    mpz_set_str(n, n_value, 10);

    pgs_certificate_t certificate;
    int status = pgs_resolve_from_integer(q, &certificate, n, candidate_bound);
    char* actual = status == PGS_OK ? mpz_get_str(NULL, 10, q) : NULL;
    int passed =
        status == PGS_OK &&
        actual != NULL &&
        strcmp(actual, expected_q) == 0 &&
        certificate.resolved_offset == expected_offset &&
        (!require_tail || certificate.tail_after_reset_count > 0UL);

    if (!passed) {
        printf(
            "FAIL certificate n=%s bound=%lu status=%d actual=%s expected=%s "
            "offset=%lu expected_offset=%lu tail=%lu\n",
            n_value,
            (unsigned long)candidate_bound,
            status,
            actual ? actual : "(null)",
            expected_q,
            (unsigned long)certificate.resolved_offset,
            (unsigned long)expected_offset,
            (unsigned long)certificate.tail_after_reset_count
        );
    }

    void (*freefunc)(void*, size_t);
    mp_get_memory_functions(NULL, NULL, &freefunc);
    if (actual != NULL) {
        freefunc(actual, strlen(actual) + 1);
    }
    mpz_clear(q);
    mpz_clear(n);
    return passed;
}

static int expect_status(unsigned long n_value, size_t candidate_bound, int expected_status) {
    mpz_t n, q;
    mpz_init_set_ui(n, n_value);
    mpz_init(q);

    int status = pgs_resolve_from_integer(q, NULL, n, candidate_bound);
    int passed = status == expected_status;
    if (!passed) {
        printf("FAIL integer chamber status n=%lu bound=%lu status=%d expected=%d\n",
            n_value,
            (unsigned long)candidate_bound,
            status,
            expected_status);
    }

    mpz_clear(q);
    mpz_clear(n);
    return passed;
}

static int expect_gmp_certificate_q(
    const char* n_value,
    size_t candidate_bound,
    size_t endpoint_offset,
    const pgs_witness_t* witnesses,
    size_t witness_count,
    const char* expected_q,
    size_t expected_closed,
    size_t expected_unresolved
) {
    mpz_t n, q;
    mpz_init(n);
    mpz_init(q);
    mpz_set_str(n, n_value, 10);

    pgs_certificate_t certificate;
    int status = pgs_resolve_from_integer_with_witnesses(
        q,
        &certificate,
        n,
        candidate_bound,
        endpoint_offset,
        witnesses,
        witness_count
    );
    char* actual = status == PGS_OK ? mpz_get_str(NULL, 10, q) : NULL;
    int passed =
        status == PGS_OK &&
        actual != NULL &&
        strcmp(actual, expected_q) == 0 &&
        certificate.closed_count == expected_closed &&
        certificate.unresolved_count == expected_unresolved &&
        certificate.q_closed == 0UL;

    if (!passed) {
        printf(
            "FAIL GMP certificate n=%s bound=%lu status=%d actual=%s expected=%s "
            "closed=%lu expected_closed=%lu unresolved=%lu expected_unresolved=%lu "
            "invalid_witness=%lu q_closed=%lu\n",
            n_value,
            (unsigned long)candidate_bound,
            status,
            actual ? actual : "(null)",
            expected_q,
            (unsigned long)certificate.closed_count,
            (unsigned long)expected_closed,
            (unsigned long)certificate.unresolved_count,
            (unsigned long)expected_unresolved,
            (unsigned long)certificate.invalid_witness_count,
            (unsigned long)certificate.q_closed
        );
    }

    void (*freefunc)(void*, size_t);
    mp_get_memory_functions(NULL, NULL, &freefunc);
    if (actual != NULL) {
        freefunc(actual, strlen(actual) + 1);
    }
    mpz_clear(q);
    mpz_clear(n);
    return passed;
}

static int expect_gmp_certificate_status(
    const char* n_value,
    size_t candidate_bound,
    size_t endpoint_offset,
    const pgs_witness_t* witnesses,
    size_t witness_count,
    int expected_status,
    size_t expected_invalid_witness
) {
    mpz_t n, q;
    mpz_init(n);
    mpz_init(q);
    mpz_set_str(n, n_value, 10);

    pgs_certificate_t certificate;
    int status = pgs_resolve_from_integer_with_witnesses(
        q,
        &certificate,
        n,
        candidate_bound,
        endpoint_offset,
        witnesses,
        witness_count
    );
    int passed =
        status == expected_status &&
        certificate.invalid_witness_count == expected_invalid_witness;

    if (!passed) {
        printf(
            "FAIL GMP certificate status n=%s bound=%lu status=%d expected=%d "
            "invalid_witness=%lu expected_invalid_witness=%lu\n",
            n_value,
            (unsigned long)candidate_bound,
            status,
            expected_status,
            (unsigned long)certificate.invalid_witness_count,
            (unsigned long)expected_invalid_witness
        );
    }

    mpz_clear(q);
    mpz_clear(n);
    return passed;
}

int main(void) {
    int total = 0;
    int passed = 0;

    static const pgs_witness_t fake_witnesses[] = {
        {1, "3", PGS_WITNESS_FACTOR},
    };

    total++; passed += expect_q(10UL, 3, "11");
    total++; passed += expect_q(11UL, 2, "13");
    total++; passed += expect_q(1000UL, 9, "1009");
    total++; passed += expect_q(10000UL, 7, "10007");
    total++; passed += expect_status(1000UL, 8, PGS_ERR_UNRESOLVED);
    total++; passed += expect_status(1357201UL, 131, PGS_ERR_UNRESOLVED);
    total++; passed += expect_q(1357201UL, 132, "1357333");
    total++; passed += expect_q_str("1693182318746371", 1132, "1693182318747503");
    total++; passed += expect_certificate("1000000033", 1024, "1000000087", 54, 1);
    total++; passed += expect_certificate(
        "1000000000000000",
        128,
        "1000000000000037",
        37,
        1
    );
    total++; passed += expect_certificate(
        "10000000000000000",
        128,
        "10000000000000061",
        61,
        1
    );
    total++; passed += expect_gmp_certificate_q(
        "100000000000000000000",
        512,
        39,
        NULL,
        0,
        "100000000000000000039",
        11,
        0
    );
    total++; passed += expect_gmp_certificate_status(
        "100000000000000000000",
        512,
        39,
        fake_witnesses,
        sizeof(fake_witnesses) / sizeof(fake_witnesses[0]),
        PGS_ERR_UNRESOLVED,
        1
    );

    printf("PGS integer chamber tests: %d/%d passed\n", passed, total);
    return passed == total ? 0 : 1;
}
