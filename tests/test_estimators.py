import pytest
import pandas as pd
import numpy as np


@pytest.fixture
def rct_data():
    """Minimal synthetic RCT dataset for unit tests."""
    rng = np.random.default_rng(42)
    n = 500
    X = rng.normal(size=(n, 3))
    T = rng.binomial(1, 0.5, size=n)
    Y = 2.0 * T + X[:, 0] + rng.normal(scale=0.5, size=n)
    return pd.DataFrame({"treatment": T, "outcome": Y, "x1": X[:, 0], "x2": X[:, 1], "x3": X[:, 2]})


def test_naive_difference_recovers_ate_in_rct(rct_data):
    pytest.skip("not implemented")


def test_double_ml_ate_close_to_true(rct_data):
    pytest.skip("not implemented")


def test_causal_forest_pehe_on_ihdp():
    pytest.skip("not implemented")
