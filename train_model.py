import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score
)

from xgboost import XGBClassifier


# ============================================
# 1. LOAD DATASET
# ============================================

print("Loading dataset...")

df = pd.read_csv("data/creditcard.csv")

print("Dataset loaded!")
print("Shape:", df.shape)


# ============================================
# 2. SEPARATE FEATURES AND TARGET
# ============================================

X = df.drop("Class", axis=1)
y = df["Class"]


# ============================================
# 3. TRAIN-TEST SPLIT
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ============================================
# 4. SCALE TIME AND AMOUNT
# ============================================

scaler = StandardScaler()

X_train[["Time", "Amount"]] = scaler.fit_transform(
    X_train[["Time", "Amount"]]
)

X_test[["Time", "Amount"]] = scaler.transform(
    X_test[["Time", "Amount"]]
)


# ============================================
# 5. CREATE MODELS
# ============================================

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1
    ),

    "XGBoost": XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1
    )
}


# ============================================
# 6. TRAIN AND EVALUATE MODELS
# ============================================

for name, model in models.items():

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    print("Training...")

    # Train model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Fraud probability
    y_prob = model.predict_proba(X_test)[:, 1]

    # Calculate metrics
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    pr_auc = average_precision_score(y_test, y_prob)

    # Display results
    print("Precision :", round(precision, 4))
    print("Recall    :", round(recall, 4))
    print("F1 Score  :", round(f1, 4))
    print("ROC-AUC   :", round(roc_auc, 4))
    print("PR-AUC    :", round(pr_auc, 4))

    # ========================================
    # SAVE XGBOOST MODEL
    # ========================================

    if name == "XGBoost":

        os.makedirs("models", exist_ok=True)

        joblib.dump(
            model,
            "models/xgboost_fraud_model.pkl"
        )

        joblib.dump(
            scaler,
            "models/scaler.pkl"
        )

        print("\nXGBoost model saved successfully!")
        print("Scaler saved successfully!")


# ============================================
# 7. FINISHED
# ============================================

print("\n============================================")
print("MODEL TRAINING COMPLETED!")
print("============================================")
print("\nSaved files:")
print("models/xgboost_fraud_model.pkl")
print("models/scaler.pkl")