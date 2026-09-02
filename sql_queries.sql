-- 1. Total Revenue and Profit by Region
SELECT Region, SUM(Net_Revenue) AS Total_Net_Revenue, SUM(Profit) AS Total_Profit
FROM superstore GROUP BY Region ORDER BY Total_Net_Revenue DESC;

-- 2. Top Performing Product Categories
SELECT Category, SUM(Sales) AS Total_Sales, AVG(Profit_Margin) AS Avg_Margin
FROM superstore GROUP BY Category ORDER BY Total_Sales DESC;
