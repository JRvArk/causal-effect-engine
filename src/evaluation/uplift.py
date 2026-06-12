import pandas as pd


def qini_curve(
    df: pd.DataFrame,
    treatment: str,
    outcome: str,
    uplift_score: str,
) -> pd.DataFrame:
    """Returns cumulative incremental gains by decile of predicted uplift."""
    raise NotImplementedError


def auuc(df: pd.DataFrame, treatment: str, outcome: str, uplift_score: str) -> float:
    """Area under the uplift curve."""
    raise NotImplementedError


def uplift_by_decile(
    df: pd.DataFrame,
    treatment: str,
    outcome: str,
    uplift_score: str,
) -> pd.DataFrame:
    raise NotImplementedError
