import os

TOKEN_FILE = "github_token.txt"

def load_github_token():
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError("GitHub token file not found. Please set your token using the 'token' command.")
    with open(TOKEN_FILE, "r") as file:
        return file.read().strip()

def save_github_token(token):
    with open(TOKEN_FILE, "w") as file:
        file.write(token)

def get_repo_url(repo_name):
    user = os.getenv("GITHUB_USER")
    if not user:
        raise EnvironmentError("GITHUB_USER environment variable not set.")
    return f"https://api.github.com/repos/{user}/{repo_name}"
