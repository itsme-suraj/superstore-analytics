"""Data cleaning and feature engineering."""
import pandas as pd
import numpy as np
import streamlit as st


def _safe_parse_date(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, format="mixed", dayfirst=False, errors="coerce")


@st.cache_data(show_spinner="Cleaning and engineering features...")
def clean_and_enrich(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.columns = [c.strip() for c in out.columns]
    out["Order Date"] = _safe_parse_date(out["Order Date"])
    out["Ship Date"] = _safe_parse_date(out["Ship Date"])
    out = out.dropna(subset=["Order Date", "Ship Date", "Sales", "Profit"])
    for col in ["Sales", "Profit", "Quantity", "Discount"]:
        out[col] = pd.to_numeric(out[col], errors="coerce").fillna(0)
    out["Order Year"] = out["Order Date"].dt.year
    out["Order Month"] = out["Order Date"].dt.month
    out["Order Month Name"] = out["Order Date"].dt.strftime("%b")
    out["Order Quarter"] = out["Order Date"].dt.quarter
    out["Order Weekday"] = out["Order Date"].dt.day_name()
    out["Order Year-Month"] = out["Order Date"].dt.to_period("M").astype(str)
    out["Ship Lag Days"] = (out["Ship Date"] - out["Order Date"]).dt.days.clip(lower=0)
    out["Profit Margin %"] = np.where(
        out["Sales"] > 0, (out["Profit"] / out["Sales"]) * 100, 0
    )
    out["Discount Bucket"] = pd.cut(
        out["Discount"],
        bins=[-0.01, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.8],
        labels=["0%", "1-10%", "11-20%", "21-30%", "31-40%", "41-50%", ">50%"],
    )
    out["Profit Status"] = np.where(
        out["Profit"] > 0, "Profitable",
        np.where(out["Profit"] < 0, "Loss", "Break-even")
    )
    return out.reset_index(drop=True)


def apply_filters(df, years=None, regions=None, categories=None, segments=None,
                  states=None, ship_modes=None, date_range=None):
    out = df.copy()
    if years: out = out[out["Order Year"].isin(years)]
    if regions: out = out[out["Region"].isin(regions)]
    if categories: out = out[out["Category"].isin(categories)]
    if segments: out = out[out["Segment"].isin(segments)]
    if states: out = out[out["State"].isin(states)]
    if ship_modes: out = out[out["Ship Mode"].isin(ship_modes)]
    if date_range and len(date_range) == 2:
        start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
        out = out[(out["Order Date"] >= start) & (out["Order Date"] <= end)]
    return out.reset_index(drop=True)
