# PIECE Model Reproduction — Implementation Scope

## Objective

Independently reimplement the original PIECE model
described in Kim, Chua, and Hu (2025).

The primary goal is faithful computational reproduction,
not model modification or extension.

## Implementation Principles

1. Follow the published mathematical formulation.
2. Verify equations against the official source code.
3. Preserve the original model assumptions.
4. Reproduce the original parameterization.
5. Use the original dataset and preprocessing procedures.
6. Match the original optimization methodology.
7. Validate numerical outputs against the reference implementation.
8. Reproduce the published behavioral and modeling results.

## Model Components

### Generative Model

Define the original probabilistic relationships among
hand position, perturbation, and sensory information.

### Bayesian Causal Inference

Compute the posterior probability of an external
perturbation using the original likelihood formulation.

### Perturbation Estimation

Implement the original state-estimation equations.

### Adaptation Prediction

Predict motor adaptation using the original model.

### Model Fitting

Estimate participant-level parameters using the
published fitting procedure.

### Numerical Validation

Compare independent implementation outputs against
the official reference implementation.

## Existing Code

- sensory_simulation.py:
  Educational simulation using illustrative parameters.
  Not part of the validated original reproduction.

- validate_dataset.py:
  Experimental data validation.

- plot_adaptation_vs_ege.py:
  Exploratory behavioral analysis.

- plot_adaptation_vs_ige.py:
  Exploratory behavioral analysis.

## Reproduction Status

- Experimental data exploration: Completed
- Behavioral calculation validation: Completed
- Exploratory behavioral analysis: Completed
- Original PIECE equations: Pending implementation
- Model fitting: Not started
- Numerical comparison with official code: Not started
- Published model results reproduction: Not started

## Reference

Kim, H. E., Chua, R., & Hu, D. (2025).
Causal inference, prediction and state estimation
in sensorimotor learning.

https://doi.org/10.1098/rspb.2025.1320

Official code:
https://github.com/ccmlab-ubc/causal-inference-piece
