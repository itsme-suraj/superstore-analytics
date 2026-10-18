import streamlit as st
import plotly.express as px
from src.data_loader import load_raw_data
from src.preprocessing import clean_and_enrich, apply_filters
from src.analytics import kpis, monthly_trend, sales_by_category, segment_breakdown, weekday_pattern
from src.insights import generate_insights
from src.ui import inject_custom_css, render_hero, render_kpis, apply_chart_theme

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# --- TOP BAR & THEME ---
colT1, colT2 = st.columns([8, 2])
with colT1:
    st.markdown("<h3 style='margin:0; padding-top:5px;'>📊 Executive Overview</h3>", unsafe_allow_html=True)
with colT2:
    theme_choice = st.radio("Theme", ["🌙 Dark", "☀️ Light"], index=0 if st.session_state.theme=="dark" else 1, horizontal=True, label_visibility="collapsed")
    new_theme = "dark" if "Dark" in theme_choice else "light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

theme = st.session_state.theme
inject_custom_css(theme)

@st.cache_data
def _load():
    return clean_and_enrich(load_raw_data())

df = _load()

# --- FULL WIDTH TOP FILTERS (No Sidebar) ---
with st.container():
    f1, f2, f3, f4 = st.columns(4)
    with f1:
        years = st.multiselect("📅 Select Year", sorted(df["Order Year"].unique()), placeholder="All Years")
    with f2:
        regions = st.multiselect("🌍 Region", sorted(df["Region"].unique()), placeholder="All Regions")
    with f3:
        cats = st.multiselect("🛍️ Category", sorted(df["Category"].unique()), placeholder="All Categories")
    with f4:
        segs = st.multiselect("👥 Segment", sorted(df["Segment"].unique()), placeholder="All Segments")

filtered = apply_filters(df, years=years, regions=regions, categories=cats, segments=segs)
k = kpis(filtered)

# --- HERO BAR ---
render_hero("Overview", "Real-time analysis of revenue, profit, and segments", 
            [f"📉 {k['orders']:,} Orders", f"👥 {k['customers']:,} Customers", f"💸 {k['avg_discount']:.1f}% Avg Disc"])

# --- CUSTOM KPI CARDS ---
render_kpis([
    ("Total Sales", f"${k['total_sales']:,.0f}", "Gross Revenue", "#38bdf8", "💵"),
    ("Total Profit", f"${k['total_profit']:,.0f}", f"Margin: {k['avg_profit_margin']:.1f}%", "#10b981", "📈"),
    ("Orders", f"{k['orders']:,}", f"AOV: ${k['avg_order_value']:,.0f}", "#a855f7", "📦"),
    ("Loss Orders", f"{k['loss_making_orders']:,}", "Needs attention", "#ef4444", "🚨")
])

st.markdown("<br>", unsafe_allow_html=True)

# --- ROW 1: CHARTS ---
c1, c2, c3 = st.columns([2, 1, 1])

with c1:
    trend = monthly_trend(filtered)
    fig1 = px.area(trend, x="Order Year-Month", y="Sales", title="📈 Monthly Sales Trend")
    fig1.update_traces(fill='tozeroy', line_color='#38bdf8')
    st.plotly_chart(apply_chart_theme(fig1, theme), use_container_width=True)

with c2:
    cat_data = sales_by_category(filtered)
    fig2 = px.pie(cat_data, names="Category", values="Sales", title="🍩 Category Share", hole=0.6)
    st.plotly_chart(apply_chart_theme(fig2, theme), use_container_width=True)

with c3:
    wd = weekday_pattern(filtered)
    fig3 = px.bar(wd, x="Order Weekday", y="Orders", title="📆 Weekday Orders")
    fig3.update_traces(marker_color='#a855f7')
    st.plotly_chart(apply_chart_theme(fig3, theme), use_container_width=True)

# --- ROW 2: CHARTS & INSIGHTS ---
c4, c5 = st.columns([2, 1])

with c4:
    seg_data = segment_breakdown(filtered)
    fig4 = px.bar(seg_data, x="Sales", y="Segment", orientation="h", title="👥 Sales by Segment", color="Segment")
    fig4.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(apply_chart_theme(fig4, theme), use_container_width=True)

with c5:
    st.markdown(f"<h4 style='color: var(--text-main); margin-bottom: 15px;'>💡 Auto Insights</h4>", unsafe_allow_html=True)
    insights = generate_insights(filtered)
    for i in insights[:3]: # Top 3 insights
        st.markdown(f'<div class="insight"><div class="t">{i["icon"]} Insight</div><div class="b">{i["text"]}</div></div>', unsafe_allow_html=True)
