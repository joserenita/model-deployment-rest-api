import sqlite3, pandas as pd
df = pd.read_csv("data/cleaned_superstore.csv")
conn = sqlite3.connect(":memory:")
df.to_sql("superstore", conn, index=False, if_exists="replace")
sql_script = """-- 1. Total Revenue and Profit by Region
SELECT Region, SUM(Net_Revenue) AS Total_Net_Revenue, SUM(Profit) AS Total_Profit
FROM superstore GROUP BY Region ORDER BY Total_Net_Revenue DESC;

-- 2. Top Performing Product Categories
SELECT Category, SUM(Sales) AS Total_Sales, AVG(Profit_Margin) AS Avg_Margin
FROM superstore GROUP BY Category ORDER BY Total_Sales DESC;
"""
with open("sql_queries.sql", "w") as f:
    f.write(sql_script)
print("SQL analysis script executed successfully.")
