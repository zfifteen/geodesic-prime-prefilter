#ifndef PGS_HIGH_SCALE_H
#define PGS_HIGH_SCALE_H

#if !defined(__APPLE__) || !defined(__aarch64__)
#error "High-Scale PGS is Apple Silicon only."
#endif

#include <stddef.h>
#include <stdio.h>

#include <gmp.h>

#ifdef __cplusplus
extern "C" {
#endif

#define PGS_HIGH_SCALE_VERSION "0.1.0"
#define PGS_DEFAULT_CANDIDATE_BOUND 128UL
#define PGS_MAX_CANDIDATE_BOUND 1048576UL
#define PGS_SCALE_MAX_EXPONENT 100000UL

enum {
    PGS_OK = 0,
    PGS_ERR_INVALID_SCALE = -1,
    PGS_ERR_NONPOSITIVE_SCALE = -2,
    PGS_ERR_UNIMPLEMENTED = -4,
    PGS_ERR_UNRESOLVED = -5,
    PGS_ERR_INVALID_BOUND = -6,
    PGS_ERR_OUTPUT = -7,
    PGS_ERR_UNSUPPORTED_SCALE = -8
};

typedef struct {
    size_t candidate_bound;
    size_t resolved_offset;
    size_t wheel_open_count;
    size_t active_count;
    size_t unresolved_count;
    size_t tail_after_reset_count;
    size_t carrier_offset;
    unsigned long carrier_d;
    size_t lock_carrier_offset;
    unsigned long lock_carrier_d;
    size_t lower_d_threat_offset;
    int status;
} pgs_certificate_t;

const char* pgs_get_version(void);
const char* pgs_status_message(int status);
int pgs_parse_scale(mpz_t out, const char* arg);
int pgs_wheel_is_open_residue(unsigned long residue);
int pgs_collect_wheel_offsets(
    size_t* offsets,
    size_t max_offsets,
    size_t* count_out,
    const mpz_t p,
    size_t candidate_bound
);
int pgs_resolve_from_integer(
    mpz_t q_out,
    pgs_certificate_t* certificate,
    const mpz_t n,
    size_t candidate_bound
);
int pgs_emit_integer_record(FILE* out, const mpz_t n, const mpz_t q);
int pgs_write_diagnostics(
    FILE* out,
    const mpz_t scale,
    const mpz_t p,
    const pgs_certificate_t* certificate
);

#ifdef __cplusplus
}
#endif

#endif
