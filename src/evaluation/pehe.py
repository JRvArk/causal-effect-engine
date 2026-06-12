import numpy as np
import pandas as pd


def pehe(true_cate: pd.Series, estimated_cate: pd.Series) -> float:
    """Precision in estimation of heterogeneous effects: sqrt(mean((tau_hat - tau)^2))."""
    raise NotImplementedError


def ate_bias(true_ate: float, estimated_ate: float) -> float:
    raise NotImplementedError


def policy_risk(true_cate: pd.Series, estimated_cate: pd.Series) -> float:
    """Expected outcome loss from treating based on estimated rather than true CATE."""
    raise NotImplementedError
