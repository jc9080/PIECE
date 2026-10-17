"""Numerical verification of the combined-cue likelihood.

Compare the analytic causal posterior with numerical
integration over the latent hand angle.

This tests the Gaussian combined-cue formulation,
not yet the full behavioral fitting model.
"""

import numpy as np
from scipy.integrate import quad
from scipy.stats import norm

from src.piece.causal_inference import causal_posterior


def numerical_causal_posterior(
    visual_cue,
    internal_cue,
    bias,
    motor_sd,
    combined_sd,
    visual_sd,
    rotation_sd,
):
    """Numerically integrate over the latent hand angle."""

    def hand_and_internal_density(hand):
        return (
            norm.pdf(hand, loc=bias, scale=motor_sd)
            * norm.pdf(
                internal_cue,
                loc=hand,
                scale=combined_sd,
            )
        )

    def integrand_h0(hand):
        return (
            hand_and_internal_density(hand)
            * norm.pdf(
                visual_cue,
                loc=hand,
                scale=visual_sd,
            )
        )

    def integrand_h1(hand):
        # Marginalize the Gaussian rotation variable.
        perturbed_visual_sd = np.sqrt(
            visual_sd**2 + rotation_sd**2
        )

        return (
            hand_and_internal_density(hand)
            * norm.pdf(
                visual_cue,
                loc=hand,
                scale=perturbed_visual_sd,
            )
        )

    likelihood_h0, _ = quad(
        integrand_h0,
        -np.inf,
        np.inf,
    )

    likelihood_h1, _ = quad(
        integrand_h1,
        -np.inf,
        np.inf,
    )

    total = likelihood_h0 + likelihood_h1

    # Equal prior probabilities:
    # P(H0) = P(H1) = 0.5
    p_h0 = likelihood_h0 / total
    p_h1 = likelihood_h1 / total

    return p_h0, p_h1


def test_analytic_matches_numerical_integration():

    cases = [
        (5.0, 1.0, 0.0, 2.0, 1.0, 2.0, 3.0),
        (0.0, 0.0, 0.0, 1.5, 1.0, 2.0, 3.0),
        (-3.0, -1.0, 0.5, 2.0, 1.5, 2.5, 4.0),
        (2.0, 1.5, -0.5, 1.8, 1.2, 3.0, 2.0),
    ]

    for params in cases:

        numerical_h0, numerical_h1 = (
            numerical_causal_posterior(*params)
        )

        analytic_h0, analytic_h1 = causal_posterior(
            visual_cue=params[0],
            internal_cue=params[1],
            bias=params[2],
            motor_sd=params[3],
            combined_sd=params[4],
            visual_sd=params[5],
            rotation_sd=params[6],
        )

        assert np.isclose(
            analytic_h0,
            numerical_h0,
            rtol=1e-6,
            atol=1e-8,
        )

        assert np.isclose(
            analytic_h1,
            numerical_h1,
            rtol=1e-6,
            atol=1e-8,
        )

        assert np.isclose(
            analytic_h0 + analytic_h1,
            1.0,
        )
