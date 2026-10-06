import os
import pandas as pd
import matplotlib.pyplot as plt

# 1. Ensure the output directory exists
os.makedirs('visualizations', exist_ok=True)

# 2. Load and clean data (replicating Part 2 cleaning pipeline)
orders = pd.read_csv('orders.csv', header=0, skip_blank_lines=True)
customers = pd.read_csv('customers.csv', header=0, skip_blank_lines=True)
products = pd.read_csv('products.csv', header=0, skip_blank_lines=True)

# Standardize payment method casing
orders['payment_method'] = orders['payment_method'].str.strip().str.upper()

# Drop the 5 exact duplicates (Task 3)
subset_cols = [
    'customer_id', 'product_id', 'order_date', 'quantity', 
    'discount_pct', 'payment_method', 'rating', 'returned'
]
orders_clean = orders.drop_duplicates(subset=subset_cols, keep='first').copy()

# Impute missing values (Task 4)
orders_clean['discount_pct'] = orders_clean['discount_pct'].fillna(0)
orders_clean['rating'] = orders_clean['rating'].fillna(orders_clean['rating'].median())

# Merge datasets and compute order values (Task 5)
df = orders_clean.merge(products, on='product_id', how='left').merge(customers, on='customer_id', how='left')
df['order_value'] = df['quantity'] * df['price'] * (1 - df['discount_pct'] / 100.0)


# --- CHART 1: Return Rate by Payment Method ---
payment_summary = df.groupby('payment_method')['returned'].agg(['count', 'mean']).reset_index()
payment_summary['return_rate_pct'] = (payment_summary['mean'] * 100).round(1)
payment_summary = payment_summary.sort_values(by='return_rate_pct', ascending=True)

plt.figure(figsize=(8, 5))
bars = plt.barh(payment_summary['payment_method'], payment_summary['return_rate_pct'], color=['#4285F4', '#FBBC05', '#EA4335'])
plt.xlabel('Return Rate (%)')
plt.title('COD Returns at 44.4% — 3x Card')
plt.xlim(0, 50)

# Label exact percentages on each bar
for bar in bars:
    width = bar.get_width()
    plt.text(width + 1, bar.get_y() + bar.get_height()/2, f'{width:.1f}%', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig('visualizations/return_rate_by_payment.png', dpi=300)
plt.close()


# --- CHART 2: Outlier-Corrected Monthly Revenue Trend ---
# Apply IQR filter on quantity to exclude outliers (Task 6)
Q1 = df['quantity'].quantile(0.25)
Q3 = df['quantity'].quantile(0.75)
IQR = Q3 - Q1
upper_bound = Q3 + 1.5 * IQR

df_corrected = df[df['quantity'] <= upper_bound].copy()
df_corrected['order_date'] = pd.to_datetime(df_corrected['order_date'])
df_corrected['year_month'] = df_corrected['order_date'].dt.to_period('M')

monthly_rev = df_corrected.groupby('year_month')['order_value'].sum().reset_index()
monthly_rev['year_month_str'] = monthly_rev['year_month'].astype(str)

plt.figure(figsize=(10, 5))
plt.plot(monthly_rev['year_month_str'], monthly_rev['order_value'], marker='o', color='#2E7D32', linewidth=2.5, markersize=8)
plt.title('Outlier-Corrected Monthly Revenue Trend (Peak: March 2026 - ₹20,318.90)')
plt.xlabel('Month')
plt.ylabel('Revenue (INR)')
plt.grid(True, linestyle='--', alpha=0.6)

for i, row in monthly_rev.iterrows():
    plt.text(row['year_month_str'], row['order_value'] + 600, f'₹{row["order_value"]:,.1f}', ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('visualizations/monthly_revenue_trend.png', dpi=300)
plt.close()

print("Successfully generated and saved both visualization PNGs to the 'visualizations/' folder!")
