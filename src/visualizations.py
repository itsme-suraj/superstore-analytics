"""Plotly chart builders."""
import plotly.express as px
import plotly.graph_objects as go

COLOR_SEQ = px.colors.qualitative.Bold
PRIMARY = "#2E86AB"
SECONDARY = "#F18F01"


def _theme(fig, title=""):
    fig.update_layout(
        title=title, template="plotly_white",
        font=dict(family="Inter, Segoe UI, sans-serif", size=13),
        margin=dict(l=40, r=20, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(bgcolor="white", font_size=12),
    )
    return fig


def line_trend(df, x, y, title=""):
    return _theme(px.line(df, x=x, y=y, markers=True,
                          color_discrete_sequence=[PRIMARY]), title)


def bar_chart(df, x, y, color=None, title="", horizontal=False, color_seq=None):
    fig = px.bar(df, x=x, y=y, color=color,
                 orientation="h" if horizontal else "v",
                 color_discrete_sequence=color_seq or COLOR_SEQ, text_auto=".2s")
    return _theme(fig, title)


def pie_chart(df, names, values, title=""):
    fig = px.pie(df, names=names, values=values, hole=0.45,
                 color_discrete_sequence=COLOR_SEQ)
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return _theme(fig, title)


def dual_bar(df, x, y1, y2, title=""):
    fig = go.Figure()
    fig.add_bar(x=df[x], y=df[y1], name=y1, marker_color=PRIMARY)
    fig.add_bar(x=df[x], y=df[y2], name=y2, marker_color=SECONDARY)
    fig.update_layout(barmode="group")
    return _theme(fig, title)


def scatter_sales_profit(df, title=""):
    fig = px.scatter(df, x="Sales", y="Profit", color="Category",
                     size="Quantity", hover_name="Product Name",
                     color_discrete_sequence=COLOR_SEQ, opacity=0.7)
    fig.add_hline(y=0, line_dash="dash", line_color="gray")
    return _theme(fig, title)


def treemap(df, path, values, title=""):
    return _theme(px.treemap(df, path=path, values=values, color=values,
                             color_continuous_scale="Teal"), title)


def gauge(value, title, max_val=100):
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value, title={"text": title},
        gauge={
            "axis": {"range": [0, max_val]},
            "bar": {"color": PRIMARY},
            "steps": [
                {"range": [0, max_val * 0.4], "color": "#FDE68A"},
                {"range": [max_val * 0.4, max_val * 0.7], "color": "#FCD34D"},
                {"range": [max_val * 0.7, max_val], "color": "#86EFAC"},
            ],
        }))
    return _theme(fig, "")
