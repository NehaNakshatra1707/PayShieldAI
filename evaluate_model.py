import pandas as pd
import numpy as np
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix,
    classification_report
)

import matplotlib.pyplot as plt


# =========================================================
# PAYSHIELD AI - MODEL EVALUATION
# =========================================================

print("=" * 60)
print("           PAYSHIELD AI MODEL EVALUATION")
print("=" * 60)


# =========================================================
# 1. LOAD DATASET
# =========================================================

print("\nLoading dataset...")

df = pd.read_csv(
    "data/creditcard.csv"
)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)


# =========================================================
# 2. SEPARATE FEATURES AND TARGET
# =========================================================

X = df.drop(
    "Class",
    axis=1
)

y = df["Class"]


print("\nFeatures:", X.shape[1])
print("Target column: Class")

print("\nClass distribution:")
print(y.value_counts())


# =========================================================
# 3. TRAIN-TEST SPLIT
# =========================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42,

    stratify=y
)


print("\nTraining samples:", len(X_train))
print("Testing samples :", len(X_test))


# =========================================================
# 4. SCALE TIME AND AMOUNT
# =========================================================

print("\nApplying preprocessing...")

scaler = StandardScaler()

X_train = X_train.copy()
X_test = X_test.copy()

X_train[["Time", "Amount"]] = scaler.fit_transform(
    X_train[["Time", "Amount"]]
)

X_test[["Time", "Amount"]] = scaler.transform(
    X_test[["Time", "Amount"]]
)


print("✅ Time and Amount standardized.")
print("✅ V1-V28 kept unchanged.")


# =========================================================
# 5. LOAD TRAINED XGBOOST MODEL
# =========================================================

MODEL_PATH = os.path.join(
    "models",
    "xgboost_fraud_model.pkl"
)


print("\nLoading trained XGBoost model...")

model = joblib.load(
    MODEL_PATH
)

print("✅ XGBoost model loaded successfully.")


# =========================================================
# 6. MAKE PREDICTIONS
# =========================================================

print("\nGenerating predictions...")

y_pred = model.predict(
    X_test
)

y_prob = model.predict_proba(
    X_test
)[:, 1]


print("✅ Predictions generated.")


# =========================================================
# 7. CALCULATE METRICS
# =========================================================

accuracy = accuracy_score(
    y_test,
    y_pred
)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

roc_auc = roc_auc_score(
    y_test,
    y_prob
)

pr_auc = average_precision_score(
    y_test,
    y_prob
)


# =========================================================
# 8. DISPLAY METRICS
# =========================================================

print("\n")
print("=" * 60)
print("                 MODEL PERFORMANCE")
print("=" * 60)

print(
    f"\nAccuracy  : {accuracy:.4f} "
    f"({accuracy * 100:.2f}%)"
)

print(
    f"Precision : {precision:.4f} "
    f"({precision * 100:.2f}%)"
)

print(
    f"Recall    : {recall:.4f} "
    f"({recall * 100:.2f}%)"
)

print(
    f"F1 Score  : {f1:.4f} "
    f"({f1 * 100:.2f}%)"
)

print(
    f"ROC-AUC   : {roc_auc:.4f}"
)

print(
    f"PR-AUC    : {pr_auc:.4f}"
)


# =========================================================
# 9. CLASSIFICATION REPORT
# =========================================================

print("\n")
print("=" * 60)
print("              CLASSIFICATION REPORT")
print("=" * 60)

print(
    classification_report(
        y_test,
        y_pred,
        target_names=[
            "Legitimate",
            "Fraud"
        ],
        zero_division=0
    )
)


# =========================================================
# 10. CONFUSION MATRIX
# =========================================================

cm = confusion_matrix(
    y_test,
    y_pred
)


print("\n")
print("=" * 60)
print("                 CONFUSION MATRIX")
print("=" * 60)

print(cm)

print("\nInterpretation:")

print(
    "True Negatives  :", cm[0][0]
)

print(
    "False Positives :", cm[0][1]
)

print(
    "False Negatives :", cm[1][0]
)

