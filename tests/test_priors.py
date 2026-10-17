import numpy as np
from scipy.integrate import quad

from src.piece.priors import (
    P_PERTURBED,
    P_UNPERTURBED,
    hand_prior_pdf,
    rotation_prior_pdf,
)


def test_causal_prior_normalization():
    assert np.isclose(P_PERTURBED + P_UNPERTURBED, 1.0)


def test_hand_prior_normalization():
    integral, _ = quad(
        lambda x: hand_prior_pdf(x, bias=1.0, motor_sd=2.0),
        -np.inf,
        np.inf,
    )
    assert np.isclose(integral, 1.0, atol=1e-8)


def test_rotation_prior_normalization():
    integral, _ = quad(
        lambda r: rotation_prior_pdf(r, rotation_sd=3.0),
        -np.inf,
        np.inf,
    )
    assert np.isclose(integral, 1.0, atol=1e-8)


def test_rotation_prior_symmetry():
    assert np.isclose(
        rotation_prior_pdf(-2.0, rotation_sd=3.0),
        rotation_prior_pdf(+2.0, rotation_sd=3.0),
    )
