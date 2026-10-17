import numpy as np
import pytest

from src.piece.adaptation import (
    expected_hand_angle,
    simulate_hand_angle,
)


def test_opposite_direction():
    result = expected_hand_angle(2.4, 0.0)
    assert np.isclose(result, -2.4)


def test_motor_bias():
    result = expected_hand_angle(2.4, 0.5)
    assert np.isclose(result, -1.9)


def test_zero_rotation():
    result = expected_hand_angle(0.0, 0.5)
    assert np.isclose(result, 0.5)


def test_reproducible_sampling():
    rng1 = np.random.default_rng(42)
    rng2 = np.random.default_rng(42)

    a = simulate_hand_angle(2.4, 0.5, 1.0, rng1)
    b = simulate_hand_angle(2.4, 0.5, 1.0, rng2)

    assert np.isclose(a, b)


def test_invalid_motor_sd():
    with pytest.raises(ValueError):
        simulate_hand_angle(
            2.4, 0.5, -1.0, np.random.default_rng(42)
        )
