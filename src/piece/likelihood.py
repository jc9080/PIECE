"""Gaussian likelihoods for PIECE causal hypotheses.

Implements an analytic Gaussian reduction using a
combined internal cue. Full paper-level equivalence
is not yet established.
"""

import numpy as np
from scipy.stats import norm


def hand_posterior_from_internal(
    internal_cue,
    bias,
    motor_sd,
    combined_sd,
):
    """Return posterior mean and variance of hand position."""

    if motor_sd <= 0 or combined_sd <= 0:
        raise ValueError("Standard deviations must be positive.")

    motor_var = motor_sd ** 2
    combined_var = combined_sd ** 2

    gain = motor_var / (motor_var + combined_var)

    mean = bias + gain * (internal_cue - bias)
    variance = motor_var * combined_var / (
        motor_var + combined_var
    )

    return mean, variance


def causal_log_likelihoods(
    visual_cue,
    internal_cue,
    bias,
    motor_sd,
    combined_sd,
    visual_sd,
    rotation_sd,
):
    """Compute conditional log likelihoods under H0 and H1."""

    if visual_sd <= 0 or rotation_sd <= 0:
        raise ValueError("Standard deviations must be positive.")

    mean, hand_var = hand_posterior_from_internal(
        internal_cue,
        bias,
        motor_sd,
        combined_sd,
    )

    variance_h0 = hand_var + visual_sd ** 2
    variance_h1 = variance_h0 + rotation_sd ** 2

    log_l0 = norm.logpdf(
        visual_cue,
        loc=mean,
        scale=np.sqrt(variance_h0),
    )

    log_l1 = norm.logpdf(
        visual_cue,
        loc=mean,
        scale=np.sqrt(variance_h1),
    )

    return log_l0, log_l1