print(
    "True Positives   :", cm[1][1]
)


# =========================================================
# 11. FEATURE IMPORTANCE
# =========================================================

print("\n")
print("=" * 60)
print("                 FEATURE IMPORTANCE")
print("=" * 60)

if hasattr(
    model,
    "feature_importances_"
):

    feature_importance = pd.DataFrame({

        "Feature": X.columns,

        "Importance":
            model.feature_importances_

    })

    feature_importance = (
        feature_importance
        .sort_values(
            by="Importance",
            ascending=False
        )
    )

    print(
        feature_importance.to_string(
            index=False
        )
    )

    # -----------------------------------------------------
    # SAVE FEATURE IMPORTANCE
    # -----------------------------------------------------

    feature_importance.to_csv(
        "feature_importance.csv",
        index=False
    )

    print(
        "\n✅ Feature importance saved to "
        "feature_importance.csv"
    )


# =========================================================
# 12. SAVE METRICS
# =========================================================

metrics = pd.DataFrame({

    "Metric": [

        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "ROC-AUC",
        "PR-AUC"

    ],

    "Score": [

        accuracy,
        precision,
        recall,
        f1,
        roc_auc,
        pr_auc

    ]

})


metrics.to_csv(
    "model_metrics.csv",
    index=False
)


print(
    "\n✅ Metrics saved to model_metrics.csv"
)


# =========================================================
# 13. SAVE CONFUSION MATRIX
# =========================================================

cm_df = pd.DataFrame(

    cm,

    index=[
        "Actual Legitimate",
        "Actual Fraud"
    ],

    columns=[
        "Predicted Legitimate",
        "Predicted Fraud"
    ]
)


cm_df.to_csv(
    "confusion_matrix.csv"
)


print(
    "✅ Confusion matrix saved to confusion_matrix.csv"
)


# =========================================================
# 14. PLOT CONFUSION MATRIX
# =========================================================

plt.figure(
    figsize=(7, 6)
)

plt.imshow(
    cm,
    interpolation="nearest"
)

plt.title(
    "PayShield AI - Confusion Matrix"
)

plt.colorbar()

plt.xticks(
    [0, 1],
    [
        "Legitimate",
        "Fraud"
    ]
)

plt.yticks(
    [0, 1],
    [
        "Legitimate",
        "Fraud"
    ]
)

plt.xlabel(
    "Predicted Label"
)

plt.ylabel(
    "Actual Label"
)

for i in range(2):

    for j in range(2):

        plt.text(
            j,
            i,
            cm[i, j],
            ha="center",
            va="center"
        )


plt.tight_layout()

plt.savefig(
    "confusion_matrix.png",
    dpi=300
)

plt.close()


print(
    "✅ Confusion matrix chart saved to "
    "confusion_matrix.png"
)


# =========================================================
# 15. FEATURE IMPORTANCE CHART
# =========================================================

if hasattr(
    model,
    "feature_importances_"
):

    top_features = (
        feature_importance
        .head(15)
        .sort_values(
            by="Importance"
        )
    )

    plt.figure(
        figsize=(10, 7)
    )

    plt.barh(
        top_features["Feature"],
        top_features["Importance"]
    )

    plt.title(
        "Top 15 Features - XGBoost Fraud Detection"
    )

    plt.xlabel(
        "Importance"
    )

    plt.ylabel(
        "Feature"
    )

    plt.tight_layout()

    plt.savefig(
        "feature_importance.png",
        dpi=300
    )

    plt.close()


    print(
        "✅ Feature importance chart saved to "
        "feature_importance.png"
    )


# =========================================================
# FINISHED
# =========================================================

print("\n")
print("=" * 60)
print("          MODEL EVALUATION COMPLETED!")
print("=" * 60)

print("\nGenerated files:")

print("1. model_metrics.csv")
print("2. confusion_matrix.csv")
print("3. confusion_matrix.png")
print("4. feature_importance.csv")
print("5. feature_importance.png")

print("\nPayShield AI evaluation completed successfully.")

