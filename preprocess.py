import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load dataset
df = pd.read_csv("data/creditcard.csv")

print("Dataset loaded!")
print("Original shape:", df.shape)

# Separate features and target
X = df.drop("Class", axis=1)
y = df["Class"]

print("\nFeatures shape:", X.shape)
print("Target shape:", y.shape)

# Scale Amount and Time
scaler = StandardScaler()

X[["Time", "Amount"]] = scaler.fit_transform(X[["Time", "Amount"]])

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining data:")
print("X_train:", X_train.shape)
print("y_train:", y_train.shape)

print("\nTesting data:")
print("X_test:", X_test.shape)
print("y_test:", y_test.shape)

print("\nFraud in training data:")
print(y_train.value_counts())

print("\nFraud in testing data:")
print(y_test.value_counts())