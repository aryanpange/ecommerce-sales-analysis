import pandas as pd

# Load dataset
df = pd.read_csv("data.csv", encoding='ISO-8859-1')

# View top rows and column info
print(df.head())
print(df.info())
print(df.describe())
# Drop rows with missing CustomerID or Description
df.dropna(subset=['CustomerID', 'Description'], inplace=True)

# Convert InvoiceDate to datetime
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

# Create a new column for TotalPrice
df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

# Filter out canceled transactions (Invoice starts with 'C')
df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

# Optional: Filter out negative or zero prices
df = df[df['TotalPrice'] > 0]

print("✅ Cleaned data shape:", df.shape)
# Create Month-Year column
df['InvoiceMonth'] = df['InvoiceDate'].dt.to_period('M')

# Group by Month and sum Total Sales
monthly_sales = df.groupby('InvoiceMonth')['TotalPrice'].sum().reset_index()
monthly_sales['InvoiceMonth'] = monthly_sales['InvoiceMonth'].astype(str)

# Plot
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12,6))
sns.lineplot(x='InvoiceMonth', y='TotalPrice', data=monthly_sales, marker='o')
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales (£)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
 
top_products = df.groupby('Description')['TotalPrice'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=top_products.values, y=top_products.index, palette='mako')
plt.title("Top 10 Products by Total Sales")
plt.xlabel("Total Sales (£)")
plt.ylabel("Product")
plt.tight_layout()
plt.show()

top_customers = df.groupby('CustomerID')['TotalPrice'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(10,6))
sns.barplot(x=top_customers.values, y=top_customers.index.astype(str), palette='viridis')
plt.title("Top 10 Customers by Revenue")
plt.xlabel("Total Spend (£)")
plt.ylabel("Customer ID")
plt.tight_layout()
plt.show()

# Reference date = 1 day after the last InvoiceDate
ref_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = df.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (ref_date - x.max()).days,  # Recency
    'InvoiceNo': 'nunique',                              # Frequency
    'TotalPrice': 'sum'                                  # Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']
print(rfm.describe())

