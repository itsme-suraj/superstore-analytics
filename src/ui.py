import streamlit as st
import plotly.express as px

def inject_custom_css(theme="dark"):
    if theme == "dark":
        css_vars = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        #MainMenu, footer {visibility: hidden;}
        .block-container {padding: 1rem 2rem 2rem !important; max-width: 100% !important;}
        .stApp { background: radial-gradient(1100px 500px at 8% -8%, rgba(124,58,237,.20), transparent 60%), radial-gradient(900px 400px at 100% 0%, rgba(56,189,248,.10), transparent 60%), #0b0e1a; font-family: 'Inter', sans-serif;}
        
        /* Hero Bar */
        .hero { background: linear-gradient(120deg, #1e1b4b 0%, #312e81 45%, #7c3aed 100%); border-radius: 12px; padding: 12px 20px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 20px rgba(124,58,237,.25);}
        .hero h1 { margin: 0; font-size: 1.4rem; color: #fff; font-weight: 800;}
        .hero p { margin: 2px 0 0; color: #c7d2fe; font-size: .85rem;}
        .chip { padding: 4px 12px; border-radius: 999px; background: rgba(255,255,255,.15); color: #fff; font-size: .75rem; font-weight: 600;}
        
        /* KPI Cards */
        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 10px 0 20px;}
        .kpi { background: linear-gradient(145deg, #161a2e, #1c2140); border: 1px solid rgba(255,255,255,.07); border-left: 4px solid var(--accent); border-radius: 12px; padding: 15px; position: relative;}
        .kpi-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: .08em; color: #9aa3c7; font-weight: 600;}
        .kpi-value { font-size: 1.6rem; font-weight: 800; color: #fff; margin-top: 4px;}
        .kpi-sub { font-size: 0.8rem; color: #5eead4; margin-top: 4px; font-weight: 500;}
        
        /* Insight Box */
        .insight { background: #141830; border: 1px solid rgba(255,255,255,.07); border-left: 4px solid #7c5cff; border-radius: 12px; padding: 12px 15px; margin-bottom: 10px;}
        .insight .t { font-weight: 700; color: #fff; margin-bottom: 4px; font-size: 0.95rem;}
        .insight .b { color: #b6bedc; font-size: .85rem; line-height: 1.4;}
        
        /* Charts Box */
        div[data-testid="stPlotlyChart"] { background: rgba(20,24,48,.55); border: 1px solid rgba(255,255,255,.06); border-radius: 12px; padding: 5px;}
        
        /* Top Filters */
        div[data-testid="stSelectbox"] > div, div[data-testid="stMultiSelect"] > div { background-color: #161a2e !important; border: 1px solid rgba(255,255,255,.15) !important; color: white !important;}
        </style>
        """
    else:
        css_vars = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        #MainMenu, footer {visibility: hidden;}
        .block-container {padding: 1rem 2rem 2rem !important; max-width: 100% !important;}
        .stApp { background: #f8fafc; font-family: 'Inter', sans-serif;}
        
        /* Hero Bar */
        .hero { background: linear-gradient(120deg, #3b82f6 0%, #2563eb 100%); border-radius: 12px; padding: 12px 20px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(37,99,235,.2);}
        .hero h1 { margin: 0; font-size: 1.4rem; color: #fff; font-weight: 800;}
        .hero p { margin: 2px 0 0; color: #dbeafe; font-size: .85rem;}
        .chip { padding: 4px 12px; border-radius: 999px; background: rgba(255,255,255,.2); color: #fff; font-size: .75rem; font-weight: 600;}
        
        /* KPI Cards */
        .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin: 10px 0 20px;}
        .kpi { background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid var(--accent); border-radius: 12px; padding: 15px; position: relative; box-shadow: 0 2px 10px rgba(0,0,0,.03);}
        .kpi-title { font-size: 0.75rem; text-transform: uppercase; letter-spacing: .08em; color: #64748b; font-weight: 600;}
        .kpi-value { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin-top: 4px;}
        .kpi-sub { font-size: 0.8rem; color: #059669; margin-top: 4px; font-weight: 500;}
        
        /* Insight Box */
        .insight { background: #ffffff; border: 1px solid #e2e8f0; border-left: 4px solid #2563eb; border-radius: 12px; padding: 12px 15px; margin-bottom: 10px; box-shadow: 0 2px 8px rgba(0,0,0,.04);}
        .insight .t { font-weight: 700; color: #0f172a; margin-bottom: 4px; font-size: 0.95rem;}
        .insight .b { color: #475569; font-size: .85rem; line-height: 1.4;}
        
        /* Charts Box */
        div[data-testid="stPlotlyChart"] { background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 5px; box-shadow: 0 2px 10px rgba(0,0,0,.02);}
        </style>
        """
    st.markdown(css_vars, unsafe_allow_html=True)

def render_hero(title, subtitle, chips):
    chips_html = "".join([f'<span class="chip">{c}</span>' for c in chips])
    st.markdown(f"""
    <div class="hero">
        <div class="hero-left">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        <div class="hero-right" style="display:flex; gap:8px;">
            {chips_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpis(kpis_list):
    # kpis_list = [("Label", "Value", "Subtext", "Color", "Icon"), ...]
    html = '<div class="kpi-grid">'
    for label, val, sub, color, icon in kpis_list:
        html += f"""
        <div class="kpi" style="--accent: {color};">
            <div style="position:absolute; right:15px; top:15px; font-size:1.5rem; opacity:0.2;">{icon}</div>
            <div class="kpi-title">{label}</div>
            <div class="kpi-value">{val}</div>
            <div class="kpi-sub">{sub}</div>
        </div>
        """
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def apply_chart_theme(fig, theme="dark", height=300):
    bg = "rgba(0,0,0,0)"
    font_color = "#FAFAFA" if theme == "dark" else "#1E293B"
    grid_color = "rgba(255,255,255,0.05)" if theme == "dark" else "rgba(0,0,0,0.05)"
    
    fig.update_layout(
        paper_bgcolor=bg, plot_bgcolor=bg, height=height,
        font=dict(family="Inter, sans-serif", color=font_color, size=12),
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        colorway=px.colors.qualitative.Bold
    )
    fig.update_xaxes(showgrid=True, gridcolor=grid_color, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=grid_color, zeroline=False)
    return fig
