# PIECE Mathematical Specification

**Project:** Independent reproduction of the original PIECE model  
**Paper:** Kim, Chua & Hu (2025), *Causal inference, prediction and state estimation in sensorimotor learning*  
**DOI:** https://doi.org/10.1098/rspb.2025.1320  
**Official repository:** https://github.com/ccmlab-ubc/causal-inference-piece  
**Status:** Mathematical specification draft, grounded in the published equations. Implementation details noted as pending are **not yet verified against the original source code**.

## 1. Purpose and scope

PIECE (Parsing of Internal and External Causes of Error) models how an observer infers whether an observed movement error comes from an external perturbation, estimates that perturbation, and adapts motor output accordingly. The target is faithful reproduction, not modification or data augmentation.

## 2. Symbols and observability

| Symbol | Definition | Availability in behavioral CSV |
|---|---|---|
| $x_h$ | Actual hand position/direction | Hand-angle proxy (`theta_maxradv`) |
| $r$ | True applied visuomotor rotation | `rotation` |
| $x_v$ | Noisy visual cue | Latent perceptual quantity; physical cursor angle can be reconstructed |
| $x_p$ | Proprioceptive cue | Latent, not directly measured |
| $x_u$ | Motor predictive cue | Latent, not directly measured |
| $C$ | Causal hypothesis: perturbed (`pert`) or not (`not pert`) | Inferred internally, not an observed subjective label |
| $z_t$ | Noisy measurement of perturbation magnitude | Defined in model; not directly recorded as a subjective estimate |
| $\hat r_t$ | Observer's estimated external rotation | Model output |
| $b$ | Intrinsic motor bias | Model parameter |
| $\sigma_h$ | Motor-noise standard deviation | Estimated using baseline data in the paper |
| $\sigma_r$ | Width of perturbation prior | Model parameter |
| $\sigma_{v,t}$ | Trial-specific visual measurement uncertainty | Determined by original model's visual-uncertainty specification |
| $K_t$ | Bayesian weight for perturbation measurement | Derived quantity |

All angles must use a consistent signed convention and units (degrees for behavioral reporting).

## 3. Generative causal structure

The model considers two hypotheses:

- $H_0: C=\neg\mathrm{pert}$ (no external rotation; $r=0$).
- $H_1: C=\mathrm{pert}$ (external rotation may be present; $r$ follows a perturbation prior).

Visual information depends on hand position under $H_0$ and on both hand position and rotation under $H_1$. Proprioceptive and motor predictive cues provide information about hand position. The published likelihood expressions assume conditional independence of the cues given the relevant latent states.

**Important:** Generating one arbitrary random visual, proprioceptive, and predictive sample per trial is *not* the required fitting algorithm. Latent cues must be handled according to the paper's integration/likelihood and simulation procedure.

## 4. Causal inference — paper equations (2.1)–(2.6)

Bayes' rule (2.1):

$$
p(C\mid x_v,x_p,x_u)
=\frac{p(C)\,p(x_v,x_p,x_u\mid C)}{p(x_v,x_p,x_u)}.
$$

Unnormalized evidence for no perturbation (2.2)–(2.3):

$$
q_0=p(C=\neg\mathrm{pert})\int
p(x_v\mid x_h)\,p(x_p\mid x_h)\,p(x_u\mid x_h)\,
p(x_h\mid C=\neg\mathrm{pert})\,dx_h.
$$

Unnormalized evidence for perturbation (2.4)–(2.6):

$$
q_1=p(C=\mathrm{pert})\iint
p(x_h\mid C=\mathrm{pert})\,p(r\mid C=\mathrm{pert})
p(x_v\mid x_h,r)\,p(x_p\mid x_h)\,p(x_u\mid x_h)
\,dr\,dx_h.
$$

Normalize the two quantities:

$$
p(C=\mathrm{pert}\mid x_v,x_p,x_u)=\frac{q_1}{q_0+q_1},
\qquad
p(C=\neg\mathrm{pert}\mid x_v,x_p,x_u)=\frac{q_0}{q_0+q_1}.
$$

