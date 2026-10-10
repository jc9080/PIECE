"""Generative model for the PIECE framework."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class GenerativeParameters:
    """Parameters of the generative model, in degrees."""
    motor_bias: float
    motor_sd: float
    visual_sd: float
    proprioceptive_sd: float
    prediction_sd: float


def generate_observations(
    hand_position: float,
    rotation: float,
    params: GenerativeParameters,
    rng: np.random.Generator,
) -> dict:
    """Generate noisy sensory cues for one reaching trial."""

    if min(
        params.visual_sd,
        params.proprioceptive_sd,
        params.prediction_sd,
    ) <= 0:
        raise ValueError("Sensory standard deviations must be positive.")

    visual = rng.normal(
        loc=hand_position + rotation,
        scale=params.visual_sd,
    )

    proprioceptive = rng.normal(
        loc=hand_position,
        scale=params.proprioceptive_sd,
    )

    motor_prediction = rng.normal(
        loc=hand_position,
        scale=params.prediction_sd,
    )

    return {
        "hand_position": hand_position,
        "rotation": rotation,
        "visual": visual,
        "proprioceptive": proprioceptive,
        "motor_prediction": motor_prediction,
    }


if __name__ == "__main__":
    rng = np.random.default_rng(42)

    # Illustrative parameters, not fitted paper estimates.
    params = GenerativeParameters(
        motor_bias=0.5,
        motor_sd=2.0,
        visual_sd=1.0,
        proprioceptive_sd=2.0,
        prediction_sd=1.5,
    )

    # Draw an actual hand position from the motor prior.
    hand_position = rng.normal(
        loc=params.motor_bias,
        scale=params.motor_sd,
    )

    observations = generate_observations(
        hand_position=hand_position,
        rotation=4.0,
        params=params,
        rng=rng,
    )

    print("=== PIECE GENERATIVE MODEL ===")
    for name, value in observations.items():
        print(f"{name:20s}: {value:+.3f} degrees")
