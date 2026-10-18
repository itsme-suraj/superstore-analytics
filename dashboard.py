"""Superstore BI Dashboard - run: streamlit run dashboard.py
Needs Superstore.csv in the same folder."""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Superstore BI", page_icon="📊", layout="wide",
                   initial_sidebar_state="collapsed")

# ───────────────────────── THEME ─────────────────────────
DARK = st.session_state.get("dark", True)
P = dict(
    bg="#0d1117" if DARK else "#f4f6fb", card="#161b26" if DARK else "#ffffff",
    bd="#262d3d" if DARK else "#e1e6f0", tx="#e8ecf5" if DARK else "#141a2b",
    mu="#8b95b0" if DARK else "#5d6785", grid="rgba(255,255,255,.07)" if DARK else "rgba(20,26,43,.08)",
    ac="#22d3ee" if DARK else "#0e7490", ac2="#f59e0b", good="#34d399" if DARK else "#059669", bad="#f87171" if DARK else "#dc2626",
)
PAL = ["#22d3ee", "#f59e0b", "#a78bfa", "#34d399", "#f472b6", "#60a5fa", "#fb923c", "#facc15"] if DARK else \
      ["#0e7490", "#d97706", "#7c3aed", "#059669", "#db2777", "#2563eb", "#ea580c", "#a16207"]

st.markdown(f"""<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');
:root{{--bg:{P['bg']};--card:{P['card']};--bd:{P['bd']};--tx:{P['tx']};--mu:{P['mu']};--ac:{P['ac']};--good:{P['good']};--bad:{P['bad']};}}
</style>""", unsafe_allow_html=True)
st.markdown("""<style>
html,body,.stApp{font-family:'Manrope',sans-serif;background:var(--bg)!important;color:var(--tx)}
header,#MainMenu,footer,[data-testid="stSidebar"],[data-testid="collapsedControl"]{display:none!important}
.block-container{max-width:100%!important;padding:.8rem 2rem 2rem!important}
.stApp p,.stApp label,.stApp span,.stApp li,.stApp h1,.stApp h2,.stApp h3,.stApp h4{color:var(--tx)}
[data-testid="stWidgetLabel"] p{color:var(--mu)!important;font-size:.78rem;font-weight:600}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div,[data-testid="stDateInput"]>div>div{background:var(--card)!important;border:1px solid var(--bd)!important;border-radius:10px!important}
div[data-baseweb="select"] input,div[data-baseweb="input"] input{color:var(--tx)!important}
span[data-baseweb="tag"]{background:var(--ac)!important}
span[data-baseweb="tag"] span{color:#fff!important}
ul[role="listbox"],div[data-baseweb="popover"]>div{background:var(--card)!important}
li[role="option"]{color:var(--tx)!important}
.topbar{display:flex;align-items:center;gap:14px;padding:6px 0 14px;border-bottom:1px solid var(--bd);margin-bottom:12px}
.logo{width:40px;height:40px;border-radius:10px;background:var(--ac);display:grid;place-items:center;font-size:20px}
.ttl{font-size:1.35rem;font-weight:800;line-height:1.1}.sub{font-size:.8rem;color:var(--mu)}
.kpi{background:var(--card);border:1px solid var(--bd);border-top:3px solid var(--c);border-radius:12px;padding:14px 16px;height:100%}
.kpi .l{font-size:.76rem;color:var(--mu);font-weight:600}
.kpi .v{font-size:1.75rem;font-weight:800;margin:2px 0}
.kpi .s{font-size:.78rem;color:var(--mu)}
.ins{background:var(--card);border:1px solid var(--bd);border-left:4px solid var(--ac);border-radius:10px;padding:12px 14px;margin-bottom:10px;font-size:.9rem;line-height:1.45}
.sec{font-size:1.05rem;font-weight:800;margin:18px 0 6px}
button[data-baseweb="tab"]{font-weight:700;font-size:.95rem;padding:10px 16px}
button[data-baseweb="tab"] p{color:var(--mu)}
button[data-baseweb="tab"][aria-selected="true"] p{color:var(--ac)}
div[data-testid="stPlotlyChart"]{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:6px}
.stButton>button,.stDownloadButton>button{background:var(--card);color:var(--tx);border:1px solid var(--bd);border-radius:10px;font-weight:700}
.stButton>button:hover,.stDownloadButton>button:hover{border-color:var(--ac);color:var(--ac)}
.box{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:18px 22px;line-height:1.7}
</style>""", unsafe_allow_html=True)

US = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
      "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
      "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
      "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
      "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
      "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
      "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
      "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
      "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT",
      "Virginia": "VA", "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}


# ───────────────────────── HELPERS ─────────────────────────
def show(obj, kind="chart", **kw):
    fn = st.plotly_chart if kind == "chart" else st.dataframe
    try:
        fn(obj, width="stretch", **kw)
    except TypeError:
        fn(obj, use_container_width=True, **kw)


def sty(fig, h=430, title=None):
    fig.update_layout(
        height=h, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", colorway=PAL,
        title=dict(text=title, x=0.01, font=dict(size=15)) if title else None,
        font=dict(family="Manrope, sans-serif", color=P["tx"], size=12),
        margin=dict(l=10, r=10, t=52 if title else 12, b=10),
        legend=dict(orientation="h", y=1.1, x=1, xanchor="right", title=None),
        hoverlabel=dict(bgcolor=P["card"], font_color=P["tx"]))
    fig.update_xaxes(gridcolor=P["grid"], zeroline=False, title=None)
    fig.update_yaxes(gridcolor=P["grid"], zeroline=False, title=None)
    return fig


def card(label, value, sub, color):
    return f'<div class="kpi" style="--c:{color}"><div class="l">{label}</div><div class="v">{value}</div><div class="s">{sub}</div></div>'


def sec(t):
    st.markdown(f'<div class="sec">{t}</div>', unsafe_allow_html=True)


def money(x):
    a = abs(x)
    return f"${x/1e6:,.2f}M" if a >= 1e6 else f"${x/1e3:,.1f}K" if a >= 1e4 else f"${x:,.0f}"


@st.cache_data(show_spinner="Loading data…")
def load():
    f = Path(__file__).parent / "Superstore.csv"
    d = pd.read_csv(f, encoding="latin-1")
    d.columns = [c.strip() for c in d.columns]
    for c in ["Order Date", "Ship Date"]:
        d[c] = pd.to_datetime(d[c], format="mixed", errors="coerce")
    d = d.dropna(subset=["Order Date", "Ship Date", "Sales", "Profit"]).copy()
    for c in ["Sales", "Profit", "Quantity", "Discount"]:
        d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0)
    d["Year"] = d["Order Date"].dt.year
    d["Quarter"] = "Q" + d["Order Date"].dt.quarter.astype(str)
    d["Month"] = d["Order Date"].dt.to_period("M").astype(str)
    d["Weekday"] = d["Order Date"].dt.day_name()
    d["Month Name"] = d["Order Date"].dt.strftime("%b")
    d["Ship Lag"] = (d["Ship Date"] - d["Order Date"]).dt.days.clip(lower=0)
    d["Margin %"] = np.where(d["Sales"] > 0, d["Profit"] / d["Sales"] * 100, 0)
    d["Discount Bucket"] = pd.cut(d["Discount"], [-.01, 0, .1, .2, .3, .4, .5, .8],
                                  labels=["0%", "1-10%", "11-20%", "21-30%", "31-40%", "41-50%", ">50%"])
    d["Status"] = np.where(d["Profit"] > 0, "Profitable", np.where(d["Profit"] < 0, "Loss", "Break-even"))
    d["Code"] = d["State"].map(US)
    return d


df = load()

# ───────────────────────── HEADER + FILTERS ─────────────────────────
dmin, dmax = df["Order Date"].min().date(), df["Order Date"].max().date()
FK = ["f_reg", "f_cat", "f_seg", "f_ship"]


def reset():
    for k in FK:
        st.session_state[k] = []
    st.session_state["f_date"] = (dmin, dmax)


h1, h2, h3 = st.columns([6, 1.2, 1])
with h1:
    st.markdown('<div class="topbar"><div class="logo">📊</div><div><div class="ttl">Superstore Business Intelligence</div>'
                '<div class="sub">Sales, profit, regions, products and shipping in one view</div></div></div>',
                unsafe_allow_html=True)
with h2:
    st.write("")
    st.toggle("🌙 Dark mode", value=True, key="dark")
