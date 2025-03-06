import pickle
import numpy as np
import pandas as pd
from flask import Flask, render_template, request
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("accident.csv").dropna()

label_encoders = {}
for col in ["Gender", "Helmet_Used", "Seatbelt_Used"]:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

X = df.drop(columns=["Survived"])
y = df["Survived"]

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(label_encoders, open("encoders.pkl", "wb"))

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    if request.method == "POST":
        try:
            age = int(request.form["age"])
            gender = request.form["gender"]
            speed = float(request.form["speed"])
            helmet = request.form["helmet"]
            seatbelt = request.form["seatbelt"]

            model = pickle.load(open("model.pkl", "rb"))
            encoders = pickle.load(open("encoders.pkl", "rb"))

            gender_encoded = encoders["Gender"].transform([gender])[0]
            helmet_encoded = encoders["Helmet_Used"].transform([helmet])[0]
            seatbelt_encoded = encoders["Seatbelt_Used"].transform([seatbelt])[0]

            input_data = pd.DataFrame([[
                age, gender_encoded, speed, helmet_encoded, seatbelt_encoded
            ]], columns=["Age", "Gender", "Speed_of_Impact", "Helmet_Used", "Seatbelt_Used"])

            prediction = model.predict(input_data)[0]
            prediction = "Survived" if prediction == 1 else "Did not survive"

        except Exception as e:
            prediction = f"Error: {e}"

    return render_template("index.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)
