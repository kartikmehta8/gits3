import os
import requests
import base64

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

def download_file(repo_name, file_name, download_path):
    token = load_github_token()
    headers = {"Authorization": f"token {token}"}
    url = get_repo_url(repo_name) + f"/contents/{file_name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        content = base64.b64decode(response.json()["content"])
        with open(download_path, "wb") as file:
            file.write(content)
        print(f"File {file_name} downloaded successfully to {download_path}.")
    else:
        print(f"Error downloading file: {response.json()}")
