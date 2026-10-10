# PIECE — Experimental Protocol Notes

## Reference

Kim, H. E., Chua, R., & Hu, D. (2025).
*Causal inference, prediction and state estimation in sensorimotor learning.*
Proceedings of the Royal Society B.

https://doi.org/10.1098/rspb.2025.1320

## 1. Experiment Overview

- Participants: 16 healthy adults
- Experimental paradigm: Visuomotor Rotation (VMR)
- Task: Perform rapid and accurate reaching movements toward a visual target
- Baseline: 70 trials per participant
- Experimental phase: 18 blocks × 100 trials = 1,800 trials
- Total: 1,870 trials per participant
- Total across 16 participants: 29,920 trials before exclusions

### Research Objective

To investigate how the sensorimotor system distinguishes
internally generated errors (IGE) from externally generated
errors (EGE), and how each contributes to motor adaptation.

## 2. Experimental Setup

- Device: Graphics tablet and stylus
- Monitor refresh rate: 144 Hz
- Hand position sampling rate: 200 Hz
- Target distance: 9 cm
- Starting position hold time: 300–500 ms
- Movement time criterion: 500 ms
- Direct vision of the hand and arm: Blocked
- Cursor: Represents stylus position on the screen

Participants were instructed to reach directly toward the
target as quickly and accurately as possible.

They were discouraged from explicitly changing their aim
in response to cursor perturbations.

## 3. Perturbation Rules

### Perturbation Type

Visuomotor rotation applied to the displayed cursor.

### Rotation Magnitudes

- 0 degrees: No perturbation
- +2 degrees / -2 degrees
- +4 degrees / -4 degrees

### Application Rules

1. Perturbations were applied on a trial-by-trial basis.
2. The rotation angle was fixed within each trial.
3. The rotation remained active during outward and return movements.
4. The cursor position changed continuously as the hand moved.
5. The rotation magnitude could differ between trials.
6. Perturbation trials were randomized.
7. Null and perturbation trials alternated during experimental blocks.
8. The experimenter did not physically manipulate the participant's hand.

Half of the null trials had no visual cursor feedback during
the reach. The remaining null trials provided veridical feedback.

## 4. Trial Procedure

1. Move the cursor to the starting position.
2. Maintain the starting position for 300–500 ms.
3. A visual target appears 9 cm away.
4. Reach quickly and accurately toward the target.
5. The cursor displays the preassigned rotation, if applicable.
6. Hand position is continuously recorded at 200 Hz.
7. Movement ends when velocity falls below the endpoint threshold.
8. Frozen endpoint cursor feedback is shown for 500 ms.
9. Return to the starting position for the next trial.

## 5. Error Definitions

### Internally Generated Error (IGE)

The deviation of the actual reaching movement from
the target direction.

IGE is not intentionally imposed by the experimenter.

Reach angle was measured at peak movement velocity.

For a target direction of zero degrees:

    IGE_t = hand_angle_t

### Externally Generated Error (EGE)

The visuomotor rotation imposed by the experimental software.

    EGE_t = rotation_t

EGE is a known experimental manipulation.

### Total Visual Error

Using a consistent signed angular convention:

    Total_Error_t = IGE_t + EGE_t

Example:

    Hand angle:       +1 degree
    Cursor rotation:  +4 degrees
    Total error:      +5 degrees

IGE and EGE are continuous error components,
not mutually exclusive classification labels.

Both may be nonzero within the same trial.

## 6. Measurement and Timing

### Hand Angle

The hand angle is calculated using hand position
at peak movement velocity relative to the starting point
and the target direction.

It is not defined using the final endpoint position.

### Perturbation Angle

The perturbation angle is assigned by the experimental software.

It is not estimated from the participant's final hand position.

The same rotation is maintained throughout a perturbation trial.

### Movement Endpoint

Movement endpoint is defined separately from peak velocity.

The experiment uses the endpoint to determine when the reach
has finished and to provide frozen visual feedback.

## 7. Adaptation Measurement

Single-trial adaptation is calculated using the
reach angles immediately before and after
the perturbation trial.

    Adaptation_t = ReachAngle_(t+1) - ReachAngle_(t-1)

Where:

- t-1: Pre-perturbation null trial
- t: Perturbation trial
- t+1: Post-perturbation null trial

The measurement captures the change in movement direction
following exposure to a perturbation.

## 8. PIECE Model Objective

PIECE stands for:

Parsing of Internal and External Causes of Error.

The model combines two computational processes:

### 8.1 Bayesian Causal Inference

Estimate the probability that an external perturbation occurred
given sensory observations and motor predictions.

### 8.2 State Estimation

Estimate the magnitude of the external perturbation.

### 8.3 Motor Adaptation

Use the inferred perturbation probability and magnitude
to predict subsequent motor corrections.

## 9. Experimental Data vs. Model Inference

Experimentally measured or controlled quantities:

- Participant identifier
- Trial number
- Hand movement angle
- Assigned cursor rotation
- Perturbation condition
- Behavioral adaptation

Latent quantities represented by the model:

- Sensory estimates
- Motor predictions
- Posterior probability of external perturbation
- Estimated perturbation magnitude

Important distinction:

The experimenter knows the imposed perturbation.

The participant must infer its likely cause and magnitude
from sensory information and internal predictions.

PIECE models this inference process rather than simply
classifying pre-labeled internal and external errors.

## 10. Implementation Notes

The Python reproduction project should:

1. Load and validate the experimental dataset.
2. Identify participants, blocks, and trial conditions.
3. Calculate IGE and EGE using the original definitions.
4. Calculate single-trial adaptation.
5. Implement the PIECE Bayesian inference equations.
6. Estimate model parameters.
7. Compare model predictions with behavioral observations.
8. Reproduce the relevant published figures.
9. Document assumptions, exclusions, and limitations.

## References and Resources

Original paper:
https://doi.org/10.1098/rspb.2025.1320

Open-access paper:
https://pmc.ncbi.nlm.nih.gov/articles/PMC12343128/

Official research repository:
https://github.com/ccmlab-ubc/causal-inference-piece

Note: These notes summarize the published experimental protocol.
The original publication and source code remain the authoritative
references for exact implementation and analysis details.
