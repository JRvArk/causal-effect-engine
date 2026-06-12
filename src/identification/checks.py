import pandas as pd


def check_overlap(
    df: pd.DataFrame,
    propensity_col: str,
    treatment_col: str,
    trim_threshold: float = 0.01,
) -> dict:
    """Flag units near 0 or 1 propensity where IPW weights explode."""
    raise NotImplementedError


def balance_diagnostics(
    df: pd.DataFrame,
    treatment_col: str,
    covariates: list[str],
) -> pd.DataFrame:
    """Standardized mean differences before and after weighting/matching."""
    raise NotImplementedError


def positivity_check(df: pd.DataFrame, treatment_col: str, covariates: list[str]) -> dict:
    raise NotImplementedError
