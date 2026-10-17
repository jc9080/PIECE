import numpy as np
import pytest

from src.piece.perturbation_observation import (
    sample_perturbation_observation,
)


def test_reproducible_with_seed():
    rng1 = np.random.default_rng(42)
    rng2 = np.random.default_rng(42)

    z1 = sample_perturbation_observation(4.0, 2.0, rng1)
    z2 = sample_perturbation_observation(4.0, 2.0, rng2)

    assert np.isclose(z1, z2)


def test_observation_mean():
    rng = np.random.default_rng(42)

    z = sample_perturbation_observation(
        rotation=np.full(100000, 4.0),
        visual_sd=2.0,
        rng=rng,
    )

    assert abs(np.mean(z) - 4.0) < 0.03


def test_observation_standard_deviation():
    rng = np.random.default_rng(42)

    z = sample_perturbation_observation(
        rotation=np.full(100000, 4.0),
        visual_sd=2.0,
        rng=rng,
    )

    assert abs(np.std(z) - 2.0) < 0.03


def test_reject_invalid_visual_sd():
    rng = np.random.default_rng(42)

    with pytest.raises(ValueError):
        sample_perturbation_observation(
            rotation=4.0,
            visual_sd=0.0,
            rng=rng,
        )


def test_vectorized_observations():
    rng = np.random.default_rng(42)

    z = sample_perturbation_observation(
        rotation=np.array([-4.0, 0.0, 4.0]),
        visual_sd=np.array([2.0, 1.0, 2.0]),
        rng=rng,
    )

    assert z.shape == (3,)
    assert np.all(np.isfinite(z))
