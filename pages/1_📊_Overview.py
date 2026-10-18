import streamlit as st
from src.data_loader import load_raw_data
from src.preprocessing import clean_and_enrich, apply_filters
from src.analytics import kpis, monthly_trend, sales_by_category, segment_breakdown
from src.visualizations import line_trend, pie_chart, bar_chart
from src.insights import generate_insights
from src.ui import render_kpis, apply_chart_theme, inject_custom_css
import plotly.express as px

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

# Ensure theme is loaded
theme = st.session_state.get("theme", "dark")

@st.cache_data
def _load():
    return clean_and_enrich(load_raw_data())

df = _load()

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.header("🔎 Dashboard Filters")
    years = st.multiselect("Year", sorted(df["Order Year"].unique()))
    regions = st.multiselect("Region", sorted(df["Region"].unique()))
    cats = st.multiselect("Category", sorted(df["Category"].unique()))
    segs = st.multiselect("Segment", sorted(df["Segment"].unique()))

filtered = apply_filters(df, years=years, regions=regions, categories=cats, segments=segs)

# --- HEADER ---
st.title("📊 Executive Overview")
st.markdown("Comprehensive view of sales performance and profitability.")

# --- KPI CARDS ---
k = kpis(filtered)
render_kpis(k)

st.divider()

# --- CHARTS ROW 1 ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Revenue Trend")
    trend = monthly_trend(filtered)
    fig_trend = px.area(trend, x="Order Year-Month", y="Sales", 
                        color_discrete_sequence=["#38BDF8"])
    fig_trend.update_traces(fill='tozeroy', line=dict(width=2))
    fig_trend = apply_chart_theme(fig_trend, theme)
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.subheader("🍩 Sales Mix")
    cat_data = sales_by_category(filtered)
    fig_pie = px.pie(cat_data, names="Category", values="Sales", hole=0.7)
    fig_pie.update_layout(showlegend=False)
    fig_pie.add_annotation(text=f"<b>${k['total_sales']/1000:.0f}K</b><br>Total", showarrow=False, font=dict(size=16))
    fig_pie = apply_chart_theme(fig_pie, theme)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- CHARTS ROW 2 ---
col3, col4 = st.columns(2)

with col3:
    st.subheader("👥 Segment Performance")
    seg_data = segment_breakdown(filtered)
    fig_bar = px.bar(seg_data, x="Segment", y="Sales", color="Segment")
    fig_bar = apply_chart_theme(fig_bar, theme)
    st.plotly_chart(fig_bar, use_container_width=True)

with col4:
    st.subheader("🚨 Profit Warnings")
    insights = generate_insights(filtered)
    for i in insights[:3]:  # Show top 3 insights
        icon = i['icon']
        text = i['text']
        st.markdown(f'<div class="insight-box"><b>{icon} Insight</b><br>{text}</div>', unsafe_allow_html=True)
