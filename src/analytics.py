"""KPI and aggregation functions."""
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def kpis(df):
    if df.empty:
        return {k: 0 for k in ["total_sales", "total_profit", "total_qty", "orders",
            "customers", "avg_order_value", "avg_profit_margin", "avg_discount",
            "avg_ship_lag", "loss_making_orders"]}
    return {
        "total_sales": float(df["Sales"].sum()),
        "total_profit": float(df["Profit"].sum()),
        "total_qty": int(df["Quantity"].sum()),
        "orders": int(df["Order ID"].nunique()),
        "customers": int(df["Customer ID"].nunique()),
        "avg_order_value": float(df["Sales"].sum() / df["Order ID"].nunique()),
        "avg_profit_margin": float(df["Profit Margin %"].mean()),
        "avg_discount": float(df["Discount"].mean() * 100),
        "avg_ship_lag": float(df["Ship Lag Days"].mean()),
        "loss_making_orders": int(df[df["Profit Status"] == "Loss"]["Order ID"].nunique()),
    }


@st.cache_data(show_spinner=False)
def sales_by_category(df):
    return (df.groupby("Category", as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Qty=("Quantity", "sum"))
            .sort_values("Sales", ascending=False))


@st.cache_data(show_spinner=False)
def sales_by_subcategory(df, top_n=15):
    return (df.groupby(["Category", "Sub-Category"], as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Qty=("Quantity", "sum"))
            .sort_values("Sales", ascending=False).head(top_n))


@st.cache_data(show_spinner=False)
def monthly_trend(df):
    g = (df.groupby("Order Year-Month", as_index=False)
         .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Qty=("Quantity", "sum")))
    g["Rolling Sales 3M"] = g["Sales"].rolling(3, min_periods=1).mean()
    return g


@st.cache_data(show_spinner=False)
def sales_by_region(df):
    return (df.groupby("Region", as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                 Qty=("Quantity", "sum"), Orders=("Order ID", "nunique"))
            .sort_values("Sales", ascending=False))


@st.cache_data(show_spinner=False)
def sales_by_state(df, top_n=15):
    return (df.groupby("State", as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Qty=("Quantity", "sum"))
            .sort_values("Sales", ascending=False).head(top_n))


@st.cache_data(show_spinner=False)
def segment_breakdown(df):
    return (df.groupby("Segment", as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                 Orders=("Order ID", "nunique")))


@st.cache_data(show_spinner=False)
def ship_mode_breakdown(df):
    return (df.groupby("Ship Mode", as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"),
                 AvgLag=("Ship Lag Days", "mean"), Orders=("Order ID", "nunique"))
            .sort_values("Sales", ascending=False))


@st.cache_data(show_spinner=False)
def top_products(df, n=10, by="Sales"):
    return (df.groupby(["Product ID", "Product Name"], as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Qty=("Quantity", "sum"))
            .sort_values(by, ascending=False).head(n))


@st.cache_data(show_spinner=False)
def discount_impact(df):
    return (df.groupby("Discount Bucket", as_index=False, observed=False)
            .agg(AvgProfit=("Profit", "mean"), TotalSales=("Sales", "sum"),
                 Orders=("Order ID", "nunique")))


@st.cache_data(show_spinner=False)
def top_customers(df, n=10):
    return (df.groupby(["Customer ID", "Customer Name"], as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
            .sort_values("Sales", ascending=False).head(n))


@st.cache_data(show_spinner=False)
def profit_leakage(df, n=10):
    loss = df[df["Profit"] < 0]
    if loss.empty:
        return pd.DataFrame(columns=["Product Name", "Sales", "Profit", "Orders"])
    return (loss.groupby("Product Name", as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique"))
            .sort_values("Profit", ascending=True).head(n))


@st.cache_data(show_spinner=False)
def year_over_year(df):
    return (df.groupby("Order Year", as_index=False)
            .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique")))


@st.cache_data(show_spinner=False)
def weekday_pattern(df):
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    g = (df.groupby("Order Weekday", as_index=False)
         .agg(Sales=("Sales", "sum"), Orders=("Order ID", "nunique")))
    g["Order Weekday"] = pd.Categorical(g["Order Weekday"], categories=order, ordered=True)
    return g.sort_values("Order Weekday")
