import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Load cleaned dataset
df = pd.read_csv("clean_dataset.csv")

# --- Text Features (TF-IDF on commit messages) ---
vectorizer = TfidfVectorizer(max_features=500)
X_text = vectorizer.fit_transform(df["CleanMessage"].fillna(""))

# --- Numeric Features (example: churn) ---
numeric_features = df[["Churn"]].fillna(0).values

# --- Combine Features ---
X = np.hstack([X_text.toarray(), numeric_features])

# --- Labels (example: severity high/low) ---
# Temporary: assign random labels for testing

y = np.random.randint(0, 2, size=len(df))


# Save feature matrix and labels
np.save("X.npy", X)
np.save("y.npy", y)
print(f"✅ Feature matrix saved with shape {X.shape}")
