import pandas as pd


def s_learner(df: pd.DataFrame, treatment: str, outcome: str, covariates: list[str]) -> pd.Series:
    raise NotImplementedError


def t_learner(df: pd.DataFrame, treatment: str, outcome: str, covariates: list[str]) -> pd.Series:
    raise NotImplementedError


def x_learner(df: pd.DataFrame, treatment: str, outcome: str, covariates: list[str]) -> pd.Series:
    """Künzel et al. (2019) — handles imbalanced treatment/control group sizes well."""
    raise NotImplementedError


def dr_learner(df: pd.DataFrame, treatment: str, outcome: str, covariates: list[str]) -> pd.Series:
    raise NotImplementedError


def causal_forest(df: pd.DataFrame, treatment: str, outcome: str, covariates: list[str]) -> pd.Series:
    """Wager & Athey (2018) — honest causal forests via EconML CausalForestDML."""
    raise NotImplementedError
