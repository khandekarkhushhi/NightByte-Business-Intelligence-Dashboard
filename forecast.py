import pandas as pd
from sklearn.linear_model import LinearRegression

df = pd.read_csv("data/orders.csv")

df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Revenue"] = df["Quantity"] * df["Price"]

daily = (
    df.groupby(df["Order_Date"].dt.date)["Revenue"]
    .sum()
    .reset_index()
)

daily["Day_Number"] = range(len(daily))

X = daily[["Day_Number"]]
y = daily["Revenue"]

model = LinearRegression()
model.fit(X, y)

next_day = [[len(daily)]]

prediction = model.predict(next_day)

print("Predicted Revenue Tomorrow:", round(prediction[0], 2))