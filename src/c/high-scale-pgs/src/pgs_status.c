#include "../include/pgs_high_scale.h"

const char* pgs_status_message(int status) {
    switch (status) {
        case PGS_OK:
            return "ok";
        case PGS_ERR_INVALID_SCALE:
            return "invalid scale syntax";
        case PGS_ERR_NONPOSITIVE_SCALE:
            return "scale must be positive";
        case PGS_ERR_UNIMPLEMENTED:
            return "PGS section is not implemented";
        case PGS_ERR_UNRESOLVED:
            return "PGS chamber unresolved";
        case PGS_ERR_INVALID_BOUND:
            return "invalid candidate bound";
        case PGS_ERR_OUTPUT:
            return "output error";
        case PGS_ERR_UNSUPPORTED_SCALE:
            return "scale is larger than the current exact chamber backend";
        default:
            return "unknown PGS status";
    }
}
