import streamlit as st
from src.data_loader import load_raw_data, get_data_info
from src.preprocessing import clean_and_enrich
from src.ui import inject_custom_css, render_hero, render_kpis

st.set_page_config(page_title="Superstore Analytics", page_icon="🛒", layout="wide")

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# --- TOP BAR (Header & Theme Toggle) ---
colT1, colT2 = st.columns([8, 2])
with colT1:
    st.markdown("<h3 style='margin:0; padding-top:5px;'>🛒 Superstore Dashboard</h3>", unsafe_allow_html=True)
with colT2:
    theme_choice = st.radio("Theme", ["🌙 Dark", "☀️ Light"], index=0 if st.session_state.theme=="dark" else 1, horizontal=True, label_visibility="collapsed")
    new_theme = "dark" if "Dark" in theme_choice else "light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

inject_custom_css(st.session_state.theme)

@st.cache_data(show_spinner="Loading data...")
def _load():
    return clean_and_enrich(load_raw_data())

try:
    df = _load()
except FileNotFoundError:
    st.error("❌ `Superstore.csv` not found.")
    st.stop()

info = get_data_info(df)

# Hero Section
render_hero("Superstore Overview", "Executive sales & profit intelligence dashboard", 
            [f"📦 {info['rows']:,} Records", f"📋 {info['cols']} Columns", f"💾 {info['memory_mb']} MB"])

# KPIs
render_kpis([
    ("Total Records", f"{info['rows']:,}", "Dataset size", "#38bdf8", "🗂️"),
    ("Total Columns", f"{info['cols']}", "Features available", "#a855f7", "📋"),
    ("Data Memory", f"{info['memory_mb']} MB", "RAM usage", "#fbbf24", "💾"),
    ("Missing Values", f"{info['missing']}", "Cleaned & handled", "#10b981", "✅")
])

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Cards
st.markdown("### 🚀 Quick Navigation")
cols = st.columns(4)
pages = [
    ("📊 Overview", "pages/1_📊_Overview.py"), ("💰 Sales", "pages/2_💰_Sales_Analysis.py"),
    ("📈 Profit", "pages/3_📈_Profit_Intelligence.py"), ("🏙️ Regional", "pages/4_🏙️_Regional_Analysis.py"),
    ("🛍️ Products", "pages/5_🛍️_Product_Analytics.py"), ("🚚 Shipping", "pages/6_🚚_Shipping_Operations.py"),
    ("🔍 Explorer", "pages/7_🔍_Custom_Explorer.py")
]
for i, (name, path) in enumerate(pages):
    with cols[i % 4]:
        if st.button(name, use_container_width=True):
            st.switch_page(path)

st.markdown("<br>", unsafe_allow_html=True)

# Data Preview
with st.expander("📄 Preview Dataset", expanded=True):
    st.dataframe(df.head(15), use_container_width=True)
