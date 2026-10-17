import streamlit as st
from pathlib import Path
from src.data_loader import load_raw_data
from src.preprocessing import clean_and_enrich, apply_filters
from src.analytics import sales_by_category, sales_by_subcategory, top_products
from src.visualizations import bar_chart, pie_chart, treemap

st.set_page_config(page_title="Product Analytics", page_icon="🛍️", layout="wide")
css = Path(__file__).parent.parent / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)


@st.cache_data
def _load():
    return clean_and_enrich(load_raw_data())


df = _load()
st.sidebar.header("🔎 Filters")
cats = st.sidebar.multiselect("Category", sorted(df["Category"].unique()))
filtered = apply_filters(df, categories=cats)

st.title("🛍️ Product Analytics")

# Category overview
cat = sales_by_category(filtered)
col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(pie_chart(cat, "Category", "Sales", "🍩 Category Sales Mix"),
                    use_container_width=True)
with col2:
    st.plotly_chart(bar_chart(cat, "Category", "Profit",
                    title="💰 Profit by Category"), use_container_width=True)

st.divider()

# Sub-category
st.subheader("🏅 Sub-Category Performance")
sub = sales_by_subcategory(filtered, top_n=17)
st.plotly_chart(bar_chart(sub, "Sales", "Sub-Category",
                title="Sub-Category Sales", horizontal=True),
                use_container_width=True)

st.divider()

# Treemap
st.subheader("🗺️ Category → Sub-Category Treemap")
st.plotly_chart(treemap(filtered, ["Category", "Sub-Category"], "Sales",
                "Hierarchy of Sales"), use_container_width=True)

st.divider()

# Top products table
st.subheader("🥇 Top 15 Products by Sales")
top = top_products(filtered, n=15, by="Sales")
st.dataframe(top, use_container_width=True)

st.divider()

# Top products chart
st.subheader("📊 Top Products Visualization")
st.plotly_chart(bar_chart(top, "Sales", "Product Name",
                title="Top Products", horizontal=True),
                use_container_width=True)
