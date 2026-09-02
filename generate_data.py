import os, pandas as pd, numpy as np
os.makedirs("data", exist_ok=True)
np.random.seed(42)
n_rows = 500
dates = pd.date_range(start="2025-01-01", periods=180, freq="D")
raw_data = {
    "Order_ID": [f"ORD-{1000+i}" for i in range(n_rows)],
    "Order_Date": np.random.choice(dates, n_rows),
    "Customer_ID": [f"CUST-{np.random.randint(100, 150)}" for _ in range(n_rows)],
    "Customer_Segment": np.random.choice(['Consumer', 'Corporate', 'Home Office'], n_rows),
    "Region": np.random.choice(['East', 'West', 'Central', 'South'], n_rows),
    "Category": np.random.choice(['Technology', 'Office Supplies', 'Furniture'], n_rows),
    "Sales": np.random.uniform(10.0, 1200.0, n_rows),
    "Quantity": np.random.randint(1, 15, n_rows),
    "Discount": np.random.choice([0.0, 0.1, 0.2, 0.3, 0.5], n_rows),
    "Profit": np.random.uniform(-100.0, 350.0, n_rows),
    "Customer_Satisfaction_Score": np.random.choice([1, 2, 3, 4, 5, np.nan], n_rows, p=[0.05, 0.1, 0.25, 0.35, 0.2, 0.05]),
    "Return_Status": np.random.choice(['Yes', 'No', None], n_rows, p=[0.12, 0.83, 0.05])
}
df_raw = pd.DataFrame(raw_data)
df_raw.to_csv("data/raw_superstore.csv", index=False)
df_clean = df_raw.copy()
df_clean['Sales'] = df_clean['Sales'].fillna(df_clean['Sales'].median())
df_clean['Profit'] = df_clean['Profit'].fillna(df_clean['Profit'].median())
df_clean['Customer_Satisfaction_Score'] = df_clean['Customer_Satisfaction_Score'].fillna(df_clean['Customer_Satisfaction_Score'].mode()[0])
df_clean['Return_Status'] = df_clean['Return_Status'].fillna('No')
df_clean['Order_Date'] = pd.to_datetime(df_clean['Order_Date'])
df_clean['Net_Revenue'] = df_clean['Sales'] * (1 - df_clean['Discount'])
df_clean['Profit_Margin'] = (df_clean['Profit'] / df_clean['Sales']) * 100
df_clean['Is_Profitable'] = df_clean['Profit'].apply(lambda x: 1 if x > 0 else 0)
df_clean.to_csv("data/cleaned_superstore.csv", index=False)
print("Data generated successfully.")
