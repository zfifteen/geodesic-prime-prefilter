#include "../include/pgs_high_scale.h"

#include <stdlib.h>

typedef struct {
    unsigned long* values;
    size_t count;
    size_t capacity;
} factor_list_t;

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

static int append_factor(factor_list_t* list, unsigned long value) {
    if (list->count == list->capacity) {
        size_t next_capacity = list->capacity == 0UL ? 1024UL : list->capacity * 2UL;
        unsigned long* next = (unsigned long*)realloc(
            list->values,
            next_capacity * sizeof(unsigned long)
        );
        if (next == NULL) {
            return PGS_ERR_OUTPUT;
        }
        list->values = next;
        list->capacity = next_capacity;
    }
    list->values[list->count++] = value;
    return PGS_OK;
}

static int build_factor_list(factor_list_t* list, unsigned long limit) {
    list->values = NULL;
    list->count = 0;
    list->capacity = 0;

    unsigned char* composite = (unsigned char*)calloc((size_t)limit + 1UL, 1UL);
    if (composite == NULL) {
        return PGS_ERR_OUTPUT;
    }

    for (unsigned long value = 2UL; value <= limit; value++) {
        if (composite[value]) {
            continue;
        }
        int status = append_factor(list, value);
        if (status != PGS_OK) {
            free(composite);
            return status;
        }
        if (value <= limit / value) {
            for (unsigned long multiple = value * value; multiple <= limit; multiple += value) {
                composite[multiple] = 1U;
            }
        }
    }

    free(composite);
    return PGS_OK;
}

static int apply_gmp_closure(
    unsigned char* closed,
    const mpz_t n,
    size_t candidate_bound,
    unsigned long factor_bound
) {
    factor_list_t factors;
    int status = build_factor_list(&factors, factor_bound);
    if (status != PGS_OK) {
        return status;
    }

    for (size_t factor_index = 0; factor_index < factors.count; factor_index++) {
        unsigned long factor = factors.values[factor_index];
        unsigned long remainder = mpz_fdiv_ui(n, factor);
        unsigned long first_offset = (remainder == 0UL) ? factor : factor - remainder;
        for (
            size_t offset = (size_t)first_offset;
            offset <= candidate_bound;
            offset += (size_t)factor
        ) {
            closed[offset] = 1U;
        }
    }

    free(factors.values);
    return PGS_OK;
}

