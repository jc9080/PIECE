import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/vmr_all.csv")

data = df.loc[
    df["perturbation"]
    & df["adaptation"].notna()
    & df["theta_maxradv_clean"].notna()
].copy()

# Remove participant-by-rotation condition means.
groups = data.groupby(["id", "rotation"])

data["IGE"] = (
    data["theta_maxradv_clean"]
    - groups["theta_maxradv_clean"].transform("mean")
)

data["adaptation_residual"] = (
    data["adaptation"]
    - groups["adaptation"].transform("mean")
)

# Overall regression
slope, intercept = np.polyfit(
    data["IGE"],
    data["adaptation_residual"],
    1
)

# Participant-specific slopes
slopes = []

for pid, g in data.groupby("id"):
    if g["IGE"].nunique() > 1:
        slopes.append(
            np.polyfit(
                g["IGE"],
                g["adaptation_residual"],
                1
            )[0]
        )

print("\n=== CLEANED IGE ANALYSIS ===")
print("Trials:", len(data))
print("Participants:", data["id"].nunique())
print("Overall slope:", slope)
print("Mean participant slope:", np.mean(slopes))
print("SD of slopes:", np.std(slopes, ddof=1))
print("IGE range:", data["IGE"].min(), data["IGE"].max())

# Plot
plt.figure(figsize=(7, 5))

plt.scatter(
    data["IGE"],
    data["adaptation_residual"],
    s=5,
    alpha=0.12
)

x = np.linspace(data["IGE"].min(), data["IGE"].max(), 100)

plt.plot(
    x,
    slope * x + intercept,
    linewidth=2,
    label=f"Slope = {slope:.3f}"
)

plt.axhline(0, color="gray", linestyle="--")

plt.xlabel("Centered Internal Error (degrees)")
plt.ylabel("Adaptation Residual (degrees)")
plt.title("Motor Adaptation vs Internal Error (Cleaned)")

plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig(
    "results/figures/adaptation_vs_ige_clean.png",
    dpi=300
)

plt.show()