with h3:
    st.write("")
    st.button("↺ Reset filters", on_click=reset, key="rst")

f1, f2, f3, f4, f5 = st.columns([2, 1.4, 1.4, 1.4, 1.4])
with f1:
    dr = st.date_input("📅 Order date range", value=(dmin, dmax), min_value=dmin, max_value=dmax, key="f_date")
with f2:
    reg = st.multiselect("🌍 Region", sorted(df["Region"].unique()), key="f_reg", placeholder="All regions")
with f3:
    cat = st.multiselect("🛍️ Category", sorted(df["Category"].unique()), key="f_cat", placeholder="All categories")
with f4:
    seg = st.multiselect("👥 Segment", sorted(df["Segment"].unique()), key="f_seg", placeholder="All segments")
with f5:
    shp = st.multiselect("🚚 Ship mode", sorted(df["Ship Mode"].unique()), key="f_ship", placeholder="All modes")

f = df
if isinstance(dr, (tuple, list)) and len(dr) == 2:
    f = f[(f["Order Date"].dt.date >= dr[0]) & (f["Order Date"].dt.date <= dr[1])]
for col, val in [("Region", reg), ("Category", cat), ("Segment", seg), ("Ship Mode", shp)]:
    if val:
        f = f[f[col].isin(val)]

if f.empty:
    st.warning("No records match these filters. Widen the date range or click Reset filters.")
    st.stop()

sales, profit = f["Sales"].sum(), f["Profit"].sum()
orders = f["Order ID"].nunique()
K = dict(sales=sales, profit=profit, margin=profit / sales * 100 if sales else 0, orders=orders,
         cust=f["Customer ID"].nunique(), aov=sales / orders, qty=int(f["Quantity"].sum()),
         disc=f["Discount"].mean() * 100, lag=f["Ship Lag"].mean(),
         loss=f[f["Status"] == "Loss"]["Order ID"].nunique())

tabs = st.tabs(["🏠 Overview", "💰 Sales", "📈 Profit", "🗺️ Regions", "🛍️ Products & Customers",
                "🚚 Shipping", "🔍 Data Explorer", "📘 Guide & About"])

