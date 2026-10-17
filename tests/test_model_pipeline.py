import numpy as np

from src.piece.model_pipeline import predict_hand_angle


def test_pipeline_consistency():
    # Illustrative inputs only; not fitted paper parameters.
    result = predict_hand_angle(
        visual_error=5.0,
        visual_cue=5.0,
        internal_cue=1.0,
        perturbation_observation=4.0,
        bias=0.0,
        motor_sd=2.0,
        combined_sd=1.0,
        rotation_sd=3.0,
        alpha=1.0,
        beta=0.2,
    )

    assert np.isclose(result["visual_sd"], 2.0)

    assert 0 <= result["p_perturbed"] <= 1

    expected_rotation = (
        result["p_perturbed"]
        * (9.0 / (9.0 + 4.0))
        * 4.0
    )

    assert np.isclose(
        result["estimated_rotation"],
        expected_rotation,
    )

    assert np.isclose(
        result["predicted_hand_angle"],
        -result["estimated_rotation"],
    )
