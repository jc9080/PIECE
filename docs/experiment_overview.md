# Experimental Overview

## Research question

How does the sensorimotor system distinguish errors caused by intrinsic motor variability from those caused by external disturbances, and decide which errors should drive adaptation?

The original study by Kim, Chua, and Hu (2025) examines whether the motor system adapts to **externally generated errors (EGE)** while largely discounting **internally generated errors (IGE)**, and proposes the Bayesian **Parsing of Internal and External Causes of Error (PIECE)** model to explain that behavior.

## Experimental design

![Schematic of the PIECE experimental design and triplet adaptation measure](../assets/experimental_design.svg)

*Original explanatory schematic based on the methods of Kim et al. (2025). It is not a reproduction of a figure from the article; directions and angles are illustrative, not to scale.*

### Participants and task

- **Participants:** 16 healthy young adults recruited from the University of British Columbia (8 women; ages 19–29).
- **Apparatus:** Graphics tablet and stylus, with hand position displayed as a cursor on a monitor that obscured direct view of the hand.
- **Task:** Make fast, accurate reaches toward a target **9 cm** from the starting position.
- **Feedback manipulation:** The displayed cursor could be rotated relative to the true hand direction.

### What was manipulated?

The primary experimental manipulation was **visuomotor rotation**, or EGE:

- Rotation angles: **−4°, −2°, 0°, +2°, +4°**.
- The experiment also included *target-jump trials*, analyzed separately in the supplementary material. This project's initial reproduction focuses on visuomotor rotation.
- Perturbation trials were separated by unperturbed (*null*) trials. The rotation conditions were pseudorandomized.

### What was observed?

- **Reach angle:** Angular deviation of the hand trajectory from the straight-ahead target, measured at peak radial velocity; used as the operational measure of IGE.
- **EGE:** Experimentally imposed visual cursor rotation.
- **Single-trial adaptation:** Change in reach angle on the trial immediately after versus immediately before a perturbation:

  `adaptation_t = reach_angle_(t+1) - reach_angle_(t-1)`

This triplet measure avoids directly subtracting the perturbation-trial hand angle from the outcome, which would mechanically introduce IGE into the adaptation measure.

### Experimental schedule

- **Baseline:** 70 unperturbed reaches per participant.
- **Experimental phase:** 18 blocks × 100 trials = **1,800 trials** per participant.
- **Perturbation schedule:** Each of the five visuomotor rotation levels occurred 100 times per participant, alongside null trials and target-jump conditions.

## Main behavioral finding

Participants showed a strong, approximately linear adaptation response to **EGE** but almost no systematic adaptation to **IGE**, even when errors were similar in magnitude. The article reports a group-level binned regression slope of approximately **−0.594** for EGE versus **−0.043** for IGE (Figure 2).

## How PIECE explains the finding

The PIECE model integrates three sources of information:

1. **Visual cue** (`x_v`): Where the feedback cursor appears.
2. **Proprioceptive cue** (`x_p`): Information about actual hand position.
3. **Motor predictive cue** (`x_u`): Prediction of hand position based on the motor command.

Using Bayesian causal inference, the model estimates whether visual feedback was externally perturbed. This probability weights an estimate of the perturbation magnitude, producing a corrective motor response in the opposite direction. Unlike a simple hand-to-target alignment model, PIECE specifically estimates the *external* cause of error.

## Reproduction objectives

This repository aims to independently implement the published mathematical model in Python using the authors' experimental dataset. Planned milestones include:

1. Validate the dataset and reproduce behavioral analysis (Figure 2).
2. Implement the PIECE causal inference and state estimation equations.
3. Fit participant-specific parameters with maximum likelihood estimation (MLE).
4. Reproduce model simulations and posterior predictive checks.
5. Compare PIECE with PReMo, PEA, and REM using the Bayesian Information Criterion (BIC).

These are **project objectives**, not claims that all results have already been reproduced.

## Data and source

- **Article:** Kim, H. E., Chua, R., & Hu, D. (2025). *Causal inference, prediction and state estimation in sensorimotor learning*. Proceedings of the Royal Society B, 292, 20251320. https://doi.org/10.1098/rspb.2025.1320
- **Original dataset and code:** https://osf.io/pmqu5/