static int witness_valid(const mpz_t n, size_t offset, const char* witness_decimal) {
    mpz_t candidate, witness, remainder;
    mpz_init(candidate);
    mpz_init(witness);
    mpz_init(remainder);
    int valid = 0;

    mpz_add_ui(candidate, n, (unsigned long)offset);
    if (mpz_set_str(witness, witness_decimal, 10) == 0 &&
        mpz_cmp_ui(witness, 1UL) > 0 &&
        mpz_cmp(witness, candidate) < 0) {
        mpz_mod(remainder, candidate, witness);
        valid = mpz_cmp_ui(remainder, 0UL) == 0;
    }

    mpz_clear(remainder);
    mpz_clear(witness);
    mpz_clear(candidate);
    return valid;
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
    certificate->closed_count = 0;
    certificate->certificate_closed_count = 0;
    certificate->invalid_witness_count = 0;
    certificate->q_closed = 0;
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

static int resolve_gmp_certificate(
    mpz_t q_out,
    pgs_certificate_t* certificate,
    const mpz_t n,
    size_t candidate_bound,
    size_t endpoint_offset,
    const pgs_witness_t* witnesses,
    size_t witness_count
) {
    unsigned char* closed = (unsigned char*)calloc(candidate_bound + 1UL, 1UL);
    if (closed == NULL) {
        return PGS_ERR_OUTPUT;
    }

    int status = apply_gmp_closure(
        closed,
        n,
        candidate_bound,
        PGS_GMP_CLOSURE_FACTOR_BOUND
    );
    if (status != PGS_OK) {
        free(closed);
        return status;
    }

    size_t certificate_closed_count = 0;
    size_t invalid_witness_count = 0;
    for (size_t index = 0; index < witness_count; index++) {
        size_t offset = witnesses[index].offset;
        if (
            offset == 0UL ||
            offset > candidate_bound ||
            witnesses[index].witness_decimal == NULL
        ) {
            invalid_witness_count++;
            continue;
        }
        if (witness_valid(n, offset, witnesses[index].witness_decimal)) {
            if (!closed[offset]) {
                certificate_closed_count++;
            }
            closed[offset] = 1U;
        } else {
            invalid_witness_count++;
        }
    }

    unsigned long n_mod_30 = mpz_fdiv_ui(n, 30UL);
    size_t wheel_open_count = 0;
    size_t closed_count = 0;
    size_t unresolved_count = 0;
    size_t end = candidate_bound;
    if (endpoint_offset != 0UL && endpoint_offset <= candidate_bound) {
        end = endpoint_offset - 1UL;
    }

    for (size_t offset = 1; offset <= end; offset++) {
        unsigned long residue = (n_mod_30 + (unsigned long)(offset % 30UL)) % 30UL;
        if (!pgs_wheel_is_open_residue(residue)) {
            continue;
        }
        wheel_open_count++;
        if (closed[offset]) {
            closed_count++;
        } else {
            unresolved_count++;
        }
    }

    size_t q_closed = 0;
    int endpoint_residue_open = 0;
    if (endpoint_offset != 0UL && endpoint_offset <= candidate_bound) {
        unsigned long endpoint_residue =
            (n_mod_30 + (unsigned long)(endpoint_offset % 30UL)) % 30UL;
        endpoint_residue_open = pgs_wheel_is_open_residue(endpoint_residue);
        q_closed = closed[endpoint_offset] ? 1UL : 0UL;
    }

    if (certificate != NULL) {
        certificate->candidate_bound = candidate_bound;
        certificate->resolved_offset = 0;
        certificate->wheel_open_count = wheel_open_count;
        certificate->active_count = unresolved_count == 0UL ? 1UL : unresolved_count;
        certificate->unresolved_count = unresolved_count;
        certificate->closed_count = closed_count;
        certificate->certificate_closed_count = certificate_closed_count;
        certificate->invalid_witness_count = invalid_witness_count;
        certificate->q_closed = q_closed;
        certificate->status = PGS_ERR_UNRESOLVED;
    }

    if (
        endpoint_offset != 0UL &&
        endpoint_offset <= candidate_bound &&
        endpoint_residue_open &&
        unresolved_count == 0UL &&
        invalid_witness_count == 0UL &&
        q_closed == 0UL
    ) {
        mpz_add_ui(q_out, n, (unsigned long)endpoint_offset);
        if (certificate != NULL) {
            certificate->resolved_offset = endpoint_offset;
            certificate->active_count = 1UL;
            certificate->status = PGS_OK;
        }
        free(closed);
        return PGS_OK;
    }

    free(closed);
    return PGS_ERR_UNRESOLVED;
}

int pgs_resolve_from_integer(
    mpz_t q_out,
    pgs_certificate_t* certificate,
    const mpz_t n,
    size_t candidate_bound
) {
    return pgs_resolve_from_integer_with_witnesses(
        q_out,
        certificate,
        n,
        candidate_bound,
        0,
        NULL,
        0
    );
}

int pgs_resolve_from_integer_with_witnesses(
    mpz_t q_out,
    pgs_certificate_t* certificate,
    const mpz_t n,
    size_t candidate_bound,
    size_t endpoint_offset,
    const pgs_witness_t* witnesses,
    size_t witness_count
) {
    clear_certificate(certificate);
    if (candidate_bound < 1 || candidate_bound > PGS_MAX_CANDIDATE_BOUND) {
        return PGS_ERR_INVALID_BOUND;
    }
    if (mpz_sgn(n) < 0 || mpz_cmp_ui(n, 5UL) < 0) {
        return PGS_ERR_UNRESOLVED;
    }
    if (witness_count > 0UL && witnesses == NULL) {
        return PGS_ERR_UNRESOLVED;
    }
    if (!mpz_fits_ulong_p(n)) {
        return resolve_gmp_certificate(
            q_out,
            certificate,
            n,
            candidate_bound,
            endpoint_offset,
            witnesses,
            witness_count
        );
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