# ───────────────────────── OVERVIEW ─────────────────────────
with tabs[0]:
    cols = st.columns(6)
    items = [("Total sales", money(K["sales"]), f"{K['qty']:,} units sold", P["ac"]),
             ("Total profit", money(K["profit"]), f"Margin {K['margin']:.1f}%", P["good"]),
             ("Orders", f"{K['orders']:,}", f"AOV ${K['aov']:,.0f}", "#a78bfa"),
             ("Customers", f"{K['cust']:,}", f"{K['orders']/K['cust']:.1f} orders each", "#f472b6"),
             ("Avg discount", f"{K['disc']:.1f}%", f"Ship lag {K['lag']:.1f} days", P["ac2"]),
             ("Loss orders", f"{K['loss']:,}", f"{K['loss']/K['orders']*100:.1f}% of orders", P["bad"])]
    for c, it in zip(cols, items):
        c.markdown(card(*it), unsafe_allow_html=True)
    st.write("")

    m = f.groupby("Month", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    fig = go.Figure()
    fig.add_scatter(x=m["Month"], y=m["Sales"], name="Sales", fill="tozeroy", line=dict(color=PAL[0], width=2.5),
                    fillcolor="rgba(34,211,238,.12)" if DARK else "rgba(14,116,144,.10)")
    fig.add_scatter(x=m["Month"], y=m["Profit"], name="Profit", line=dict(color=PAL[1], width=2.5))
    show(sty(fig, 400, "Monthly sales and profit"))

    a, b, c = st.columns(3)
    cs = f.groupby("Category", as_index=False)["Sales"].sum()
    with a:
        show(sty(px.pie(cs, names="Category", values="Sales", hole=.6), 380, "Sales by category"))
    sg = f.groupby("Segment", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    with b:
        show(sty(px.bar(sg, x="Segment", y=["Sales", "Profit"], barmode="group"), 380, "Segments: sales vs profit"))
    wd = f.groupby("Weekday", as_index=False)["Order ID"].nunique().rename(columns={"Order ID": "Orders"})
    wd["Weekday"] = pd.Categorical(wd["Weekday"], ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], True)
    with c:
        show(sty(px.bar(wd.sort_values("Weekday"), x="Weekday", y="Orders"), 380, "Orders by weekday"))

    sec("💡 Auto insights")
    cs2 = f.groupby("Category")["Sales"].sum()
    sub = f.groupby("Sub-Category")["Profit"].sum()
    rg = f.groupby("Region")["Profit"].sum()
    mo = f.groupby("Month Name")["Sales"].sum()
    corr = f[["Discount", "Profit"]].corr().iloc[0, 1]
    tips = [f"🏆 **{cs2.idxmax()}** leads with **{money(cs2.max())}** ({cs2.max()/cs2.sum()*100:.0f}% of sales).",
            f"🌍 **{rg.idxmax()}** is the most profitable region at **{money(rg.max())}**.",
            f"📅 Sales peak in **{mo.idxmax()}**.",
            (f"🚨 **{sub.idxmin()}** loses **{money(abs(sub.min()))}**. Review pricing." if sub.min() < 0 else "✅ Every sub-category is profitable."),
            (f"📉 Discount and profit are negatively correlated ({corr:.2f}). Deep discounts hurt." if corr < -.2 else f"ℹ️ Discount vs profit correlation is {corr:.2f}.")]
    ic = st.columns(len(tips))
    for c, t in zip(ic, tips):
        c.markdown(f'<div class="ins">{t}</div>', unsafe_allow_html=True)

# ───────────────────────── SALES ─────────────────────────
with tabs[1]:
    a, b = st.columns(2)
    y = f.groupby("Year", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    y["Growth %"] = y["Sales"].pct_change() * 100
    with a:
        fig = px.bar(y, x="Year", y="Sales", text=y["Growth %"].map(lambda v: "" if pd.isna(v) else f"{v:+.1f}%"))
        fig.update_xaxes(type="category")
        show(sty(fig, 440, "Yearly sales (label = YoY growth)"))
    with b:
        q = f.groupby(["Year", "Quarter"], as_index=False)["Sales"].sum().pivot(index="Quarter", columns="Year", values="Sales")
        show(sty(px.imshow(q, aspect="auto", color_continuous_scale="Teal", text_auto=".2s"), 440, "Quarter x year heatmap"))
    sc = f.groupby(["Category", "Sub-Category"], as_index=False).agg(Sales=("Sales", "sum"), Qty=("Quantity", "sum")).sort_values("Sales")
    a, b = st.columns(2)
    with a:
        show(sty(px.bar(sc, x="Sales", y="Sub-Category", color="Category", orientation="h"), 560, "Sales by sub-category"))
    with b:
        tp = f.groupby("Product Name", as_index=False)["Sales"].sum().nlargest(12, "Sales").sort_values("Sales")
        tp["Product Name"] = tp["Product Name"].str.slice(0, 38)
        show(sty(px.bar(tp, x="Sales", y="Product Name", orientation="h", text_auto=".2s"), 560, "Top 12 products by sales"))

# ───────────────────────── PROFIT ─────────────────────────
with tabs[2]:
    cols = st.columns(4)
    for c, it in zip(cols, [("Profit", money(K["profit"]), "Net", P["good"]), ("Margin", f"{K['margin']:.1f}%", "Profit / sales", P["ac"]),
                            ("Loss orders", f"{K['loss']:,}", "Need attention", P["bad"]), ("Avg discount", f"{K['disc']:.1f}%", "Across lines", P["ac2"])]):
        c.markdown(card(*it), unsafe_allow_html=True)
    st.write("")
    a, b = st.columns(2)
    d = f.groupby("Discount Bucket", observed=False).agg(Avg=("Profit", "mean"), Sales=("Sales", "sum")).reset_index()
    with a:
        fig = px.bar(d, x="Discount Bucket", y="Avg", color="Avg", color_continuous_scale=[P["bad"], P["ac2"], P["good"]], text_auto=".1f")
        fig.update_coloraxes(showscale=False)
        show(sty(fig, 440, "Average profit per line by discount level"))
    sp = f.groupby("Sub-Category", as_index=False)["Profit"].sum().sort_values("Profit")
    with b:
        fig = px.bar(sp, x="Profit", y="Sub-Category", orientation="h", color=sp["Profit"] > 0,
                     color_discrete_map={True: P["good"], False: P["bad"]})
        fig.update_layout(showlegend=False)
        show(sty(fig, 440, "Profit by sub-category"))
    smp = f.sample(min(len(f), 3000), random_state=1)
    fig = px.scatter(smp, x="Sales", y="Profit", color="Category", size="Quantity", hover_name="Product Name", opacity=.65)
    fig.add_hline(y=0, line_dash="dash", line_color=P["mu"])
    show(sty(fig, 460, "Sales vs profit (sample of 3,000 lines)"))
    sec("🚨 Biggest loss-making products")
    pl = f[f["Profit"] < 0].groupby("Product Name", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Lines=("Order ID", "count")).nsmallest(10, "Profit")
    show(pl, "df", hide_index=True)

# ───────────────────────── REGIONS ─────────────────────────
with tabs[3]:
    st_ = f.groupby(["State", "Code"], as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    mt = st.radio("Map metric", ["Sales", "Profit"], horizontal=True, key="mapm")
    fig = px.choropleth(st_, locations="Code", locationmode="USA-states", color=mt, scope="usa", hover_name="State",
                        color_continuous_scale="Teal" if mt == "Sales" else "RdYlGn")
    fig.update_geos(bgcolor="rgba(0,0,0,0)", lakecolor="rgba(0,0,0,0)")
    show(sty(fig, 560, f"{mt} by US state"))
    a, b = st.columns(2)
    rr = f.groupby("Region", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    with a:
        show(sty(px.bar(rr, x="Region", y=["Sales", "Profit"], barmode="group"), 460, "Region performance"))
    with b:
        t15 = st_.nlargest(15, "Sales").sort_values("Sales")
        show(sty(px.bar(t15, x="Sales", y="State", orientation="h", color="Profit", color_continuous_scale="RdYlGn"), 460, "Top 15 states (colour = profit)"))
    show(sty(px.treemap(f, path=["Region", "State", "City"], values="Sales", color="Profit", color_continuous_scale="RdYlGn", color_continuous_midpoint=0), 520, "Region > state > city"))

# ───────────────────────── PRODUCTS & CUSTOMERS ─────────────────────────
with tabs[4]:
    show(sty(px.treemap(f, path=["Category", "Sub-Category"], values="Sales", color="Profit", color_continuous_scale="RdYlGn", color_continuous_midpoint=0), 500, "Category > sub-category (size = sales, colour = profit)"))
    by = st.radio("Rank products by", ["Sales", "Profit", "Quantity"], horizontal=True, key="rankby")
    n = st.slider("How many", 5, 25, 12, key="topn")
    a, b = st.columns(2)
    tp = f.groupby("Product Name", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Quantity=("Quantity", "sum")).nlargest(n, by).sort_values(by)
    tp["Product Name"] = tp["Product Name"].str.slice(0, 40)
    with a:
        show(sty(px.bar(tp, x=by, y="Product Name", orientation="h", text_auto=".2s"), 560, f"Top {n} products by {by.lower()}"))
    tc = f.groupby("Customer Name", as_index=False).agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "nunique")).nlargest(n, "Sales").sort_values("Sales")
    with b:
        show(sty(px.bar(tc, x="Sales", y="Customer Name", orientation="h", color="Profit", color_continuous_scale="RdYlGn", text_auto=".2s"), 560, f"Top {n} customers"))

# ───────────────────────── SHIPPING ─────────────────────────
with tabs[5]:
    sm = f.groupby("Ship Mode", as_index=False).agg(Lag=("Ship Lag", "mean"), Orders=("Order ID", "nunique"), Sales=("Sales", "sum"))
    cols = st.columns(3)
    for c, it in zip(cols, [("Avg ship lag", f"{K['lag']:.1f} days", "Order to ship", P["ac"]),
                            ("Fastest mode", sm.loc[sm["Lag"].idxmin(), "Ship Mode"], f"{sm['Lag'].min():.1f} days", P["good"]),
                            ("Most used", sm.loc[sm["Orders"].idxmax(), "Ship Mode"], f"{sm['Orders'].max():,} orders", P["ac2"])]):
        c.markdown(card(*it), unsafe_allow_html=True)
    st.write("")
    a, b, c = st.columns(3)
    with a:
        show(sty(px.bar(sm, x="Ship Mode", y="Lag", text_auto=".1f"), 420, "Average lag (days)"))
    with b:
        show(sty(px.pie(sm, names="Ship Mode", values="Orders", hole=.55), 420, "Order share"))
    with c:
        show(sty(px.histogram(f, x="Ship Lag", color="Ship Mode", nbins=8, barmode="stack"), 420, "Lag distribution"))
    ml = f.groupby(["Month", "Ship Mode"], as_index=False)["Ship Lag"].mean()
    show(sty(px.line(ml, x="Month", y="Ship Lag", color="Ship Mode"), 420, "Ship lag trend by mode"))

# ───────────────────────── EXPLORER ─────────────────────────
with tabs[6]:
    q = st.text_input("🔎 Search customer, product or city", key="srch")
    v = f
    if q:
        mk = f["Customer Name"].str.contains(q, case=False) | f["Product Name"].str.contains(q, case=False) | f["City"].str.contains(q, case=False)
        v = f[mk]
    allc = ["Order Date", "Order ID", "Customer Name", "Segment", "Region", "State", "Category", "Sub-Category",
            "Product Name", "Ship Mode", "Sales", "Quantity", "Discount", "Profit", "Margin %", "Status"]
    cc = st.multiselect("Columns", allc, default=["Order Date", "Customer Name", "Category", "Product Name", "Sales", "Profit"], key="cols")
    a, b = st.columns([2, 1])
    sc_ = a.selectbox("Sort by", cc or allc, key="sortc")
    asc = b.radio("Order", ["Descending", "Ascending"], horizontal=True, key="sorto") == "Ascending"
    st.caption(f"{len(v):,} rows | Sales {money(v['Sales'].sum())} | Profit {money(v['Profit'].sum())}")
    show(v[cc or allc].sort_values(sc_, ascending=asc), "df", height=520, hide_index=True)
    st.download_button("⬇️ Download filtered CSV", v.to_csv(index=False).encode(), "superstore_filtered.csv", "text/csv")

# ───────────────────────── GUIDE & ABOUT ─────────────────────────
with tabs[7]:
    a, b = st.columns(2)
    with a:
        st.markdown("""<div class="box"><b style="font-size:1.1rem">📘 How to use</b><br>
1. <b>Filters sit at the top.</b> Date range, region, category, segment and ship mode apply to every tab at once.<br>
2. <b>Leave a filter empty</b> to include everything. Click <b>Reset filters</b> to start over.<br>
3. <b>Switch theme</b> with the Dark mode toggle at the top right.<br>
4. <b>Hover</b> a chart for exact values. Click legend items to hide or show a series. Use the toolbar to zoom, pan or download a PNG.<br>
5. <b>Start at Overview</b>, then move to Sales, Profit, Regions, Products and Shipping to dig deeper.<br>
6. <b>Data Explorer</b> lets you search, pick columns, sort and download the filtered rows as CSV.</div>""", unsafe_allow_html=True)
        st.markdown("""<div class="box" style="margin-top:12px"><b style="font-size:1.1rem">🧭 Tab guide</b><br>
<b>Overview</b> headline KPIs, trend, mix and insights.<br><b>Sales</b> yearly growth, quarters, sub-categories, top products.<br>
<b>Profit</b> discount impact, profit by sub-category, loss makers.<br><b>Regions</b> US map, states, cities.<br>
<b>Products & Customers</b> hierarchy and rankings.<br><b>Shipping</b> lag by mode and trend.</div>""", unsafe_allow_html=True)
    with b:
        st.markdown(f"""<div class="box"><b style="font-size:1.1rem">ℹ️ About</b><br>
Interactive business dashboard built on the Superstore sales dataset (<b>{len(df):,}</b> order lines, {dmin:%b %Y} to {dmax:%b %Y}).<br><br>
<b>Metric definitions</b><br>
• Margin = total profit / total sales<br>• AOV = total sales / unique orders<br>• Loss order = an order with at least one loss-making line<br>
• Ship lag = ship date minus order date, in days<br><br>
<b>Stack</b>: Python, Streamlit, Pandas, Plotly.<br><b>Data file</b>: Superstore.csv (same folder as dashboard.py).<br>
<b>Run</b>: <code>streamlit run dashboard.py</code></div>""", unsafe_allow_html=True)
