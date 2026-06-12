from pathlib import Path

import duckdb
import pandas as pd

RAW_DIR = Path("data/raw")
DB_PATH = Path("data/db/causal.duckdb")


def get_connection() -> duckdb.DuckDBPyConnection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(DB_PATH))


def load_lalonde(db: duckdb.DuckDBPyConnection) -> None:
    raise NotImplementedError


def load_ihdp(db: duckdb.DuckDBPyConnection) -> None:
    raise NotImplementedError


def load_criteo(db: duckdb.DuckDBPyConnection) -> None:
    raise NotImplementedError


def load_hillstrom(db: duckdb.DuckDBPyConnection) -> None:
    raise NotImplementedError
