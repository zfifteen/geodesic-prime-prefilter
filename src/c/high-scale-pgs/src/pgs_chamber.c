#include "../include/pgs_high_scale.h"

#include <stdlib.h>

typedef enum {
    CANDIDATE_REJECTED = 0,
    CANDIDATE_RESOLVED_SURVIVOR = 1,
    CANDIDATE_UNRESOLVED = 2
} candidate_status_t;

typedef struct {
    size_t offset;
    unsigned long divisor_count;
    candidate_status_t status;
    size_t carrier_offset;
    unsigned long carrier_d;
} candidate_state_t;

static unsigned long divisor_count_ui(unsigned long value) {
    if (value == 1UL) {
        return 1UL;
    }

    unsigned long remaining = value;
    unsigned long count = 1UL;

    unsigned long exponent = 0;
    while ((remaining % 2UL) == 0UL) {
        remaining /= 2UL;
        exponent++;
    }
    if (exponent != 0UL) {
        count *= exponent + 1UL;
    }

    for (unsigned long factor = 3UL; factor <= remaining / factor; factor += 2UL) {
        exponent = 0;
        while ((remaining % factor) == 0UL) {
            remaining /= factor;
            exponent++;
        }
        if (exponent != 0UL) {
            count *= exponent + 1UL;
        }
    }

    if (remaining > 1UL) {
        count *= 2UL;
    }

    return count;
}

static void clear_certificate(pgs_certificate_t* certificate) {
    if (certificate == NULL) {
        return;
    }
    certificate->candidate_bound = 0;
    certificate->resolved_offset = 0;
    certificate->wheel_open_count = 0;
    certificate->active_count = 0;
    certificate->unresolved_count = 0;
    certificate->tail_after_reset_count = 0;
    certificate->carrier_offset = 0;
    certificate->carrier_d = 0;
    certificate->lock_carrier_offset = 0;
    certificate->lock_carrier_d = 0;
    certificate->lower_d_threat_offset = 0;
    certificate->status = PGS_ERR_UNRESOLVED;
}

static void unresolved_certificate(
    pgs_certificate_t* certificate,
    size_t candidate_bound,
    size_t wheel_open_count,
    size_t active_count,
    size_t unresolved_count
) {
    if (certificate == NULL) {
        return;
    }
    clear_certificate(certificate);
    certificate->candidate_bound = candidate_bound;
    certificate->wheel_open_count = wheel_open_count;
    certificate->active_count = active_count;
    certificate->unresolved_count = unresolved_count;
    certificate->status = PGS_ERR_UNRESOLVED;
}