**Implementation requirement:** Use the exact original priors, sensory-noise relationships, and integration/simulation approach. The equations above state the model logic; they do not by themselves determine all numerical settings.

## 5. Perturbation state estimation — equations (2.7)–(2.9)

The trial-specific perturbation observation follows

$$
z_t\sim\mathcal N(r_t,\sigma_{v,t}^{2}).
$$

Under the unperturbed hypothesis, the estimated rotation is zero. Thus (2.7)–(2.8):

$$
\hat r_t=p(C=\mathrm{pert}\mid x_{v,t},x_{p,t},x_{u,t})\,K_t z_t.
$$

Bayesian weight (2.9):

$$
K_t=\frac{1/\sigma_{v,t}^{2}}{1/\sigma_{v,t}^{2}+1/\sigma_r^{2}}
=\frac{\sigma_r^2}{\sigma_r^2+\sigma_{v,t}^2}.
$$

The paper assumes independent trial-by-trial effects with no carried-over perturbation memory for this protocol.

## 6. Motor output — equations (2.10)–(2.11)

$$
x_{h,t+1}=-\hat r_t+b+\epsilon_{t+1},
\qquad
\epsilon_{t+1}\sim\mathcal N(0,\sigma_h^2).
$$

This predicts an opposite-signed motor correction, adjusted by motor bias and stochastic motor variability.

**Distinction:** Observed `adaptation` in the CSV is the change in hand angle from the preceding to following null trials; do not blindly equate it with a simulated next-trial absolute hand position without reproducing the paper's behavioral observation mapping.

## 7. Relationship to the dataset

Previously checked on the local dataset:

- `total error = theta_maxradv + rotation` for 7,972 valid rows.
- `adaptation_t = theta_maxradv_(t+1) - theta_maxradv_(t-1)` for 7,884 valid trials.
- `perturbation=True` is a designated experimental-trial type, even for `rotation=0`.

These are **behavioral data checks**, not a validation of the PIECE model likelihood or fit.

## 8. Fit and parameter verification checklist

Before implementing a claim of exact paper reproduction, verify against the official `src` package and `experiment-1/scripts/model-fitting.ipynb`:

- [ ] Exact distribution and prior parameters for $x_h$, $r$, and $C$.
- [ ] Exact functional dependence of $\sigma_{v,t}$ on error magnitude.
- [ ] Whether and precisely how $x_p$ and $x_u$ are combined during fitting.
- [ ] Which participant-specific parameters are free, fixed, or estimated from baseline.
- [ ] Sampling/integration method, numerical tolerances, and random seeds.
- [ ] Likelihood of observed behavior and fitting objective.
- [ ] Bounds, initialization, optimizer, and convergence criteria.
- [ ] Data exclusions and trial-to-prediction alignment.
- [ ] Independent numerical checks against published/reference outputs.

Do **not** label any of these as verified solely on the basis of an illustrative sensory simulator.

## 9. Suggested implementation modules

| Module | Responsibility | Status |
|---|---|---|
| `src/piece/sensory_simulation.py` | Educational illustration only | Separate from reproduction |
| `src/piece/original_model.py` | Faithful causal inference + state estimation | Pending |
| `src/piece/model_fitting.py` | Published participant-level fitting procedure | Pending |
| `scripts/validate_dataset.py` | Behavioral data checks | Implemented |
| `tests/test_original_model.py` | Normalization and reference parity checks | Pending |

## 10. Reference materials

1. Kim HE, Chua R, Hu D (2025). *Causal inference, prediction and state estimation in sensorimotor learning*. Proceedings of the Royal Society B. DOI: 10.1098/rspb.2025.1320.
2. Published open access: https://pmc.ncbi.nlm.nih.gov/articles/PMC12343128/
3. Official implementation and analysis notebooks: https://github.com/ccmlab-ubc/causal-inference-piece

---

**Reproduction rule:** Every numerical or modeling assumption not explicitly verified against the published formulation and official reference code must be identified as provisional, not introduced silently.
