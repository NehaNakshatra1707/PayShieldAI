import pandas as pd

df = pd.read_csv("data/creditcard.csv")

fraud = df[df["Class"] == 1].iloc[0]

print("\n========== FRAUD TRANSACTION ==========\n")

print(fraud.to_string())

print("\n======================================")