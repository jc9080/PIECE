"""Motor output prediction for the PIECE model."""

import numpy as np


def expected_hand_angle(estimated_rotation, motor_bias):
    """Expected next-trial hand angle, excluding motor noise."""
    return -np.asarray(estimated_rotation) + motor_bias


def simulate_hand_angle(
    estimated_rotation,
    motor_bias,
    motor_sd,
    rng,
):
    """Sample next-trial hand angle with Gaussian motor noise."""
    if not np.isfinite(motor_sd) or motor_sd < 0:
        raise ValueError("motor_sd must be finite and nonnegative.")

    expected = expected_hand_angle(
        estimated_rotation,
        motor_bias,
    )

    return rng.normal(loc=expected, scale=motor_sd)
