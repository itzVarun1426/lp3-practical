
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. DATA PREPROCESSING

print("\n========== DATA PREPROCESSING ==========")

df = pd.read_csv("ML/uber_fair_prediction/uber.csv")

print("Original Dataset Shape:", df.shape)

# Remove unnecessary columns
df = df.drop(columns=['Unnamed: 0', 'key'])

# Remove missing values
df = df.dropna()

# Convert datetime
df['pickup_datetime'] = pd.to_datetime(
    df['pickup_datetime'], utc=True, errors='coerce'
)
df = df.dropna(subset=['pickup_datetime'])

# Extract date and time features
df['year'] = df['pickup_datetime'].dt.year
df['month'] = df['pickup_datetime'].dt.month
df['day'] = df['pickup_datetime'].dt.day
df['hour'] = df['pickup_datetime'].dt.hour
df['day_of_week'] = df['pickup_datetime'].dt.day_of_week

df = df.drop(columns=['pickup_datetime'])

# Calculate geographical distance
def haversine_distance(lat1, lon1, lat2, lon2):

    R = 6371

    lat1, lon1, lat2, lon2 = map(
        np.radians, [lat1, lon1, lat2, lon2]
    )

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        np.sin(dlat / 2)**2
        + np.cos(lat1) * np.cos(lat2)
        * np.sin(dlon / 2)**2
    )

    return 2 * R * np.arcsin(np.sqrt(a))


df['distance_km'] = haversine_distance(
    df['pickup_latitude'],
    df['pickup_longitude'],
    df['dropoff_latitude'],
    df['dropoff_longitude']
)

# Remove invalid geographical coordinates
df = df[
    df['pickup_latitude'].between(-90, 90) &
    df['dropoff_latitude'].between(-90, 90) &
    df['pickup_longitude'].between(-180, 180) &
    df['dropoff_longitude'].between(-180, 180)
]

# Remove invalid fare, passenger and distance values
df = df[
    (df['fare_amount'] > 0) &
    (df['passenger_count'] >= 1) &
    (df['passenger_count'] <= 6) &
    (df['distance_km'] > 0) &
    (df['distance_km'] <= 100)
]

print("Dataset Shape After Preprocessing:", df.shape)

# 2. OUTLIER DETECTION USING IQR

print("\n========== OUTLIER DETECTION ==========")

Q1 = df['fare_amount'].quantile(0.25)
Q3 = df['fare_amount'].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

outliers = df[
    (df['fare_amount'] < lower_limit) |
    (df['fare_amount'] > upper_limit)
]

print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower Limit:", lower_limit)
print("Upper Limit:", upper_limit)
print("Number of Outliers:", len(outliers))

# Remove fare outliers
df = df[
    df['fare_amount'].between(lower_limit, upper_limit)
]

print("Dataset Shape After Outlier Removal:", df.shape)

# 3. CORRELATION ANALYSIS

print("\n========== CORRELATION ANALYSIS ==========")

correlation = df.corr(numeric_only=True)

print("\nCorrelation with Fare Amount:")
print(correlation['fare_amount'].sort_values(ascending=False))

# Save correlation heatmap
plt.figure(figsize=(12, 8))

sns.heatmap(
    correlation,
    annot=True,
    cmap='coolwarm',
    fmt='.2f'
)

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("correlation_heatmap.png")
plt.close()

print("Correlation heatmap saved successfully!")

# 4. MODEL TRAINING

print("\n========== MODEL TRAINING ==========")

X = df.drop(columns=['fare_amount'])
y = df['fare_amount']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Training Records:", len(X_train))
print("Testing Records:", len(X_test))

# Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

lr_predictions = lr_model.predict(X_test)

print("Linear Regression Training Completed!")

# Random Forest Regression
rf_model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train, y_train)

rf_predictions = rf_model.predict(X_test)

print("Random Forest Regression Training Completed!")

# 5. MODEL EVALUATION

print("\n========== MODEL EVALUATION ==========")

def evaluate_model(name, actual, predicted):

    mae = mean_absolute_error(actual, predicted)

    mse = mean_squared_error(actual, predicted)

    rmse = np.sqrt(mse)

    r2 = r2_score(actual, predicted)

    return {
        'Model': name,
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2 Score': r2
    }


results = []

results.append(
    evaluate_model("Linear Regression", y_test, lr_predictions)
)

results.append(
    evaluate_model("Random Forest", y_test, rf_predictions)
)

results_df = pd.DataFrame(results)

print("\nMODEL COMPARISON:")
print(results_df.to_string(index=False))

# 6. SAMPLE PREDICTION

print("\n========== SAMPLE FARE PREDICTION ==========")

sample_ride = X_test.iloc[[0]]

predicted_fare = rf_model.predict(sample_ride)

print("Predicted Uber Fare: $", round(predicted_fare[0], 2))
print("Actual Uber Fare: $", round(y_test.iloc[0], 2))


# Save actual vs predicted graph
plt.figure(figsize=(8, 5))

plt.scatter(y_test, rf_predictions, alpha=0.3)

plt.xlabel("Actual Fare")
plt.ylabel("Predicted Fare")

plt.title("Actual vs Predicted Uber Fare")

plt.tight_layout()
plt.savefig("actual_vs_predicted.png")
plt.close()


