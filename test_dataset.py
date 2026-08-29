import pandas as pd

df = pd.read_csv("data/creditcard.csv")

print("Dataset loaded successfully!")
print("Shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())