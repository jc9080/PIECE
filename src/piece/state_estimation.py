"""Perturbation state estimation for PIECE.

Implements the estimator documented in equations (2.8)-(2.9).

This module expects a perturbation observation z and
a causal posterior probability as inputs.

Paper-level integration with behavioral observations
is not yet implemented.
"""

import numpy as np


def bayesian_weight(rotation_sd, visual_sd):
    """Compute the weight assigned to a perturbation observation."""

    if rotation_sd <= 0 or visual_sd <= 0:
        raise ValueError("Standard deviations must be positive.")

    rotation_var = np.square(rotation_sd)
    visual_var = np.square(visual_sd)

    return rotation_var / (rotation_var + visual_var)


def estimate_perturbation(
    z,
    p_perturbed,
    rotation_sd,
    visual_sd,
):
    """Estimate external rotation using causal uncertainty."""

    probability = np.asarray(p_perturbed)

    if np.any(~np.isfinite(probability)):
        raise ValueError("Posterior probabilities must be finite.")

    if np.any((probability < 0) | (probability > 1)):
        raise ValueError("Posterior probabilities must be between 0 and 1.")

    weight = bayesian_weight(rotation_sd, visual_sd)

    return p_perturbed * weight * z


if __name__ == "__main__":
    probability = 0.8
    observation = 5.0

    weight = bayesian_weight(
        rotation_sd=3.0,
        visual_sd=np.sqrt(6.0),
    )

    estimate = estimate_perturbation(
        z=observation,
        p_perturbed=probability,
        rotation_sd=3.0,
        visual_sd=np.sqrt(6.0),
    )

    print("=== PERTURBATION STATE ESTIMATION ===")
    print(f"Causal posterior: {probability:.3f}")
    print(f"Bayesian weight: {weight:.3f}")
    print(f"Observation: {observation:.3f} degrees")
    print(f"Estimated perturbation: {estimate:.3f} degrees")
