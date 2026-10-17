"""Perturbation observation model for PIECE.

Equation:
    z_t ~ Normal(r_t, sigma_v,t^2)

Here r_t is the actual experimental rotation, while z_t
is a noisy sensory measurement of that rotation.
"""

import numpy as np


def sample_perturbation_observation(rotation, visual_sd, rng):
    """Sample z from a Gaussian centered on actual rotation."""

    rotation = np.asarray(rotation, dtype=float)
    visual_sd = np.asarray(visual_sd, dtype=float)

    if not np.all(np.isfinite(rotation)):
        raise ValueError("rotation must be finite.")

    if not np.all(np.isfinite(visual_sd)):
        raise ValueError("visual_sd must be finite.")

    if np.any(visual_sd <= 0):
        raise ValueError("visual_sd must be positive.")

    return rng.normal(loc=rotation, scale=visual_sd)
