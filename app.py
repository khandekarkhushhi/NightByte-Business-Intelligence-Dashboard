import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="NightByte Analytics",
    page_icon="🌙",
    layout="wide"
)

df = pd.read_csv("data/orders.csv")

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Revenue"] = df["Quantity"] * df["Price"]
df["Hour"] = df["Order_Date"].dt.hour
df["Day"] = df["Order_Date"].dt.day_name()
df["Month"] = df["Order_Date"].dt.month_name()

st.title("🌙 NightByte Business Intelligence & Demand Forecasting Dashboard")
st.write("Analytics dashboard for food delivery orders, customer behavior, revenue trends, and demand forecasting.")

st.sidebar.header("Dashboard Filters")

selected_location = st.sidebar.selectbox(
    "Select Location",
    ["All"] + sorted(df["Location"].unique().tolist())
)

selected_payment = st.sidebar.selectbox(
    "Select Payment Mode",
    ["All"] + sorted(df["Payment_Mode"].unique().tolist())
)

if selected_location != "All":
    df = df[df["Location"] == selected_location]

if selected_payment != "All":
    df = df[df["Payment_Mode"] == selected_payment]

total_revenue = df["Revenue"].sum()
total_orders = df["Order_ID"].nunique()
avg_order_value = total_revenue / total_orders if total_orders != 0 else 0
total_customers = df["Customer_ID"].nunique()

daily_ml = (
    df.groupby(df["Order_Date"].dt.date)["Revenue"]
    .sum()
    .reset_index()
)

if len(daily_ml) > 1:
    daily_ml["Day_Number"] = range(len(daily_ml))

    X = daily_ml[["Day_Number"]]
    y = daily_ml["Revenue"]

    model = LinearRegression()
    model.fit(X, y)

    future_day = pd.DataFrame({
        "Day_Number": [len(daily_ml)]
    })

    predicted_revenue = model.predict(future_day)[0]
else:
    predicted_revenue = 0

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
c2.metric("Total Orders", total_orders)
c3.metric("Average Order Value", f"₹{avg_order_value:.2f}")
c4.metric("Predicted Revenue Tomorrow", f"₹{predicted_revenue:.0f}")

st.divider()

st.subheader("📌 Business Insights")

top_item_name = df.groupby("Item_Name")["Quantity"].sum().idxmax()
top_location = df.groupby("Location")["Revenue"].sum().idxmax()
peak_hour = df.groupby("Hour")["Order_ID"].count().idxmax()
best_payment = df["Payment_Mode"].value_counts().idxmax()

st.write(f"✅ Most ordered item: **{top_item_name}**")
st.write(f"✅ Highest revenue location: **{top_location}**")
st.write(f"✅ Peak ordering hour: **{peak_hour}:00**")
st.write(f"✅ Most used payment mode: **{best_payment}**")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("🍽️ Top Selling Items")

    top_items = (
        df.groupby("Item_Name")["Quantity"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots()
    top_items.plot(kind="bar", ax=ax)
    ax.set_xlabel("Item Name")
    ax.set_ylabel("Quantity Sold")
    ax.set_title("Top 10 Selling Items")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    st.subheader("💰 Revenue by Item")

    item_revenue = (
        df.groupby("Item_Name")["Revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig, ax = plt.subplots()
    item_revenue.plot(kind="bar", ax=ax)
    ax.set_xlabel("Item Name")
    ax.set_ylabel("Revenue")
    ax.set_title("Top 10 Items by Revenue")
    plt.xticks(rotation=45)
    st.pyplot(fig)

col3, col4 = st.columns(2)

with col3:
    st.subheader("⏰ Peak Ordering Hours")

    hourly = df.groupby("Hour")["Order_ID"].count()

    fig, ax = plt.subplots()
    hourly.plot(kind="line", marker="o", ax=ax)
    ax.set_xlabel("Hour")
    ax.set_ylabel("Number of Orders")
    ax.set_title("Orders by Hour")
    st.pyplot(fig)

with col4:
    st.subheader("📍 Revenue by Location")

    location_rev = (
        df.groupby("Location")["Revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots()
    location_rev.plot(kind="bar", ax=ax)
    ax.set_xlabel("Location")
    ax.set_ylabel("Revenue")
    ax.set_title("Location-wise Revenue")
    plt.xticks(rotation=30)
    st.pyplot(fig)

col5, col6 = st.columns(2)

with col5:
    st.subheader("💳 Payment Mode Usage")

    payment = df["Payment_Mode"].value_counts()

    fig, ax = plt.subplots()
    payment.plot(kind="pie", autopct="%1.1f%%", ax=ax)
    ax.set_ylabel("")
    ax.set_title("Payment Mode Distribution")
    st.pyplot(fig)

with col6:
    st.subheader("📈 Daily Revenue Trend")

    daily_revenue = df.groupby(df["Order_Date"].dt.date)["Revenue"].sum()

    fig, ax = plt.subplots()
    daily_revenue.plot(ax=ax)
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")
    ax.set_title("Daily Revenue Trend")
    plt.xticks(rotation=45)
    st.pyplot(fig)

st.divider()

st.subheader("👥 Customer Segmentation")

customer_data = (
    df.groupby("Customer_ID")
    .agg(
        Total_Spent=("Revenue", "sum"),
        Total_Orders=("Order_ID", "nunique"),
        Total_Quantity=("Quantity", "sum")
    )
    .sort_values(by="Total_Spent", ascending=False)
)

def customer_segment(amount):
    if amount >= customer_data["Total_Spent"].quantile(0.75):
        return "High Value Customer"
    elif amount >= customer_data["Total_Spent"].quantile(0.40):
        return "Medium Value Customer"
    else:
        return "Low Value Customer"

customer_data["Customer_Segment"] = customer_data["Total_Spent"].apply(customer_segment)

st.dataframe(customer_data.head(20))

st.subheader("📊 Customer Segment Count")

segment_count = customer_data["Customer_Segment"].value_counts()

fig, ax = plt.subplots()
segment_count.plot(kind="bar", ax=ax)
ax.set_xlabel("Customer Segment")
ax.set_ylabel("Number of Customers")
ax.set_title("Customer Segmentation")
plt.xticks(rotation=20)
st.pyplot(fig)

st.divider()

st.subheader("📄 Dataset Preview")
st.dataframe(df.head(30))

st.download_button(
    label="Download Filtered Dataset",
    data=df.to_csv(index=False),
    file_name="nightbyte_filtered_orders.csv",
    mime="text/csv"
)