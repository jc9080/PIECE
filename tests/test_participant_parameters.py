import numpy as np
import pandas as pd
import pytest

from src.piece.participant_parameters import extract_motor_sd


def test_extract_participant_motor_sd():
    df = pd.DataFrame({
        "id": ["01_i", "01_i", "02_i", "02_i"],
        "motor_sd": [1.5, 1.5, 2.0, 2.0],
    })

    result = extract_motor_sd(df)

    assert len(result) == 2
    assert np.isclose(result["01_i"], 1.5)
    assert np.isclose(result["02_i"], 2.0)


def test_reject_inconsistent_motor_sd():
    df = pd.DataFrame({
        "id": ["01_i", "01_i"],
        "motor_sd": [1.5, 1.8],
    })

    with pytest.raises(ValueError):
        extract_motor_sd(df)


def test_reject_invalid_motor_sd():
    df = pd.DataFrame({
        "id": ["01_i", "02_i"],
        "motor_sd": [0.0, 2.0],
    })

    with pytest.raises(ValueError):
        extract_motor_sd(df)


def test_reject_missing_column():
    df = pd.DataFrame({
        "id": ["01_i"],
    })

    with pytest.raises(ValueError):
        extract_motor_sd(df)


def test_reject_empty_dataset():
    df = pd.DataFrame({
        "id": [],
        "motor_sd": [],
    })

    with pytest.raises(ValueError):
        extract_motor_sd(df)
