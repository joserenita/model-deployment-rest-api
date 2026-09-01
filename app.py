import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set Streamlit Page Config
st.set_page_config(
    page_title="Superstore Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Superstore Sales & Analytics Dashboard")
st.markdown("Explore key business metrics, sales distributions, and performance insights.")

# --- USE CACHING FOR EXPENSIVE DATA LOADING ---
@st.cache_data
def load_data():
    np.random.seed(42)
    categories = ['Furniture', 'Office Supplies', 'Technology']
    regions = ['East', 'West', 'Central', 'South']
    
    dates = pd.date_range(start="2025-01-01", periods=200, freq="D")
    data = []
    for _ in range(300):
        data.append({
            "Order Date": np.random.choice(dates),
            "Category": np.random.choice(categories),
            "Region": np.random.choice(regions),
            "Sales": round(np.random.uniform(20.0, 500.0), 2),
            "Profit": round(np.random.uniform(-50.0, 150.0), 2),
            "Quantity": np.random.randint(1, 10)
        })
    return pd.DataFrame(data)

df = load_data()

# --- INTERACTIVE FILTERS (SIDEBAR) ---
st.sidebar.header("Filter Options")

region_filter = st.sidebar.multiselect(
    "Select Region:",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

category_filter = st.sidebar.multiselect(
    "Select Category:",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

# Apply Filters
filtered_df = df[(df["Region"].isin(region_filter)) & (df["Category"].isin(category_filter))]

# --- HANDLE EMPTY FILTER RESULTS GRACEFULLY ---
if filtered_df.empty:
    st.warning("⚠️ No data available for the selected filters. Please adjust your criteria on the sidebar.")
    st.stop()

# --- KPI SECTION ---
st.markdown("### 📈 Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)
avg_order_value = filtered_df["Sales"].mean()

col1.metric("Total Revenue", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Total Orders", f"{total_orders}")
col4.metric("Avg Order Value", f"${avg_order_value:,.2f}")

st.divider()

# --- DYNAMIC VISUALIZATIONS ---
st.markdown("### 📊 Business Analytics & Visualizations")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    sales_time = filtered_df.groupby("Order Date")["Sales"].sum().reset_index()
    fig_time = px.line(sales_time, x="Order Date", y="Sales", title="Sales Trend Over Time", template="plotly_white")
    st.plotly_chart(fig_time, use_container_width=True)

with chart_col2:
    sales_cat = filtered_df.groupby("Category")["Sales"].sum().reset_index()
    fig_cat = px.bar(sales_cat, x="Category", y="Sales", color="Category", title="Total Sales by Category", template="plotly_white")
    st.plotly_chart(fig_cat, use_container_width=True)

fig_scatter = px.scatter(
    filtered_df, x="Sales", y="Profit", color="Category", hover_data=["Region"],
    title="Sales vs. Profit Margin Distribution", template="plotly_white"
)
st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()

# --- PREDICTION FORM / ANALYTICAL SUMMARY ---
st.markdown("### 🔮 Quick Profit Predictor")
st.write("Estimate anticipated profit based on sale conditions:")

pred_col1, pred_col2 = st.columns(2)
with pred_col1:
    input_sales = st.number_input("Enter Sales Amount ($)", min_value=1.0, value=100.0)
with pred_col2:
    input_qty = st.number_input("Enter Item Quantity", min_value=1, value=2)

estimated_profit = input_sales * 0.22 - (input_qty * 1.5)
st.success(f"**Estimated Projected Profit:** ${estimated_profit:.2f}")
