# Ecommerce-Returns-Analytics

This project utilizes Pandas to perform a comprehensive return rate analysis on e-commerce order and return data. It merges transactional datasets to calculate key performance indicators (KPIs) like the Overall Return Rate and segmented rates by Category, Supplier, and Marketing Channel.

The core output is a Rule-Based Return Risk Score for every product, derived from a weighted average of its individual return rate (70%) and its respective category's average return rate (30%). This scoring mechanism identifies the top 30% of high-risk products, which are then saved for targeted business intervention and integration into a Power BI dashboard for visualization.

Key Features:

1. Data Cleaning & Feature Engineering: Creation of an is_returned flag and standardization of price/quantity data.
2. KPI Calculation: Detailed return rates by various business dimensions.
3. Risk Scoring: Implementation of a weighted risk model to prioritize product risk.
4. Output: high_risk_products.csv file for downstream analysis and mitigation strategies.
