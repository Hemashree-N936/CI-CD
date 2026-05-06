import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load datasets
cve_df = pd.read_csv("cve_data.csv")
commits_df = pd.read_csv("commit_history.csv")

# --- Text Normalization ---
stop_words = set(stopwords.words("english"))

def clean_text(text):
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)  # keep only letters
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stop_words]
    return " ".join(tokens)

commits_df["CleanMessage"] = commits_df["Message"].apply(clean_text)
cve_df["CleanDescription"] = cve_df["Description"].apply(clean_text)

# --- Feature Engineering Basics ---
# Example: commit churn (lines added/deleted)
if "FilesChanged" in commits_df.columns:
    commits_df["Churn"] = commits_df["FilesChanged"].apply(lambda x: len(str(x).split(",")))

# Merge CVE + commits (simple keyword match on CVE IDs in commit messages)
merged = commits_df.merge(
    cve_df,
    left_on="Message",
    right_on="CVE_ID",
    how="left"
)

# Save cleaned dataset
merged.to_csv("clean_dataset.csv", index=False)
print(f"✅ Clean dataset saved with {len(merged)} rows")
