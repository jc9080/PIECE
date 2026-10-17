import numpy as np
import pytest

from src.piece.visual_uncertainty import (
    visual_error_magnitude,
    visual_uncertainty,
)


def test_positive_error():
    assert np.isclose(
        visual_error_magnitude(1.0, 4.0), 5.0
    )


def test_negative_error():
    assert np.isclose(
        visual_error_magnitude(-1.0, -4.0), 5.0
    )


def test_zero_error():
    assert np.isclose(
        visual_error_magnitude(2.0, -2.0), 0.0
    )


def test_linear_uncertainty():
    # Illustrative coefficients, not published estimates.
    result = visual_uncertainty(5.0, alpha=1.0, beta=0.2)
    assert np.isclose(result, 2.0)


def test_uncertainty_increases_with_error():
    errors = np.array([0.0, 2.0, 4.0, 6.0])
    sigma = visual_uncertainty(errors, alpha=1.0, beta=0.2)
    assert np.all(np.diff(sigma) > 0)


def test_invalid_error():
    with pytest.raises(ValueError):
        visual_uncertainty(-1.0, alpha=1.0, beta=0.2)
