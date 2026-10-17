"""Data loading with Streamlit caching."""
import pandas as pd
import streamlit as st
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "Superstore.csv"


@st.cache_data(show_spinner="Loading dataset...")
def load_raw_data(path: str | None = None) -> pd.DataFrame:
    file = Path(path) if path else DATA_PATH
    if not file.exists():
        raise FileNotFoundError(f"Dataset not found at {file}")
    return pd.read_csv(file, encoding="latin-1")


@st.cache_data(show_spinner=False)
def get_data_info(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "cols": df.shape[1],
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1024**2, 2),
        "missing": int(df.isna().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "columns": list(df.columns),
    }
  
