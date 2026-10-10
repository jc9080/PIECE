import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("data/raw/vmr_all.csv")

# Select valid perturbation trials
data = df.loc[
    df["perturbation"] & df["adaptation"].notna()
].copy()

# Calculate participant-level means
subject_means = (
    data.groupby(["id", "rotation"])["adaptation"]
    .mean()
    .reset_index()
)

# Calculate group mean and standard error
summary = (
    subject_means.groupby("rotation")["adaptation"]
    .agg(["mean", "sem"])
    .reset_index()
)

print("\n=== ADAPTATION VS EGE ===")
print(summary.to_string(index=False))

# Create figure
plt.figure(figsize=(7, 5))

plt.errorbar(
    summary["rotation"],
    summary["mean"],
    yerr=summary["sem"],
    fmt="o-",
    capsize=4
)

plt.axhline(0, color="gray", linestyle="--")

plt.xlabel("External Error / Rotation (degrees)")
plt.ylabel("Mean Adaptation (degrees)")
plt.title("Motor Adaptation vs External Perturbation")

plt.xticks([-4, -2, 0, 2, 4])
plt.grid(alpha=0.2)
plt.tight_layout()

plt.savefig(
    "results/figures/adaptation_vs_ege.png",
    dpi=300
)

plt.show()
