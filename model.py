from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import pandas as pd


df= pd.read_csv("accident.csv")
# Drop rows with missing target values if any
df = df.dropna(subset=["Survived"])

# Fill missing values for Speed_of_Impact with the median
imputer = SimpleImputer(strategy="median")
df["Speed_of_Impact"] = imputer.fit_transform(df[["Speed_of_Impact"]])

# Fill missing value in Gender with the most frequent value
df.loc[:, "Gender"] = df["Gender"].fillna(df["Gender"].mode()[0])


# Encode categorical variables
label_encoders = {}
for col in ["Gender", "Helmet_Used", "Seatbelt_Used"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Split dataset
X = df.drop(columns=["Survived"])
y = df["Survived"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("Model for accident prediction trained with accuracy",accuracy)
