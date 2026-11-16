import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import classification_report
from sklearn.utils.class_weight import compute_class_weight

dataset = pd.read_csv("ML/ANN/Churn_Modelling.csv")
print(dataset.head())
print(dataset.shape)


# STEP 3: Separate features and target
# Remove unnecessary columns
X = dataset.drop(
    columns=["RowNumber", "CustomerId", "Surname", "Exited"]
)

# Target variable
y = dataset["Exited"]

# STEP 4: Split dataset into training and testing sets

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining Data Shape:", X_train.shape)
print("Testing Data Shape:", X_test.shape)

# STEP 5: Normalize and encode the data

numerical_columns = [
    "CreditScore",
    "Age",
    "Tenure",
    "Balance",
    "NumOfProducts",
    "HasCrCard",
    "IsActiveMember",
    "EstimatedSalary"
]

categorical_columns = ["Geography", "Gender"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numerical_columns),
        ("cat", OneHotEncoder(handle_unknown="ignore"),
         categorical_columns)
    ],
    sparse_threshold=0.0
)

# Fit on training data and transform
X_train = preprocessor.fit_transform(X_train)

# Transform testing data
X_test = preprocessor.transform(X_test)

print("\nNormalized Training Shape:", X_train.shape)
print("Normalized Testing Shape:", X_test.shape)


# STEP 6: Build the initial ANN model

initial_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),

    tf.keras.layers.Dense(16, activation="relu"),

    tf.keras.layers.Dense(8, activation="relu"),

    tf.keras.layers.Dense(1, activation="sigmoid")
])

initial_model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

print("\nInitial ANN Model Summary:")
initial_model.summary()


# STEP 7: Train the initial model
initial_history = initial_model.fit(
    X_train,
    y_train,
    epochs=30,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)
# STEP 8: Identify points of improvement

# Improvements:
# 1. More neurons
# 2. Batch Normalization
# 3. Dropout to prevent overfitting
# 4. Early Stopping
# 5. Class weights for imbalanced data


# Calculate class weights

classes = np.unique(y_train)

weights = compute_class_weight(
    class_weight="balanced",
    classes=classes,
    y=y_train
)

class_weights = dict(zip(classes, weights))


# STEP 9: Build improved ANN model

improved_model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(X_train.shape[1],)),

    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.3),

    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Dropout(0.2),

    tf.keras.layers.Dense(16, activation="relu"),

    tf.keras.layers.Dense(1, activation="sigmoid")
])

improved_model.compile(
    optimizer="adam",
    loss="binary_crossentropy",
    metrics=["accuracy"]
)

print("\nImproved ANN Model Summary:")
improved_model.summary()


# STEP 10: Train improved model using Early Stopping

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

improved_history = improved_model.fit(
    X_train,
    y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[early_stopping],
    class_weight=class_weights,
    verbose=1
)


# STEP 11: Predict test data

y_pred_probability = improved_model.predict(X_test)

# Convert probabilities into 0 or 1
y_pred = (y_pred_probability >= 0.5).astype(int).ravel()


# STEP 12: Calculate accuracy

accuracy = accuracy_score(y_test, y_pred)

print("\n===================================")
print("MODEL ACCURACY")
print("===================================")

print("Accuracy:", round(accuracy * 100, 2), "%")


# STEP 13: Calculate confusion matrix

cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:")
print(cm)


# STEP 14: Display confusion matrix using heatmap

plt.figure(figsize=(6, 4))

sns.heatmap(
    cm,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=["Stayed (0)", "Exited (1)"],
    yticklabels=["Stayed (0)", "Exited (1)"]
)

plt.xlabel("Predicted Values")
plt.ylabel("Actual Values")
plt.title("Bank Customer Churn Confusion Matrix")

plt.show()


# STEP 15: Display classification report

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        target_names=["Stayed", "Exited"]
    )
)


# STEP 16: Plot training and validation accuracy

plt.figure(figsize=(8, 5))

plt.plot(
    improved_history.history["accuracy"],
    label="Training Accuracy"
)

plt.plot(
    improved_history.history["val_accuracy"],
    label="Validation Accuracy"
)

plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.title("ANN Training and Validation Accuracy")

plt.legend()
plt.grid()

plt.show()


# STEP 17: Plot training and validation loss

plt.figure(figsize=(8, 5))

plt.plot(
    improved_history.history["loss"],
    label="Training Loss"
)

plt.plot(
    improved_history.history["val_loss"],
    label="Validation Loss"
)

plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("ANN Training and Validation Loss")

plt.legend()
plt.grid()

plt.show()


# STEP 18: Final result

print("\n===================================")
print("BANK CUSTOMER CHURN PREDICTION")
print("===================================")

print("Final Model Accuracy:",
      round(accuracy * 100, 2), "%")


