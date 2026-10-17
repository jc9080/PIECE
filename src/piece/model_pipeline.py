"""Integration of the current PIECE component implementations.

This is an integration scaffold, not yet an exact
behavioral fitting implementation of the published PIECE.
Latent cue values and alpha/beta must be supplied explicitly.
"""

from .visual_uncertainty import visual_uncertainty
from .causal_inference import causal_posterior
from .state_estimation import estimate_perturbation
from .adaptation import expected_hand_angle


def predict_hand_angle(
    visual_error,
    visual_cue,
    internal_cue,
    perturbation_observation,
    bias,
    motor_sd,
    combined_sd,
    rotation_sd,
    alpha,
    beta,
):
    """Return intermediate values and expected motor output."""

    visual_sd = visual_uncertainty(
        abs(visual_error), alpha, beta
    )

    p_h0, p_h1 = causal_posterior(
        visual_cue=visual_cue,
        internal_cue=internal_cue,
        bias=bias,
        motor_sd=motor_sd,
        combined_sd=combined_sd,
        visual_sd=visual_sd,
        rotation_sd=rotation_sd,
    )

    estimated_rotation = estimate_perturbation(
        z=perturbation_observation,
        p_perturbed=p_h1,
        rotation_sd=rotation_sd,
        visual_sd=visual_sd,
    )

    predicted_hand = expected_hand_angle(
        estimated_rotation, bias
    )

    return {
        "visual_sd": visual_sd,
        "p_perturbed": p_h1,
        "estimated_rotation": estimated_rotation,
        "predicted_hand_angle": predicted_hand,
    }
