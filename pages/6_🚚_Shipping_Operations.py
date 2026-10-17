import streamlit as st
from pathlib import Path
from src.data_loader import load_raw_data
from src.preprocessing import clean_and_enrich, apply_filters
from src.analytics import ship_mode_breakdown, weekday_pattern, kpis
from src.visualizations import bar_chart

st.set_page_config(page_title="Shipping Operations", page_icon="🚚", layout="wide")
css = Path(__file__).parent.parent / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)


@st.cache_data
def _load():
    return clean_and_enrich(load_raw_data())


df = _load()
st.sidebar.header("🔎 Filters")
years = st.sidebar.multiselect("Year", sorted(df["Order Year"].unique()))
filtered = apply_filters(df, years=years)

st.title("🚚 Shipping Operations")
k = kpis(filtered)

c1, c2, c3 = st.columns(3)
c1.metric("📦 Avg Ship Lag", f"{k['avg_ship_lag']:.1f} days")
c2.metric("🧾 Orders", f"{k['orders']:,}")
c3.metric("🚚 Ship Modes", filtered["Ship Mode"].nunique())

st.divider()

# Ship mode breakdown
ship = ship_mode_breakdown(filtered)
st.subheader("📊 Ship Mode Performance")
st.dataframe(ship, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(ship, "Ship Mode", "AvgLag",
                    title="⏱️ Avg Lag by Ship Mode"),
                    use_container_width=True)
with col2:
    st.plotly_chart(bar_chart(ship, "Ship Mode", "Orders",
                    title="📦 Order Volume by Ship Mode"),
                    use_container_width=True)

st.divider()

# Ship mode sales
st.subheader("💰 Sales by Ship Mode")
st.plotly_chart(bar_chart(ship, "Ship Mode", "Sales",
                title="Sales by Ship Mode", horizontal=True),
                use_container_width=True)

st.divider()

# Weekday pattern
st.subheader("📆 Weekday Order Pattern")
wd = weekday_pattern(filtered)
st.plotly_chart(bar_chart(wd, "Order Weekday", "Orders",
                title="Orders by Weekday"), use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(wd, "Order Weekday", "Sales",
                    title="Sales by Weekday"), use_container_width=True)
with col2:
    st.info(
        f"**Busiest Day:** {wd.loc[wd['Orders'].idxmax(), 'Order Weekday']}\n\n"
        f"**Slowest Day:** {wd.loc[wd['Orders'].idxmin(), 'Order Weekday']}\n\n"
        f"**Total Orders:** {wd['Orders'].sum():,}"
    )
