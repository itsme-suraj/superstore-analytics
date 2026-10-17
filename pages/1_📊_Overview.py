import streamlit as st
from pathlib import Path
from src.data_loader import load_raw_data
from src.preprocessing import clean_and_enrich, apply_filters
from src.analytics import kpis, monthly_trend, sales_by_category, segment_breakdown
from src.visualizations import line_trend, pie_chart, bar_chart, gauge
from src.insights import generate_insights

st.set_page_config(page_title="Overview", page_icon="📊", layout="wide")
css = Path(__file__).parent.parent / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)


@st.cache_data
def _load():
    return clean_and_enrich(load_raw_data())


df = _load()
st.sidebar.header("🔎 Filters")
years = st.sidebar.multiselect("Year", sorted(df["Order Year"].unique()))
regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()))
cats = st.sidebar.multiselect("Category", sorted(df["Category"].unique()))
segs = st.sidebar.multiselect("Segment", sorted(df["Segment"].unique()))

filtered = apply_filters(df, years=years, regions=regions, categories=cats, segments=segs)
st.title("📊 Executive Overview")
k = kpis(filtered)

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("💵 Sales", f"${k['total_sales']:,.0f}")
c2.metric("📈 Profit", f"${k['total_profit']:,.0f}")
c3.metric("🧾 Orders", f"{k['orders']:,}")
c4.metric("👥 Customers", f"{k['customers']:,}")
c5.metric("💳 AOV", f"${k['avg_order_value']:,.0f}")

st.divider()
col1, col2 = st.columns([2, 1])
with col1:
    trend = monthly_trend(filtered)
    st.plotly_chart(line_trend(trend, "Order Year-Month", "Sales",
                                "📈 Monthly Sales Trend"), use_container_width=True)
with col2:
    st.plotly_chart(gauge(max(min(k["avg_profit_margin"], 100), -100),
                          "Avg Margin %", 100), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    cat = sales_by_category(filtered)
    st.plotly_chart(pie_chart(cat, "Category", "Sales", "🍩 Sales by Category"),
                    use_container_width=True)
with col2:
    seg = segment_breakdown(filtered)
    st.plotly_chart(bar_chart(seg, "Segment", "Sales", title="👥 Sales by Segment"),
                    use_container_width=True)

st.divider()
st.subheader("💡 Auto Insights")
for i in generate_insights(filtered):
    st.markdown(f'<div class="insight-card insight-{i["type"]}">{i["icon"]} {i["text"]}</div>',
                unsafe_allow_html=True)
