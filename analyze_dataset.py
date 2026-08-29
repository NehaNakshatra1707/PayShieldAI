import pandas as pd

# Load dataset
df = pd.read_csv("data/creditcard.csv")

print("========== DATASET INFORMATION ==========")

print("\nShape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nClass Distribution:")
print(df["Class"].value_counts())

print("\nClass Percentage:")
print(df["Class"].value_counts(normalize=True) * 100)

print("\nBasic Statistics:")
print(df.describe())