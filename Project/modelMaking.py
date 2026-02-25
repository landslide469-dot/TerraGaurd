import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load data
data = pd.read_csv('100_dataset.csv')
data = data.dropna()

# Features
features = ['humidity', 'rainfall_24hr', 'rainfall_3days', 'soil_moisture', 'elevation']


X = data[features]
y = data['typeof_disaster']

# Split
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model (balanced for multi-class)
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight='balanced',
    verbose=1
)

model.fit(x_train, y_train)

# Accuracy
predictions = model.predict(x_test)
accuracy = accuracy_score(y_test, predictions)

print("Model Accuracy:", accuracy)

# -------- USER INPUT --------

print("\nEnter New Data For Prediction")

humidity = float(input("Humidity: "))
rainfall_24hr = float(input("Rainfall (24hr): "))
rainfall_3days = float(input("Rainfall (3 days): "))
soil_moisture = float(input("Soil Moisture: "))
elevation = float(input("Elevation: "))

user_data = pd.DataFrame(
    [[humidity, rainfall_24hr, rainfall_3days, soil_moisture, elevation]],
    columns=features
)

prediction = model.predict(user_data)[0]
probabilities = model.predict_proba(user_data)[0]

print("\nPredicted Disaster Type:", prediction)

print("\nClass Probabilities:")
for cls, prob in zip(model.classes_, probabilities):
    print(f"{cls}: {round(prob*100,2)}%")
    
sts = joblib.dump(model,"terraModel.pkl")

if sts:
    print("Model Saved !")    
    