import pandas as pd
import os

# -----------------------------------------------------
# File paths (change these if needed)
# -----------------------------------------------------
ORDERS_FILE = "orders.csv"
RETURNS_FILE = "returns.csv"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("📦 Loading datasets...")

# -----------------------------------------------------
# Step 1: Load datasets
# -----------------------------------------------------
orders = pd.read_csv(r"C:\Users\jivit\OneDrive\Documents\Matplotib & Seaborn\zInternship\Order.csv")
returns = pd.read_csv(r"C:\Users\jivit\OneDrive\Documents\Matplotib & Seaborn\zInternship\Return.csv")

# -----------------------------------------------------
# Step 2: Merge orders and returns
# -----------------------------------------------------
data = pd.merge(orders, returns, on="order_id", how="left")

# -----------------------------------------------------
# Step 3: Create 'is_returned' flag
# -----------------------------------------------------
data["is_returned"] = data["return_date"].notnull().astype(int)

# -----------------------------------------------------
# Step 4: Clean numeric columns
# -----------------------------------------------------
data["price"] = pd.to_numeric(data["price"], errors="coerce").fillna(0)
data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce").fillna(1)
data["order_value"] = data["price"] * data["quantity"]

print("\n✅ Data loaded and cleaned successfully!\n")

# -----------------------------------------------------
# Step 5: Overall return rate
# -----------------------------------------------------
overall_return_rate = data["is_returned"].mean() * 100
print(f"📊 Overall Return Rate: {overall_return_rate:.2f}%\n")

# -----------------------------------------------------
# Step 6: Return Rate by Category
# -----------------------------------------------------
cat_rr = data.groupby("category")["is_returned"].mean().reset_index()
cat_rr["return_rate_%"] = cat_rr["is_returned"] * 100
cat_rr = cat_rr.sort_values("return_rate_%", ascending=False)
print("🔹 Return Rate by Category:\n", cat_rr, "\n")

# -----------------------------------------------------
# Step 7: Return Rate by Supplier
# -----------------------------------------------------
sup_rr = data.groupby("supplier")["is_returned"].mean().reset_index()
sup_rr["return_rate_%"] = sup_rr["is_returned"] * 100
sup_rr = sup_rr.sort_values("return_rate_%", ascending=False)
print("🔹 Return Rate by Supplier:\n", sup_rr, "\n")

# -----------------------------------------------------
# Step 8: Return Rate by Marketing Channel
# -----------------------------------------------------
chan_rr = data.groupby("marketing_channel")["is_returned"].mean().reset_index()
chan_rr["return_rate_%"] = chan_rr["is_returned"] * 100
chan_rr = chan_rr.sort_values("return_rate_%", ascending=False)
print("🔹 Return Rate by Marketing Channel:\n", chan_rr, "\n")

# -----------------------------------------------------
# Step 9: Rule-Based Return Risk Score
# -----------------------------------------------------
product_risk = data.groupby(["product_id", "category", "supplier"]).agg(
    total_orders=("order_id", "count"),
    total_returns=("is_returned", "sum"),
    avg_price=("price", "mean")
).reset_index()

# Product return rate
product_risk["product_return_rate"] = product_risk["total_returns"] / product_risk["total_orders"]

# Merge with category-level rate
product_risk = pd.merge(product_risk, cat_rr[["category", "return_rate_%"]],
                        on="category", how="left")
product_risk["category_return_rate"] = product_risk["return_rate_%"] / 100

# Final score = 70% product + 30% category risk
product_risk["return_risk_score"] = (
    0.7 * product_risk["product_return_rate"] + 0.3 * product_risk["category_return_rate"]
)

# -----------------------------------------------------
# Step 10: Save high-risk products
# -----------------------------------------------------
cutoff = product_risk["return_risk_score"].quantile(0.7)
high_risk = product_risk[product_risk["return_risk_score"] >= cutoff]

output_path = os.path.join(OUTPUT_DIR, "high_risk_products.csv")
high_risk.to_csv(output_path, index=False)

print("💾 High-risk products saved to:", output_path)
print("\n📈 Top High-Risk Products:\n", high_risk[["product_id", "category", "supplier", "return_risk_score"]])

print("\n✅ Analysis complete! You can now import 'high_risk_products.csv' into Power BI.")