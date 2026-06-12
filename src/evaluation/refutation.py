import pandas as pd


def placebo_treatment(
    df: pd.DataFrame,
    treatment: str,
    outcome: str,
    covariates: list[str],
    n_simulations: int = 100,
) -> dict:
    """Replace treatment with a random permutation; estimate should collapse to ~0."""
    raise NotImplementedError


def random_common_cause(
    df: pd.DataFrame,
    treatment: str,
    outcome: str,
    covariates: list[str],
    n_simulations: int = 100,
) -> dict:
    """Add a random covariate; estimate should be stable."""
    raise NotImplementedError


def subset_stability(
    df: pd.DataFrame,
    treatment: str,
    outcome: str,
    covariates: list[str],
    n_subsets: int = 10,
    subset_fraction: float = 0.8,
) -> dict:
    """Estimate on random subsets; check variance across subsets."""
    raise NotImplementedError
