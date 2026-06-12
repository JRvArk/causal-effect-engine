import math


def e_value(point_estimate: float, se: float, null_value: float = 0.0) -> dict:
    """
    E-value: minimum strength of association an unobserved confounder must have
    with both treatment and outcome to fully explain away the observed effect.
    VanderWeele & Ding (2017).
    """
    raise NotImplementedError


def rv_sens(point_estimate: float, se: float, df_residual: int) -> dict:
    """
    Robustness value (RV): how much unobserved confounding (as partial R²)
    would be needed to bring the effect to zero or flip its sign.
    Cinelli & Hazlett (2020) — sensemakr approach.
    """
    raise NotImplementedError
