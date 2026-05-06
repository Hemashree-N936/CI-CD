from git import Repo
import pandas as pd
import os

def clone_or_open_repo(repo_url, local_path="repo"):
    """
    Clone the repo if not already present, otherwise open it.
    """
    if not os.path.exists(local_path):
        print(f"📥 Cloning {repo_url}...")
        repo = Repo.clone_from(repo_url, local_path)
    else:
        print(f"📂 Using existing repo at {local_path}")
        repo = Repo(local_path)
    return repo

def extract_commits(repo, max_count=100):
    """
    Extract commit metadata into a DataFrame.
    """
    commits = []
    for commit in repo.iter_commits('main', max_count=max_count):
        commits.append({
            "CommitHash": commit.hexsha,
            "Author": commit.author.name,
            "Date": commit.committed_datetime.isoformat(),
            "Message": commit.message.strip(),
            "FilesChanged": [diff.a_path for diff in commit.diff(commit.parents or [])]
        })
    return pd.DataFrame(commits)

def save_to_csv(df, filename="commit_history.csv"):
    """
    Save commit history to CSV.
    """
    df.to_csv(filename, index=False)
    print(f"✅ Saved {len(df)} commits to {filename}")

if __name__ == "__main__":
    repo_url = "https://github.com/psf/requests.git"

    repo = clone_or_open_repo(repo_url)
    df = extract_commits(repo, max_count=200)
    save_to_csv(df)
