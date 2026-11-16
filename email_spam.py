
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

# 1. LOAD DATASET

print("\n========== 1. LOADING DATASET ==========")

df = pd.read_csv("ML/email_spam_detection/emails.csv")

print("Dataset Shape:", df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nColumn Names:")
print(df.columns)

# 2. DATA PREPROCESSING

print("\n========== 2. DATA PREPROCESSING ==========")

# Remove duplicate records
df = df.drop_duplicates()

# Remove rows containing missing values
df = df.dropna()

# Separate features and target      First column = Email ID     Last column = Prediction

X = df.iloc[:, 1:-1]
y = df.iloc[:, -1]

# Convert features into numeric values
X = X.apply(pd.to_numeric, errors="coerce")

# Remove rows containing invalid feature values
valid_rows = X.notna().all(axis=1)

X = X.loc[valid_rows]
y = y.loc[valid_rows]

# Convert target into integer values
y = pd.to_numeric(y).astype(int)

# Check target labels
if not set(y.unique()).issubset({0, 1}):
    raise ValueError("Target column must contain only 0 and 1.")

print("Dataset after preprocessing:", X.shape)
print("Target shape:", y.shape)

print("\nSpam and Normal Email Distribution:")
print(y.value_counts().rename(index={
    0: "Normal Email",
    1: "Spam Email"
}))

# 3. SPLIT DATASET INTO TRAINING AND TESTING

print("\n========== 3. TRAIN TEST SPLIT ==========")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)

# 4. K-NEAREST NEIGHBORS (KNN)

print("\n========== 4. KNN CLASSIFICATION ==========")

knn_model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", KNeighborsClassifier(
        n_neighbors=5,
        n_jobs=-1
    ))
])

print("Training KNN model...")

knn_model.fit(X_train, y_train)

knn_predictions = knn_model.predict(X_test)

print("KNN prediction completed!")

# 5. SUPPORT VECTOR MACHINE (SVM)

print("\n========== 5. SVM CLASSIFICATION ==========")

svm_model = Pipeline([
    ("scaler", StandardScaler()),
    ("classifier", LinearSVC(
        random_state=42,
        max_iter=10000
    ))
])

print("Training SVM model...")

svm_model.fit(X_train, y_train)

svm_predictions = svm_model.predict(X_test)

print("SVM prediction completed!")

# 6. MODEL EVALUATION

print("\n========== 6. MODEL EVALUATION ==========")

def evaluate_model(model_name, actual, predicted):

    accuracy = accuracy_score(actual, predicted)

    precision = precision_score(
        actual, predicted, zero_division=0
    )

    recall = recall_score(
        actual, predicted, zero_division=0
    )

    f1 = f1_score(
        actual, predicted, zero_division=0
    )

    print("\n", model_name, "PERFORMANCE")
    print("--------------------------------")

    print("Accuracy :", round(accuracy * 100, 2), "%")
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))

    print("\nClassification Report:")
    print(classification_report(
        actual,
        predicted,
        zero_division=0
    ))

    return [accuracy, precision, recall, f1]


knn_results = evaluate_model(
    "KNN", y_test, knn_predictions
)

svm_results = evaluate_model(
    "SVM", y_test, svm_predictions
)

# 7. COMPARE BOTH MODELS

print("\n========== 7. MODEL COMPARISON ==========")

comparison = pd.DataFrame(
    [knn_results, svm_results],
    columns=[
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score"
    ],
    index=["KNN", "SVM"]
)

print(comparison.round(4))

# 8. CONFUSION MATRIX

print("\n========== 8. CONFUSION MATRIX ==========")

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

ConfusionMatrixDisplay.from_predictions(
    y_test,
    knn_predictions,
    display_labels=["Normal", "Spam"],
    cmap="Blues",
    ax=axes[0],
    colorbar=False
)

axes[0].set_title("KNN Confusion Matrix")

ConfusionMatrixDisplay.from_predictions(
    y_test,
    svm_predictions,
    display_labels=["Normal", "Spam"],
    cmap="Purples",
    ax=axes[1],
    colorbar=False
)

axes[1].set_title("SVM Confusion Matrix")

plt.tight_layout()
plt.savefig("confusion_matrices.png")
plt.close()

# 9. PERFORMANCE COMPARISON GRAPH

print("\n========== 9. PERFORMANCE GRAPH ==========")

comparison.plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("KNN vs SVM Performance Comparison")
plt.xlabel("Classification Algorithms")
plt.ylabel("Performance Score")
plt.ylim(0, 1.05)
plt.xticks(rotation=0)
plt.legend(loc="lower right")
plt.tight_layout()

plt.savefig("model_comparison.png")
plt.close()

# 10. FINAL RESULT

print("\n========== 10. FINAL RESULT ==========")

if svm_results[0] > knn_results[0]:
    print("SVM performed better in terms of accuracy.")

elif knn_results[0] > svm_results[0]:
    print("KNN performed better in terms of accuracy.")

else:
    print("Both models achieved equal accuracy.")

print("\nPractical executed successfully!")

print("\nGenerated Files:")
print("1. confusion_matrices.png")
print("2. model_comparison.png")
