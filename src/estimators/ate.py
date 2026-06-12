from dataclasses import dataclass

import pandas as pd


@dataclass
class ATEResult:
    estimator: str
    ate: float
    se: float
    ci_lower: float
    ci_upper: float


def naive_difference(df: pd.DataFrame, treatment: str, outcome: str) -> ATEResult:
    """Treated vs. untreated means — the strawman confounding corrupts."""
    raise NotImplementedError


def ipw(df: pd.DataFrame, treatment: str, outcome: str, propensity_col: str) -> ATEResult:
    raise NotImplementedError


def matching(df: pd.DataFrame, treatment: str, outcome: str, covariates: list[str]) -> ATEResult:
    raise NotImplementedError


def aipw(df: pd.DataFrame, treatment: str, outcome: str, covariates: list[str]) -> ATEResult:
    """Doubly-robust: consistent if either outcome model or propensity model is correct."""
    raise NotImplementedError


def double_ml(df: pd.DataFrame, treatment: str, outcome: str, covariates: list[str]) -> ATEResult:
    """Double/Debiased ML with cross-fitting. Chernozhukov et al. (2018)."""
    raise NotImplementedError
