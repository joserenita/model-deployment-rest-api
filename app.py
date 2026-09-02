import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="End-to-End Superstore Sales & Customer Insights Capstone", layout="wide")

st.title("📈 End-to-End Superstore Sales & Customer Insights Capstone")
st.markdown("### Executive Overview & Key Performance Indicators")

@st.cache_data
def load_data():
    df = pd.read_csv("data/cleaned_superstore.csv")
    df['Order_Date'] = pd.to_datetime(df['Order_Date'])
    return df

try:
    df = load_data()

    # Sidebar Filters
    st.sidebar.header("Filter Data")
    region_filter = st.sidebar.multiselect("Select Region", options=df['Region'].unique(), default=df['Region'].unique())
    category_filter = st.sidebar.multiselect("Select Category", options=df['Category'].unique(), default=df['Category'].unique())

    filtered_df = df[(df['Region'].isin(region_filter)) & (df['Category'].isin(category_filter))]

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
    else:
        # 8 Core KPIs Display
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Gross Revenue", f"${filtered_df['Sales'].sum():,.2f}")
        col2.metric("Net Revenue", f"${filtered_df['Net_Revenue'].sum():,.2f}")
        col3.metric("Total Profit", f"${filtered_df['Profit'].sum():,.2f}")
        col4.metric("Avg Profit Margin", f"{filtered_df['Profit_Margin'].mean():.2f}%")

        col5, col6, col7, col8 = st.columns(4)
        col5.metric("Total Orders", f"{filtered_df['Order_ID'].nunique():,}")
        col6.metric("Units Sold", f"{filtered_df['Quantity'].sum():,}")
        col7.metric("Avg CSAT Score", f"{filtered_df['Customer_Satisfaction_Score'].mean():.2f} / 5.0")
        col8.metric("Return Rate", f"{(filtered_df['Return_Status'].value_counts(normalize=True).get('Yes', 0) * 100):.2f}%")

        st.markdown("---")

        # Visualizations
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("Net Revenue by Category")
            fig_cat = px.bar(filtered_df, x='Category', y='Net_Revenue', color='Category', title="Net Revenue by Product Category")
            st.plotly_chart(fig_cat, use_container_width=True)

        with col_right:
            st.subheader("Profitability vs Discount")
            fig_disc = px.scatter(filtered_df, x='Discount', y='Profit_Margin', color='Category', hover_data=['Order_ID'], title="Discount Impact on Profit Margin")
            st.plotly_chart(fig_disc, use_container_width=True)

except FileNotFoundError:
    st.error("Data file not found! Please run `python3 generate_data.py` first.")
