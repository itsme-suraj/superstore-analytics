import streamlit as st
from pathlib import Path
from src.data_loader import load_raw_data, get_data_info
from src.preprocessing import clean_and_enrich
from src.ui import inject_custom_css

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Superstore Analytics", 
    page_icon="🛒", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THEME MANAGEMENT ---
# Default theme setup
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

# Sidebar for Theme Toggle
with st.sidebar:
    st.markdown("### ⚙️ App Settings")
    
    # We use a radio button but format it to look like a toggle
    theme_choice = st.radio(
        "Choose Theme",
        ["🌙 Dark Mode", "☀️ Light Mode"],
        index=0 if st.session_state.theme == "dark" else 1,
        horizontal=True
    )
    
    # Detect change and reload to apply CSS perfectly
    new_theme = "dark" if "Dark" in theme_choice else "light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun() # Force reload to apply new colors cleanly
        
    st.divider()
    st.info("👈 Use the sidebar to navigate to different dashboard pages.")

# Apply the CSS based on current theme
inject_custom_css(st.session_state.theme)

# --- DATA LOADING ---
@st.cache_data(show_spinner="Loading Superstore Data...")
def _load():
    return clean_and_enrich(load_raw_data())

try:
    df = _load()
except FileNotFoundError:
    st.error("❌ `Superstore.csv` not found in the project root. Please upload it.")
    st.stop()

# --- LANDING PAGE HERO SECTION ---
# Using inline styling that adapts to the theme variables defined in ui.py
st.markdown(f"""
<div style="
    padding: 3rem 2rem; 
    border-radius: 20px; 
    background: var(--kpi-bg); 
    border: 1px solid var(--kpi-border);
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
">
    <h1 style="font-size: 3rem; margin-bottom: 0.5rem; color: var(--text-main);">
        🛒 Superstore Analytics
    </h1>
    <p style="font-size: 1.2rem; color: var(--text-muted); max-width: 600px; margin: 0 auto;">
        Executive-grade business intelligence dashboard for sales, profit, and operational metrics.
    </p>
</div>
""", unsafe_allow_html=True)

# --- DATASET OVERVIEW ---
info = get_data_info(df)
st.markdown("### 📊 Dataset Summary")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Total Records</div><div class="kpi-value">{info['rows']:,}</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Total Columns</div><div class="kpi-value">{info['cols']}</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Memory Usage</div><div class="kpi-value">{info['memory_mb']} MB</div></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">Missing Values</div><div class="kpi-value">{info['missing']}</div></div>""", unsafe_allow_html=True)

st.divider()

# --- NAVIGATION / FEATURES GRID ---
st.markdown("### 🚀 Explore Dashboard Pages")

pages_data = [
    ("📊 Overview", "Executive KPIs, revenue trends, and category mix.", "pages/1_📊_Overview.py"),
    ("💰 Sales Analysis", "Deep dive into products, customers, and quantity.", "pages/2_💰_Sales_Analysis.py"),
    ("📈 Profit Intel", "Margins, discount impact, and loss-making products.", "pages/3_📈_Profit_Intelligence.py"),
    ("🏙️ Regional Map", "State performance and geographic sales heatmap.", "pages/4_🏙️_Regional_Analysis.py"),
    ("🛍️ Product Analytics", "Category and sub-category performance breakdowns.", "pages/5_🛍️_Product_Analytics.py"),
    ("🚚 Operations", "Ship mode lag times and weekday order patterns.", "pages/6_🚚_Shipping_Operations.py"),
    ("🔍 Data Explorer", "Filter, sort, and download custom datasets.", "pages/7_🔍_Custom_Explorer.py")
]

# Render pages in a 3-column grid
cols = st.columns(3)
for idx, (title, desc, path) in enumerate(pages_data):
    with cols[idx % 3]:
        st.markdown(f"""
        <div style="
            padding: 1.5rem; 
            border-radius: 12px; 
            background: var(--kpi-bg); 
            border: 1px solid var(--kpi-border);
            height: 100%;
            margin-bottom: 1rem;
        ">
            <h4 style="color: var(--accent-color); margin-top: 0;">{title}</h4>
            <p style="color: var(--text-muted); font-size: 0.9rem;">{desc}</p>
        </div>
        """, unsafe_allow_html=True)
        # Use Streamlit buttons for actual navigation
        if st.button(f"Open {title.split(' ')[1]}", key=f"btn_{idx}", use_container_width=True):
            st.switch_page(path)

st.divider()

# --- DATA PREVIEW ---
with st.expander("📄 View Raw Dataset Preview", expanded=False):
    st.dataframe(df.head(20), use_container_width=True)
