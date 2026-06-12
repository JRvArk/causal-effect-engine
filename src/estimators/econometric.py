import pandas as pd


def difference_in_differences(
    df: pd.DataFrame,
    treatment: str,
    outcome: str,
    time_col: str,
    unit_col: str,
) -> dict:
    raise NotImplementedError


def instrumental_variables(
    df: pd.DataFrame,
    treatment: str,
    outcome: str,
    instrument: str,
    covariates: list[str],
) -> dict:
    raise NotImplementedError


def regression_discontinuity(
    df: pd.DataFrame,
    running_var: str,
    outcome: str,
    cutoff: float,
    bandwidth: float | None = None,
) -> dict:
    raise NotImplementedError
