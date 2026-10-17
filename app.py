"""Superstore Analytics — Main app."""
import streamlit as st
from pathlib import Path
from src.data_loader import load_raw_data, get_data_info
from src.preprocessing import clean_and_enrich

st.set_page_config(page_title="Superstore Analytics", page_icon="🛒", layout="wide")
css_path = Path(__file__).parent / "assets" / "style.css"
if css_path.exists():
    st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


@st.cache_data(show_spinner="Preparing data...")
def _load():
    return clean_and_enrich(load_raw_data())


def main():
    st.title("🛒 Superstore Sales Analytics")
    st.caption("Executive-grade analytics for sales, profit, and operations.")
    try:
        df = _load()
    except FileNotFoundError:
        st.error("❌ Superstore.csv not found. Place it in project root.")
        st.stop()

    info = get_data_info(df)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🧾 Rows", f"{info['rows']:,}")
    c2.metric("📋 Columns", info["cols"])
    c3.metric("💾 Memory", f"{info['memory_mb']} MB")
    c4.metric("⚠️ Missing", info["missing"])

    st.divider()
    st.subheader("🚀 Pages")
    cols = st.columns(3)
    pages = [
        ("📊 Overview", "KPIs, trend, category mix, auto insights"),
        ("💰 Sales Analysis", "Revenue deep-dive, top products/customers"),
        ("📈 Profit Intelligence", "Margin, discount impact, loss makers"),
        ("🏙️ Regional Analysis", "State performance + US map"),
        ("🛍️ Product Analytics", "Category & sub-category breakdown"),
        ("🚚 Shipping Operations", "Ship mode lag & weekday patterns"),
        ("🔍 Custom Explorer", "Filter + download CSV"),
    ]
    for i, (t, d) in enumerate(pages):
        with cols[i % 3]:
            st.markdown(f"### {t}\n{d}")

    st.divider()
    st.subheader("📄 Preview")
    st.dataframe(df.head(20), use_container_width=True, height=400)
    st.sidebar.success("👈 Navigate pages from the sidebar")


if __name__ == "__main__":
    main()
