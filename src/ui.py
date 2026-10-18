import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def inject_custom_css(theme="dark"):
    # Load base CSS
    css_path = "assets/style.css"
    with open(css_path) as f:
        base_css = f.read()
    
    # Theme variables
    if theme == "dark":
        root_vars = """
        :root {
            --bg-color: #0E1117;
            --text-main: #FAFAFA;
            --text-muted: #A0AAB5;
            --kpi-bg: linear-gradient(145deg, #1E232F, #161A24);
            --kpi-border: rgba(255,255,255,0.05);
            --insight-bg: #1A1F2B;
            --accent-color: #38BDF8; /* Light Blue */
        }
        .stApp { background-color: #0E1117; }
        """
    else:
        root_vars = """
        :root {
            --bg-color: #F8FAFC;
            --text-main: #1E293B;
            --text-muted: #64748B;
            --kpi-bg: #FFFFFF;
            --kpi-border: #E2E8F0;
            --insight-bg: #FFFFFF;
            --accent-color: #2563EB; /* Blue */
        }
        .stApp { background-color: #F8FAFC; }
        """
    
    st.markdown(f"<style>{root_vars}\n{base_css}</style>", unsafe_allow_html=True)

def render_kpis(kpi_dict):
    """Renders beautiful custom HTML KPI cards."""
    html = '<div class="kpi-grid">'
    
    # Card 1: Sales
    html += f"""
    <div class="kpi-card">
        <div class="kpi-icon">💵</div>
        <div class="kpi-title">Total Sales</div>
        <div class="kpi-value">${kpi_dict['total_sales']:,.0f}</div>
        <div class="kpi-sub">↑ Revenue</div>
    </div>
    """
    # Card 2: Profit
    html += f"""
    <div class="kpi-card">
        <div class="kpi-icon">📈</div>
        <div class="kpi-title">Total Profit</div>
        <div class="kpi-value">${kpi_dict['total_profit']:,.0f}</div>
        <div class="kpi-sub">Margin: {kpi_dict['avg_profit_margin']:.1f}%</div>
    </div>
    """
    # Card 3: Orders
    html += f"""
    <div class="kpi-card">
        <div class="kpi-icon">📦</div>
        <div class="kpi-title">Total Orders</div>
        <div class="kpi-value">{kpi_dict['orders']:,}</div>
        <div class="kpi-sub">Avg Value: ${kpi_dict['avg_order_value']:,.0f}</div>
    </div>
    """
    # Card 4: Customers
    html += f"""
    <div class="kpi-card">
        <div class="kpi-icon">👥</div>
        <div class="kpi-title">Customers</div>
        <div class="kpi-value">{kpi_dict['customers']:,}</div>
        <div class="kpi-sub">Active Base</div>
    </div>
    """
    
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def apply_chart_theme(fig, theme="dark"):
    """Makes Plotly charts transparent and theme-aware."""
    bg_color = "rgba(0,0,0,0)"
    font_color = "#FAFAFA" if theme == "dark" else "#1E293B"
    grid_color = "rgba(255,255,255,0.1)" if theme == "dark" else "rgba(0,0,0,0.05)"
    
    fig.update_layout(
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font=dict(family="Inter, sans-serif", color=font_color),
        margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        colorway=px.colors.qualitative.Bold
    )
    
    fig.update_xaxes(showgrid=True, gridcolor=grid_color, zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor=grid_color, zeroline=False)
    return fig
