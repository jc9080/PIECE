import numpy as np
from scipy.integrate import quad

from src.piece.likelihood import (
    hand_posterior_from_internal,
    causal_log_likelihoods,
)


def test_hand_posterior():
    mean, variance = hand_posterior_from_internal(
        internal_cue=1.0,
        bias=0.0,
        motor_sd=2.0,
        combined_sd=1.0,
    )

    assert np.isclose(mean, 0.8)
    assert np.isclose(variance, 0.8)


def test_large_discrepancy_favors_perturbation():
    log_l0, log_l1 = causal_log_likelihoods(
        visual_cue=10.0,
        internal_cue=0.0,
        bias=0.0,
        motor_sd=2.0,
        combined_sd=1.0,
        visual_sd=1.0,
        rotation_sd=4.0,
    )

    assert log_l1 > log_l0


def test_likelihood_normalization():
    params = dict(
        internal_cue=0.0,
        bias=0.0,
        motor_sd=2.0,
        combined_sd=1.0,
        visual_sd=1.0,
        rotation_sd=4.0,
    )

    for hypothesis in (0, 1):
        integral, _ = quad(
            lambda x: np.exp(
                causal_log_likelihoods(
                    visual_cue=x,
                    **params,
                )[hypothesis]
            ),
            -np.inf,
            np.inf,
        )

        assert np.isclose(integral, 1.0, atol=1e-8)
