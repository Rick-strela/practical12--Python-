import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('sales.xlsx')

print("=== ІНФОРМАЦІЯ ПРО ДАТАСЕТ ===")
print(df.info())

print("\n=== ОПИСОВА СТАТИСТИКА ===")
print(df.describe())

print("\nКількість дублікатів:", df.duplicated().sum())
print("Кількість пропусків по стовпцях:\n", df.isnull().sum())

df_clean = df.drop_duplicates().copy()

median_quantity = df_clean['quantity'].median()
df_clean['quantity'] = df_clean['quantity'].fillna(median_quantity)

df_clean['sales'] = df_clean['price'] * df_clean['quantity']

median_sales = df_clean['sales'].median()
df_clean['sales'] = df_clean['sales'].fillna(median_sales)

df_clean = df_clean.dropna(subset=['customer'])

df_clean = df_clean[df_clean['sales'] > 0]

print("\n=== СТАТИСТИКА ПІСЛЯ ОЧИЩЕННЯ ===")
print(df_clean.info())

customer_summary = df_clean.groupby('customer').agg(
    total_sales=('sales', 'sum'),
    avg_check=('sales', 'mean'),
    order_count=('sales', 'count')
).reset_index()

customer_summary = customer_summary.sort_values(by='total_sales', ascending=False)

print("\n=== РЕЗУЛЬТАТИ ГРУПУВАННЯ ЗА КЛІЄНТАМИ ===")
print(customer_summary.to_string(index=False))

plt.figure(figsize=(10, 6))
sns.set_theme(style="whitegrid")

ax = sns.barplot(
    data=customer_summary,
    x='customer',
    y='total_sales',
    palette='viridis'
)

plt.title('Total Sales by Customer', fontsize=14, fontweight='bold')
plt.xlabel('Клієнт', fontsize=12)
plt.ylabel('Сумарний обіг (грн)', fontsize=12)

for p in ax.patches:
    ax.annotate(
        f'{p.get_height():,.0f}',
        (p.get_x() + p.get_width() / 2., p.get_height()),
        ha='center', va='bottom',
        fontsize=10, xytext=(0, 5),
        textcoords='offset points'
    )

plt.tight_layout()
plt.savefig('total_sales_by_customer.png', dpi=300)
plt.show()