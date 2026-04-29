#include "../include/pgs_high_scale.h"

int pgs_wheel_is_open_residue(unsigned long residue) {
    unsigned long r = residue % 30UL;
    return r == 1UL || r == 7UL || r == 11UL || r == 13UL ||
           r == 17UL || r == 19UL || r == 23UL || r == 29UL;
}

int pgs_collect_wheel_offsets(
    size_t* offsets,
    size_t max_offsets,
    size_t* count_out,
    const mpz_t p,
    size_t candidate_bound
) {
    if (count_out != NULL) {
        *count_out = 0;
    }
    if (candidate_bound < 1 || candidate_bound > PGS_MAX_CANDIDATE_BOUND) {
        return PGS_ERR_INVALID_BOUND;
    }

    unsigned long p_mod_30 = mpz_fdiv_ui(p, 30UL);
    size_t count = 0;
    for (size_t offset = 1; offset <= candidate_bound; offset++) {
        unsigned long residue = (p_mod_30 + (unsigned long)(offset % 30UL)) % 30UL;
        if (!pgs_wheel_is_open_residue(residue)) {
            continue;
        }
        if (offsets != NULL) {
            if (count >= max_offsets) {
                if (count_out != NULL) {
                    *count_out = count;
                }
                return PGS_ERR_OUTPUT;
            }
            offsets[count] = offset;
        }
        count++;
    }

    if (count_out != NULL) {
        *count_out = count;
    }
    return PGS_OK;
}
