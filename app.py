import pandas as pd
import streamlit as st

st.set_page_config(page_title="Sales Dashboard", layout="wide")


@st.cache_data
def load_data():
    return pd.read_csv("data/superstore_dashboard.csv", parse_dates=["order_date"])


df = load_data()

st.title("Sales Analytics Dashboard")

# ---------- Sidebar filters ----------
st.sidebar.header("Filters")

min_date = df["order_date"].min().date()
max_date = df["order_date"].max().date()
start, end = st.sidebar.slider(
    "Order date range",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD",
)

all_markets = sorted(df["market"].unique())
markets = st.sidebar.multiselect("Market", options=all_markets, default=all_markets)

all_categories = sorted(df["category"].unique())
categories = st.sidebar.multiselect("Category", options=all_categories, default=all_categories)

max_discount = st.sidebar.slider("Maximum discount (%)", min_value=0, max_value=85, value=85, step=5)

# ---------- Apply the filters ----------
mask = (
    df["order_date"].between(pd.Timestamp(start), pd.Timestamp(end))
    & df["market"].isin(markets)
    & df["category"].isin(categories)
    & (df["discount"] <= max_discount / 100 + 1e-9)
)
filtered = df[mask]

st.caption(f"Showing {len(filtered):,} of {len(df):,} order lines")

if filtered.empty:
    st.warning("No matching records. Try widening the date range or selecting more markets or categories.")
    st.stop()

# ---------- KPI cards ----------
total_sales = filtered["sales"].sum()
total_profit = filtered["profit"].sum()
margin = total_profit / total_sales * 100
orders = filtered["order_id"].nunique()
aov = total_sales / orders

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total sales", f"{total_sales:,.0f}")
c2.metric("Total profit", f"{total_profit:,.0f}")
c3.metric("Profit margin", f"{margin:.1f}%")
c4.metric("Orders", f"{orders:,}")
c5.metric("Average order value", f"{aov:,.2f}")


import plotly.express as px

# ---------- Charts ----------
left, right = st.columns(2)

# 1) Bar chart: profit by sub-category
by_sub = (filtered.groupby("sub_category", as_index=False)
                  .agg(sales=("sales", "sum"), profit=("profit", "sum"))
                  .sort_values("profit"))
by_sub["result"] = by_sub["profit"].apply(lambda p: "Profit" if p >= 0 else "Loss")
fig_bar = px.bar(by_sub, x="profit", y="sub_category", orientation="h",
                 color="result",
                 color_discrete_map={"Profit": "#1f6feb", "Loss": "#d9534f"},
                 title="Profit by sub-category",
                 labels={"profit": "Profit", "sub_category": ""})
fig_bar.update_layout(showlegend=False)
left.plotly_chart(fig_bar)

# 2) Line chart: monthly sales
monthly = (filtered.set_index("order_date")["sales"]
                   .resample("MS").sum().reset_index())
fig_line = px.line(monthly, x="order_date", y="sales", markers=True,
                   title="Monthly sales",
                   labels={"order_date": "Month", "sales": "Sales"})
right.plotly_chart(fig_line)


import numpy as np
# 3) Scatter plot: discount vs profit
sample = filtered.sample(min(len(filtered), 5000), random_state=42).copy()
rng = np.random.default_rng(42)
sample["discount_jitter"] = sample["discount"] + rng.uniform(-0.012, 0.012, len(sample))
fig_scatter = px.scatter(
    sample, x="discount_jitter", y="profit", color="category", opacity=0.45,
    hover_data={"discount": ":.0%", "sales": ":,.0f", "discount_jitter": False},
    title="Discount vs profit (random sample of up to 5,000 order lines; points slightly jittered)",
    labels={"discount_jitter": "Discount", "profit": "Profit"},
)
fig_scatter.add_hline(y=0, line_dash="dash", line_color="grey")
low, high = filtered["profit"].quantile([0.01, 0.99])
if high > low:
    fig_scatter.update_yaxes(range=[low * 1.2, high * 1.2])
fig_scatter.update_xaxes(tickformat=".0%")
st.plotly_chart(fig_scatter)
st.caption("The profit axis is zoomed to the middle 98% of order lines, so about 2% of extreme values are not shown.")