import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

# Load model
model = joblib.load("commit_classifier.pkl")

# Fit vectorizer on existing dataset
df = pd.read_csv("clean_dataset.csv")
vectorizer = TfidfVectorizer(max_features=500)
vectorizer.fit(df["CleanMessage"].fillna(""))

def predict_severity(message, churn=0):
    X_text = vectorizer.transform([message])
    X = np.hstack([X_text.toarray(), np.array([[churn]])])
    pred = model.predict(X)[0]
    return "High" if pred == 1 else "Low"

# Example usage
print(predict_severity("Fix buffer overflow in parser", churn=3))
