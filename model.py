import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load dataset
file = pd.read_csv('data_set.csv')   # Make sure path is correct

# Convert YES/NO to 1/0
file['landslide'] = file['landslide'].map({'YES': 1, 'NO': 0})

# Features and Target
X = file[['temp', 'humidity']]
y = file['landslide']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create model
model = LogisticRegression()

# Train model
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
print("Accuracy:", accuracy_score(y_test, y_pred))


new_data = [[19,100,100,100,100,]]
  # temp, humidity
prediction = model.predict(new_data)

if prediction[0] == 1:
    print("Landslide: YES")
else:
    print("Landslide: NO")



