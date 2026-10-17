import streamlit as st
from pathlib import Path
from src.data_loader import load_raw_data
from src.preprocessing import clean_and_enrich, apply_filters
from src.analytics import kpis, discount_impact, profit_leakage
from src.visualizations import bar_chart, scatter_sales_profit, dual_bar

st.set_page_config(page_title="Profit Intelligence", page_icon="📈", layout="wide")
css = Path(__file__).parent.parent / "assets" / "style.css"
if css.exists():
    st.markdown(f"<style>{css.read_text()}</style>", unsafe_allow_html=True)


@st.cache_data
def _load():
    return clean_and_enrich(load_raw_data())


df = _load()
st.sidebar.header("🔎 Filters")
years = st.sidebar.multiselect("Year", sorted(df["Order Year"].unique()))
regions = st.sidebar.multiselect("Region", sorted(df["Region"].unique()))
filtered = apply_filters(df, years=years, regions=regions)

st.title("📈 Profit Intelligence")
k = kpis(filtered)
c1, c2, c3, c4 = st.columns(4)
c1.metric("💵 Profit", f"${k['total_profit']:,.0f}")
c2.metric("📊 Margin", f"{k['avg_profit_margin']:.1f}%")
c3.metric("⚠️ Loss Orders", f"{k['loss_making_orders']:,}")
c4.metric("💸 Discount", f"{k['avg_discount']:.1f}%")

st.divider()
di = discount_impact(filtered)
st.plotly_chart(dual_bar(di, "Discount Bucket", "AvgProfit", "TotalSales",
                "💸 Discount vs Profit"), use_container_width=True)
st.info("Discounts above **30%** erode margins.")

st.divider()
st.plotly_chart(scatter_sales_profit(filtered, "🔍 Sales vs Profit"),
                use_container_width=True)

st.divider()
st.subheader("🚨 Top Profit Leakage")
pl = profit_leakage(filtered, 10)
if pl.empty:
    st.success("✅ No loss-making products.")
else:
    st.plotly_chart(bar_chart(pl, "Profit", "Product Name",
                    title="Worst Products", horizontal=True,
                    color_seq=["#D62828"]), use_container_width=True)
    st.dataframe(pl, use_container_width=True)
