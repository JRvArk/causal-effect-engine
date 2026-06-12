from src.estimators.ate import ATEResult

# LaLonde (1986) RCT estimate; Dehejia & Wahba (1999) replication
LALONDE_EXPERIMENTAL_ATE = 1794.0


def compare_to_experimental(result: ATEResult, experimental_ate: float = LALONDE_EXPERIMENTAL_ATE) -> dict:
    """Return bias, relative bias, and whether CI covers the experimental benchmark."""
    raise NotImplementedError
