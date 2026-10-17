"""Visual uncertainty for the PIECE model.

Paper formulation:
    sigma_v = alpha + beta * e

where e is the magnitude of cursor-to-target angular error.

Alpha and beta must be obtained from the published
parameter values; they are not estimated here.
"""

import numpy as np


def visual_error_magnitude(hand_angle, rotation):
    """Calculate absolute cursor-to-target angular error."""
    hand_angle = np.asarray(hand_angle, dtype=float)
    rotation = np.asarray(rotation, dtype=float)

    error = np.abs(hand_angle + rotation)

    if np.any(~np.isfinite(error)):
        raise ValueError("Error magnitude must be finite.")

    return error


def visual_uncertainty(error_magnitude, alpha, beta):
    """Calculate trial-specific visual standard deviation."""
    error = np.asarray(error_magnitude, dtype=float)

    if not np.all(np.isfinite([alpha, beta])):
        raise ValueError("Alpha and beta must be finite.")

    if alpha <= 0 or beta < 0:
        raise ValueError("Require alpha > 0 and beta >= 0.")

    if np.any(~np.isfinite(error)) or np.any(error < 0):
        raise ValueError("Error magnitude must be finite and nonnegative.")

    return alpha + beta * error
