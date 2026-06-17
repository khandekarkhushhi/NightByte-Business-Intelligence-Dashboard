import pandas as pd

df = pd.read_csv("orders.csv")

print(df.head())
print(df.info())
print(df.isnull().sum())