int pgs_resolve_from_integer(
    mpz_t q_out,
    pgs_certificate_t* certificate,
    const mpz_t n,
    size_t candidate_bound
) {
    clear_certificate(certificate);
    if (candidate_bound < 1 || candidate_bound > PGS_MAX_CANDIDATE_BOUND) {
        return PGS_ERR_INVALID_BOUND;
    }
    if (mpz_sgn(n) < 0 || mpz_cmp_ui(n, 5UL) < 0) {
        return PGS_ERR_UNRESOLVED;
    }
    if (!mpz_fits_ulong_p(n)) {
        size_t wheel_open_count = 0;
        int wheel_status = pgs_collect_wheel_offsets(
            NULL,
            0,
            &wheel_open_count,
            n,
            candidate_bound
        );
        if (wheel_status != PGS_OK) {
            return wheel_status;
        }
        unresolved_certificate(
            certificate,
            candidate_bound,
            wheel_open_count,
            wheel_open_count,
            wheel_open_count
        );
        return PGS_ERR_UNRESOLVED;
    }

    unsigned long start = mpz_get_ui(n);
    unsigned long* counts = (unsigned long*)calloc(candidate_bound + 1UL, sizeof(unsigned long));
    candidate_state_t* states = (candidate_state_t*)calloc(
        candidate_bound + 1UL,
        sizeof(candidate_state_t)
    );
    if (counts == NULL || states == NULL) {
        free(counts);
        free(states);
        return PGS_ERR_OUTPUT;
    }

    for (size_t offset = 1; offset <= candidate_bound; offset++) {
        if (start > ~0UL - offset) {
            free(counts);
            free(states);
            size_t wheel_open_count = 0;
            int wheel_status = pgs_collect_wheel_offsets(
                NULL,
                0,
                &wheel_open_count,
                n,
                candidate_bound
            );
            if (wheel_status != PGS_OK) {
                return wheel_status;
            }
            unresolved_certificate(
                certificate,
                candidate_bound,
                wheel_open_count,
                wheel_open_count,
                wheel_open_count
            );
            return PGS_ERR_UNRESOLVED;
        }
        counts[offset] = divisor_count_ui(start + (unsigned long)offset);
    }

    size_t wheel_open_count = 0;
    size_t state_count = 0;
    size_t unresolved_count = 0;
    size_t carrier_offset = 0;
    unsigned long carrier_d = 0;

    for (size_t offset = 1; offset <= candidate_bound; offset++) {
        unsigned long candidate = start + (unsigned long)offset;
        unsigned long divisor_count = counts[offset];

        if (pgs_wheel_is_open_residue(candidate % 30UL)) {
            candidate_state_t* state = &states[state_count++];
            wheel_open_count++;
            state->offset = offset;
            state->divisor_count = divisor_count;
            state->carrier_offset = carrier_offset;
            state->carrier_d = carrier_d;
            if (divisor_count > 2UL) {
                state->status = CANDIDATE_REJECTED;
            } else if (unresolved_count > 0UL) {
                state->status = CANDIDATE_UNRESOLVED;
            } else {
                state->status = CANDIDATE_RESOLVED_SURVIVOR;
            }
        }

        if (divisor_count > 2UL) {
            if (carrier_d == 0UL || divisor_count < carrier_d) {
                carrier_offset = offset;
                carrier_d = divisor_count;
            }
        } else {
            unresolved_count++;
        }
    }

    size_t lock_carrier_offset = 0;
    unsigned long lock_carrier_d = 0;
    for (size_t index = 0; index < state_count; index++) {
        candidate_state_t* state = &states[index];
        if (
            state->status == CANDIDATE_RESOLVED_SURVIVOR &&
            state->carrier_offset != 0UL
        ) {
            lock_carrier_offset = state->carrier_offset;
            lock_carrier_d = state->carrier_d;
            break;
        }
    }

    size_t threat_offset = 0;
    if (lock_carrier_offset != 0UL && lock_carrier_d != 0UL) {
        for (size_t offset = lock_carrier_offset + 1UL; offset <= candidate_bound; offset++) {
            unsigned long divisor_count = counts[offset];
            if (divisor_count > 2UL && divisor_count < lock_carrier_d) {
                threat_offset = offset;
                break;
            }
        }
    }

    size_t active_count = 0;
    size_t final_unresolved_count = 0;
    size_t resolved_index = 0;
    int has_resolved = 0;

    for (size_t index = 0; index < state_count; index++) {
        candidate_state_t* state = &states[index];
        candidate_status_t final_status = state->status;
        if (threat_offset != 0UL && state->offset > threat_offset) {
            final_status = CANDIDATE_REJECTED;
        }
        if (final_status == CANDIDATE_REJECTED) {
            continue;
        }
        active_count++;
        if (final_status == CANDIDATE_RESOLVED_SURVIVOR && !has_resolved) {
            resolved_index = index;
            has_resolved = 1;
        } else if (final_status == CANDIDATE_UNRESOLVED) {
            final_unresolved_count++;
        }
    }

    if (!has_resolved) {
        unresolved_certificate(
            certificate,
            candidate_bound,
            wheel_open_count,
            active_count,
            final_unresolved_count
        );
        free(counts);
        free(states);
        return PGS_ERR_UNRESOLVED;
    }

    candidate_state_t* resolved = &states[resolved_index];
    size_t tail_after_reset_count = 0;
    for (size_t index = 0; index < state_count; index++) {
        candidate_state_t* state = &states[index];
        candidate_status_t final_status = state->status;
        if (threat_offset != 0UL && state->offset > threat_offset) {
            final_status = CANDIDATE_REJECTED;
        }
        if (
            final_status == CANDIDATE_UNRESOLVED &&
            state->offset > resolved->offset
        ) {
            tail_after_reset_count++;
        }
    }

    mpz_set_ui(q_out, start + (unsigned long)resolved->offset);
    if (certificate != NULL) {
        certificate->candidate_bound = candidate_bound;
        certificate->resolved_offset = resolved->offset;
        certificate->wheel_open_count = wheel_open_count;
        certificate->active_count = active_count;
        certificate->unresolved_count = final_unresolved_count;
        certificate->tail_after_reset_count = tail_after_reset_count;
        certificate->carrier_offset = resolved->carrier_offset;
        certificate->carrier_d = resolved->carrier_d;
        certificate->lock_carrier_offset = lock_carrier_offset;
        certificate->lock_carrier_d = lock_carrier_d;
        certificate->lower_d_threat_offset = threat_offset;
        certificate->status = PGS_OK;
    }

    free(counts);
    free(states);
    return PGS_OK;
}
