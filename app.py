import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Retail Sales Analysis & Business Insights Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_sample_data():
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", end="2025-12-31", freq="D")
    n_rows = 400

    regions = ["North", "South", "East", "West"]
    categories = {
        "Electronics": ["Smartphone", "Laptop", "Headphones", "Smartwatch"],
        "Apparel": ["T-Shirt", "Jeans", "Jacket", "Sneakers"],
        "Groceries": ["Rice Bag", "Cooking Oil", "Snacks", "Beverages"],
        "Home & Kitchen": ["Mixer Grinder", "Cookware Set", "Bedsheet", "Table Lamp"]
    }
    payment_modes = ["UPI", "Credit Card", "Debit Card", "Cash"]

    selected_dates = np.random.choice(dates, size=n_rows)
    selected_regions = np.random.choice(regions, size=n_rows, p=[0.28, 0.24, 0.22, 0.26])
    selected_categories = np.random.choice(list(categories.keys()), size=n_rows)

    products = []
    unit_prices = []
    for cat in selected_categories:
        prod = np.random.choice(categories[cat])
        products.append(prod)
        base_price = {
            "Electronics": np.random.randint(1500, 55000),
            "Apparel": np.random.randint(500, 4500),
            "Groceries": np.random.randint(80, 1800),
            "Home & Kitchen": np.random.randint(400, 8500)
        }[cat]
        unit_prices.append(base_price)

    quantities = np.random.randint(1, 6, size=n_rows)
    payments = np.random.choice(payment_modes, size=n_rows, p=[0.42, 0.23, 0.20, 0.15])

    df = pd.DataFrame({
        "Order_Date": pd.to_datetime(selected_dates),
        "Region": selected_regions,
        "Category": selected_categories,
        "Product": products,
        "Quantity": quantities,
        "Unit_Price": unit_prices,
        "Payment_Mode": payments
    })

    df["Total_Sales"] = df["Quantity"] * df["Unit_Price"]
    profit_margin = np.random.uniform(0.10, 0.32, size=n_rows)
    df["Profit"] = (df["Total_Sales"] * profit_margin).round(2)
    df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)
    df = df.sort_values("Order_Date").reset_index(drop=True)
    return df

df = load_sample_data()

st.title("📊 Retail Sales Analysis & Business Insights Dashboard")
st.markdown("Interactive analysis of sales performance, regional trends, category profitability, and customer payment behavior.")

st.sidebar.header("🔎 Filter Data")
selected_region = st.sidebar.multiselect(
    "Select Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)
selected_category = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)
selected_payment = st.sidebar.multiselect(
    "Select Payment Mode",
    options=sorted(df["Payment_Mode"].unique()),
    default=sorted(df["Payment_Mode"].unique())
)

filtered_df = df[
    (df["Region"].isin(selected_region)) &
    (df["Category"].isin(selected_category)) &
    (df["Payment_Mode"].isin(selected_payment))
]

if filtered_df.empty:
    st.warning("No records match the selected filters. Please adjust your filter selection.")
    st.stop()

total_sales = filtered_df["Total_Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = len(filtered_df)
avg_order_value = total_sales / total_orders if total_orders > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"₹{total_sales:,.0f}")
col2.metric("Total Profit", f"₹{total_profit:,.0f}")
col3.metric("Total Orders", f"{total_orders:,}")
col4.metric("Avg. Order Value", f"₹{avg_order_value:,.0f}")

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Monthly Sales Trend")
    monthly_sales = filtered_df.groupby("Month")["Total_Sales"].sum()
    fig1, ax1 = plt.subplots(figsize=(6, 3.8))
    ax1.plot(monthly_sales.index, monthly_sales.values, marker="o", linewidth=2)
    ax1.set_xlabel("Month")
    ax1.set_ylabel("Sales (₹)")
    ax1.tick_params(axis="x", rotation=45)
    ax1.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    st.pyplot(fig1)

with col_right:
    st.subheader("🏷️ Sales by Category")
    category_sales = filtered_df.groupby("Category")["Total_Sales"].sum().sort_values(ascending=True)
    fig2, ax2 = plt.subplots(figsize=(6, 3.8))
    ax2.barh(category_sales.index, category_sales.values)
    ax2.set_xlabel("Total Sales (₹)")
    ax2.set_ylabel("Category")
    plt.tight_layout()
    st.pyplot(fig2)

col_bottom_left, col_bottom_right = st.columns(2)

with col_bottom_left:
    st.subheader("🌍 Profit by Region")
    region_profit = filtered_df.groupby("Region")["Profit"].sum().sort_values(ascending=False)
    fig3, ax3 = plt.subplots(figsize=(6, 3.8))
    ax3.bar(region_profit.index, region_profit.values)
    ax3.set_xlabel("Region")
    ax3.set_ylabel("Profit (₹)")
    plt.tight_layout()
    st.pyplot(fig3)

with col_bottom_right:
    st.subheader("💳 Payment Mode Share")
    payment_counts = filtered_df["Payment_Mode"].value_counts()
    fig4, ax4 = plt.subplots(figsize=(6, 3.8))
    ax4.pie(payment_counts.values, labels=payment_counts.index, autopct="%1.1f%%", startangle=90)
    ax4.axis("equal")
    plt.tight_layout()
    st.pyplot(fig4)

st.divider()

st.subheader("💡 Key Business Insights")
top_cat = filtered_df.groupby("Category")["Total_Sales"].sum().idxmax()
top_reg = filtered_df.groupby("Region")["Total_Sales"].sum().idxmax()
top_pay = filtered_df["Payment_Mode"].value_counts().idxmax()

st.markdown(f"""
- **Highest Revenue Category:** **{top_cat}** leads overall sales across the selected filters.
- **Top Performing Region:** **{top_reg}** contributes the strongest sales volume.
- **Preferred Payment Method:** **{top_pay}** is the most frequently used payment option by customers.
""")

st.subheader("📋 Filtered Sales Dataset")
st.dataframe(filtered_df, use_container_width=True)
