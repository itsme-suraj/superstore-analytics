import streamlit as st
import plotly.express as px
from src.data_loader import load_raw_data
from src.preprocessing import clean_and_enrich, apply_filters
from src.analytics import kpis, monthly_trend, top_products, sales_by_subcategory
from src.ui import render_kpis, apply_chart_theme

st.set_page_config(page_title="Sales Analysis", page_icon="💰", layout="wide")
theme = st.session_state.get("theme", "dark")

@st.cache_data
def _load():
    return clean_and_enrich(load_raw_data())

df = _load()

with st.sidebar:
    st.header("🔎 Filters")
    years = st.multiselect("Year", sorted(df["Order Year"].unique()))
    cats = st.multiselect("Category", sorted(df["Category"].unique()))

filtered = apply_filters(df, years=years, categories=cats)

st.title("💰 Sales & Revenue Analysis")
st.markdown("Deep dive into product sales, quantities, and top performers.")

# KPIs
k = kpis(filtered)
render_kpis(k)

st.divider()

# Top Products Chart
st.subheader("🏆 Top 10 Best-Selling Products")
top = top_products(filtered, n=10, by="Sales")
fig_top = px.bar(top, x="Sales", y="Product Name", orientation="h",
                 color="Sales", color_continuous_scale="Viridis")
fig_top.update_layout(yaxis={'categoryorder':'total ascending'})
fig_top = apply_chart_theme(fig_top, theme)
fig_top.update_layout(coloraxis_showscale=False)
st.plotly_chart(fig_top, use_container_width=True)

st.divider()

# Sub-category chart
st.subheader("📦 Sub-Category Volume")
sub = sales_by_subcategory(filtered, top_n=12)
fig_sub = px.bar(sub, x="Sub-Category", y="Qty", color="Category")
fig_sub = apply_chart_theme(fig_sub, theme)
st.plotly_chart(fig_sub, use_container_width=True)
