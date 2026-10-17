"""Auto-generated business insights."""


def generate_insights(df):
    insights = []
    if df.empty:
        return [{"icon": "⚠️", "type": "info", "text": "No data in current filter."}]

    cat = df.groupby("Category")["Sales"].sum()
    insights.append({"icon": "🏆", "type": "success",
        "text": f"**{cat.idxmax()}** leads sales at **${cat.max():,.0f}**."})

    sub = df.groupby("Sub-Category")["Profit"].sum()
    if (sub < 0).any():
        insights.append({"icon": "🚨", "type": "danger",
            "text": f"**{sub.idxmin()}** losing **${abs(sub.min()):,.0f}**."})

    corr = df[["Discount", "Profit"]].corr().iloc[0, 1]
    if corr < -0.2:
        insights.append({"icon": "📉", "type": "warning",
            "text": f"Discounts hurting profit (corr **{corr:.2f}**)."})

    reg = df.groupby("Region")["Profit"].sum()
    insights.append({"icon": "🌍", "type": "info",
        "text": f"**{reg.idxmax()}** region highest profit."})

    ship = df.groupby("Ship Mode")["Ship Lag Days"].mean().sort_values()
    insights.append({"icon": "🚚", "type": "info",
        "text": f"**{ship.index[0]}** fastest ship mode."})

    month = df.groupby("Order Month Name")["Sales"].sum()
    insights.append({"icon": "📅", "type": "success",
        "text": f"Sales peak in **{month.idxmax()}**."})

    loss_pct = (df["Profit"] < 0).mean() * 100
    if loss_pct > 15:
        insights.append({"icon": "⚠️", "type": "warning",
            "text": f"**{loss_pct:.1f}%** items loss-making."})

    seg = df.groupby("Segment")["Sales"].sum()
    insights.append({"icon": "👥", "type": "info",
        "text": f"**{seg.idxmax()}** = **{(seg.max()/seg.sum()*100):.1f}%** of sales."})

    return insights
