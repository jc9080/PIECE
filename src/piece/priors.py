"""Prior distributions for the PIECE model."""

from scipy.stats import norm

# Causal prior probabilities
P_PERTURBED = 0.5
P_UNPERTURBED = 0.5


def hand_prior_pdf(x_h, bias, motor_sd):
    """
    Hand-position prior.

    x_h ~ Normal(bias, motor_sd^2)
    """
    if motor_sd <= 0:
        raise ValueError("motor_sd must be positive.")

    return norm.pdf(
        x_h,
        loc=bias,
        scale=motor_sd,
    )


def rotation_prior_pdf(r, rotation_sd):
    """
    External-rotation prior.

    r ~ Normal(0, rotation_sd^2)
    """
    if rotation_sd <= 0:
        raise ValueError("rotation_sd must be positive.")

    return norm.pdf(
        r,
        loc=0.0,
        scale=rotation_sd,
    )
