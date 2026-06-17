import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

items = {
    "Maggi": 40,
    "Veg Sandwich": 60,
    "Cheese Sandwich": 80,
    "Cold Coffee": 70,
    "Tea": 15,
    "Coffee": 25,
    "French Fries": 90,
    "Veg Burger": 75,
    "Paneer Roll": 100,
    "Aloo Paratha": 50,
    "Masala Dosa": 80,
    "Momos": 70,
    "Pizza Slice": 120,
    "Pasta": 110,
    "Spring Roll": 90
}

customers = [f"CUST{str(i).zfill(3)}" for i in range(1, 121)]
hostels = ["Girls Hostel", "Boys Hostel", "Main Gate", "Library Area", "Sports Complex"]
payment_modes = ["UPI", "Cash", "Card"]

data = []

start_date = datetime(2026, 1, 1)

for order_id in range(1, 1001):
    order_date = start_date + timedelta(
        days=random.randint(0, 120),
        hours=random.choice([19, 20, 21, 22, 23, 0, 1, 2]),
        minutes=random.randint(0, 59)
    )

    item_name = random.choice(list(items.keys()))
    price = items[item_name]
    quantity = random.randint(1, 4)
    customer_id = random.choice(customers)
    location = random.choice(hostels)
    payment_mode = random.choice(payment_modes)

    data.append([
        f"ORD{str(order_id).zfill(4)}",
        order_date,
        customer_id,
        item_name,
        quantity,
        price,
        location,
        payment_mode
    ])

df = pd.DataFrame(data, columns=[
    "Order_ID",
    "Order_Date",
    "Customer_ID",
    "Item_Name",
    "Quantity",
    "Price",
    "Location",
    "Payment_Mode"
])

df.to_csv("orders.csv", index=False)

print("Dataset created successfully!")
print(df.head())