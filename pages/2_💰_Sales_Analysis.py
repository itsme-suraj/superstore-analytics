import streamlit as st
import plotly.express as px
from pathlib import Path
from src.data_loader import load_raw_data
from src.preprocessing import clean_and_enrich, apply_filters
from src.analytics import (kpis, monthly_trend, sales_by_subcategory, top_products,
                            top_customers, weekday_pattern, year_over_year)
from src.visualizations import bar_chart, treemap, dual_bar

st.set_page_config(page_title="Sales Analysis", page_icon="💰", layout="wide")
css = Path(__file__).parent.parent / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)


@st.cache_data
def _load():
    return clean_and_enrich(load_raw_data())


df = _load()
st.sidebar.header("🔎 Filters")
years = st.sidebar.multiselect("Year", sorted(df["Order Year"].unique()))
cats = st.sidebar.multiselect("Category", sorted(df["Category"].unique()))
segs = st.sidebar.multiselect("Segment", sorted(df["Segment"].unique()))
filtered = apply_filters(df, years=years, categories=cats, segments=segs)

st.title("💰 Sales Analysis")
k = kpis(filtered)
c1, c2, c3 = st.columns(3)
c1.metric("Total Sales", f"${k['total_sales']:,.0f}")
c2.metric("Quantity", f"{k['total_qty']:,}")
c3.metric("Avg Discount", f"{k['avg_discount']:.1f}%")

st.divider()
yoy = year_over_year(filtered)
st.plotly_chart(dual_bar(yoy, "Order Year", "Sales", "Profit", "📅 YoY"),
                use_container_width=True)

trend = monthly_trend(filtered)
fig = px.line(trend, x="Order Year-Month", y=["Sales", "Rolling Sales 3M"],
              markers=True, title="📈 Monthly + 3M Rolling Avg")
fig.update_layout(template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.divider()
col1, col2 = st.columns(2)
with col1:
    sub = sales_by_subcategory(filtered, 12)
    st.plotly_chart(bar_chart(sub, "Sales", "Sub-Category",
                    title="🏅 Top Sub-Categories", horizontal=True),
                    use_container_width=True)
with col2:
    wd = weekday_pattern(filtered)
    st.plotly_chart(bar_chart(wd, "Order Weekday", "Orders",
                    title="📆 Weekday Orders"), use_container_width=True)

st.divider()
top_by = st.radio("Rank by", ["Sales", "Profit", "Qty"], horizontal=True)
prods = top_products(filtered, 10, top_by)
st.plotly_chart(bar_chart(prods, top_by, "Product Name",
                title=f"Top by {top_by}", horizontal=True), use_container_width=True)

st.divider()
cust = top_customers(filtered, 10)
st.plotly_chart(bar_chart(cust, "Sales", "Customer Name",
                title="👤 Top Customers", horizontal=True), use_container_width=True)

st.divider()
st.plotly_chart(treemap(filtered, ["Category", "Sub-Category"], "Sales",
                "🗺️ Sales Treemap"), use_container_width=True)
