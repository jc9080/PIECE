"""Validate the PIECE visuomotor rotation dataset."""

from pathlib import Path

import numpy as np
import pandas as pd

DATA_PATH = Path("data/raw/vmr_all.csv")
df = pd.read_csv(DATA_PATH)

print("=== DATASET STRUCTURE ===")
print(f"Rows: {len(df):,}")
print(f"Participants: {df['id'].nunique()}")
print(f"Columns: {len(df.columns)}")
print("\nMissing values:")
print(df.isna().sum().to_string())

print("\n=== TRIAL IDENTIFIERS ===")
duplicates = df.duplicated(["id", "TN"]).sum()
print(f"Duplicate participant-trial pairs: {duplicates}")
assert duplicates == 0

print("\n=== PERTURBATION CONDITIONS ===")
print(pd.crosstab(df["rotation"], df["perturbation"]))

print("\n=== TOTAL ERROR VALIDATION ===")
valid = df["total error"].notna()
calculated = df.loc[valid, "theta_maxradv"] + df.loc[valid, "rotation"]
recorded = df.loc[valid, "total error"]

assert valid.sum() > 0
assert np.allclose(calculated, recorded, atol=1e-10)

print(f"Validated trials: {valid.sum():,}")
print(f"Max absolute error: {np.max(np.abs(calculated - recorded)):.3e}")
print("Result: PASS")

print("\n=== ADAPTATION VALIDATION ===")
comparisons = []

for pid, group in df.groupby("id"):
    group = group.set_index("TN").sort_index()

    for t, row in group.iterrows():
        if not row["perturbation"] or pd.isna(row["adaptation"]):
            continue

        if t - 1 not in group.index or t + 1 not in group.index:
            continue

        before = group.loc[t - 1, "theta_maxradv"]
        after = group.loc[t + 1, "theta_maxradv"]

        comparisons.append(
            (after - before, row["adaptation"])
        )

assert comparisons, "No adaptation trials could be validated"

comparisons = np.asarray(comparisons)
calculated = comparisons[:, 0]
recorded = comparisons[:, 1]

assert np.allclose(calculated, recorded, atol=1e-10)

print(f"Validated trials: {len(comparisons):,}")
print(f"Max absolute error: {np.max(np.abs(calculated - recorded)):.3e}")
print("Result: PASS")

print("\n=== CLEANED DATA ===")
clean = df[
    df["perturbation"]
    & df["adaptation"].notna()
    & df["theta_maxradv_clean"].notna()
]
print(f"Valid cleaned analysis trials: {len(clean):,}")

print("\nALL DATA VALIDATIONS PASSED")
