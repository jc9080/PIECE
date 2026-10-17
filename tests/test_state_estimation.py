import numpy as np
import pytest

from src.piece.state_estimation import (
    bayesian_weight,
    estimate_perturbation,
)


def test_bayesian_weight():
    weight = bayesian_weight(
        rotation_sd=3.0,
        visual_sd=np.sqrt(6.0),
    )
    assert np.isclose(weight, 0.6)


def test_estimation():
    result = estimate_perturbation(
        z=5.0,
        p_perturbed=0.8,
        rotation_sd=3.0,
        visual_sd=np.sqrt(6.0),
    )
    assert np.isclose(result, 2.4)


def test_no_perturbation_belief():
    result = estimate_perturbation(
        z=5.0,
        p_perturbed=0.0,
        rotation_sd=3.0,
        visual_sd=1.0,
    )
    assert np.isclose(result, 0.0)


def test_estimation_sign():
    result = estimate_perturbation(
        z=-4.0,
        p_perturbed=0.8,
        rotation_sd=3.0,
        visual_sd=1.0,
    )
    assert result < 0


def test_invalid_probability():
    with pytest.raises(ValueError):
        estimate_perturbation(
            z=5.0,
            p_perturbed=1.5,
            rotation_sd=3.0,
            visual_sd=1.0,
        )
