import streamlit as st
import plotly.express as px
from pathlib import Path
from src.data_loader import load_raw_data
from src.preprocessing import clean_and_enrich, apply_filters
from src.analytics import sales_by_region, sales_by_state
from src.visualizations import bar_chart, pie_chart

st.set_page_config(page_title="Regional Analysis", page_icon="🏙️", layout="wide")
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

st.title("🏙️ Regional Analysis")

# Region-wise performance
reg = sales_by_region(filtered)
st.subheader("🌍 Region-wise Performance")
st.dataframe(reg, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(bar_chart(reg, "Region", "Sales", title="Sales by Region"),
                    use_container_width=True)
with col2:
    st.plotly_chart(pie_chart(reg, "Region", "Profit", "Profit by Region"),
                    use_container_width=True)

st.divider()

# Top states
st.subheader("🏆 Top States by Sales")
top_states = sales_by_state(filtered, top_n=15)
st.plotly_chart(bar_chart(top_states, "Sales", "State",
                title="Top 15 States", horizontal=True),
                use_container_width=True)

st.divider()

# US Map
st.subheader("🗺️ US Sales Map")
state_data = filtered.groupby("State", as_index=False)["Sales"].sum()
fig = px.choropleth(
    state_data,
    locations="State",
    locationmode="USA-states",
    color="Sales",
    scope="usa",
    color_continuous_scale="Blues",
    title="Sales Heatmap by State",
)
fig.update_layout(template="plotly_white", margin=dict(l=20, r=20, t=50, b=20))
st.plotly_chart(fig, use_container_width=True)
