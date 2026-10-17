"""Load participant-specific fixed inputs for PIECE."""

import numpy as np
import pandas as pd


def extract_motor_sd(df):
    """Return one validated motor SD per participant."""

    required = {"id", "motor_sd"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("Dataset is empty.")

    values = {}

    for participant_id, group in df.groupby("id"):
        sd = pd.to_numeric(
            group["motor_sd"], errors="coerce"
        ).to_numpy(dtype=float)

        if not np.all(np.isfinite(sd)):
            raise ValueError(
                f"{participant_id}: invalid motor_sd"
            )

        if np.any(sd <= 0):
            raise ValueError(
                f"{participant_id}: motor_sd must be positive"
            )

        if not np.allclose(sd, sd[0], rtol=0, atol=1e-10):
            raise ValueError(
                f"{participant_id}: motor_sd changes across trials"
            )

        values[participant_id] = float(sd[0])

    return values
