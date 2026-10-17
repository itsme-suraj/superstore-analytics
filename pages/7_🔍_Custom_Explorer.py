import streamlit as st
from pathlib import Path
from src.data_loader import load_raw_data
from src.preprocessing import clean_and_enrich

st.set_page_config(page_title="Custom Explorer", page_icon="🔍", layout="wide")
css = Path(__file__).parent.parent / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)


@st.cache_data
def _load():
    return clean_and_enrich(load_raw_data())


df = _load()
st.title("🔍 Custom Data Explorer")
st.caption("Filter, sort, view, and download records from the Superstore dataset.")

with st.expander("🛠️ Advanced Filters", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        years = st.multiselect("Year", sorted(df["Order Year"].unique()))
        regions = st.multiselect("Region", sorted(df["Region"].unique()))
    with col2:
        cats = st.multiselect("Category", sorted(df["Category"].unique()))
        segs = st.multiselect("Segment", sorted(df["Segment"].unique()))
    with col3:
        ship = st.multiselect("Ship Mode", sorted(df["Ship Mode"].unique()))
        status = st.multiselect("Profit Status", sorted(df["Profit Status"].unique()))

# Apply filters
view = df.copy()
if years: view = view[view["Order Year"].isin(years)]
if regions: view = view[view["Region"].isin(regions)]
if cats: view = view[view["Category"].isin(cats)]
if segs: view = view[view["Segment"].isin(segs)]
if ship: view = view[view["Ship Mode"].isin(ship)]
if status: view = view[view["Profit Status"].isin(status)]

st.markdown(f"### 📋 {len(view):,} rows match your filters")

# Column selection
cols = st.multiselect(
    "Select columns to display",
    options=view.columns.tolist(),
    default=["Order Date", "Customer Name", "Category", "Sales", "Profit"]
)

if cols:
    st.dataframe(view[cols], use_container_width=True, height=500)

# Sorting
if cols:
    sort_col = st.selectbox("Sort by", cols)
    sort_order = st.radio("Order", ["Descending", "Ascending"], horizontal=True)
    view_sorted = view.sort_values(sort_col, ascending=(sort_order == "Ascending"))
    st.dataframe(view_sorted[cols], use_container_width=True, height=400)

# Download
st.divider()
st.subheader("⬇️ Download Filtered Data")
csv = view.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Download Filtered CSV",
    csv,
    "filtered_superstore.csv",
    "text/csv",
    use_container_width=True,
)

# Summary stats
st.divider()
st.subheader("📊 Filtered Summary")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows", f"{len(view):,}")
c2.metric("Total Sales", f"${view['Sales'].sum():,.0f}")
c3.metric("Total Profit", f"${view['Profit'].sum():,.0f}")
c4.metric("Avg Margin", f"{view['Profit Margin %'].mean():.1f}%")
