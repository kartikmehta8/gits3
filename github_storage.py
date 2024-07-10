import argparse
import requests
import os
import base64

from utils import load_github_token, save_github_token, get_repo_url

def create_repo(repo_name):
    token = load_github_token()
    headers = {"Authorization": f"token {token}"}
    data = {"name": repo_name, "private": False}
    response = requests.post('https://api.github.com/user/repos', json=data, headers=headers)
    if response.status_code == 201:
        print(f"Repository {repo_name} created successfully.")
    else:
        print(f"Error creating repository: {response.json()}")

def add_file(repo_name, file_path):
    token = load_github_token()
    headers = {"Authorization": f"token {token}"}
    with open(file_path, "rb") as file:
        content = base64.b64encode(file.read()).decode("utf-8")
    filename = os.path.basename(file_path)
    url = get_repo_url(repo_name) + f"/contents/{filename}"
    data = {"message": "add file", "content": content}
    response = requests.put(url, json=data, headers=headers)
    if response.status_code == 201:
        print(f"File {filename} added successfully to {repo_name}.")
    else:
        print(f"Error adding file: {response.json()}")

def remove_file(repo_name, file_name):
    token = load_github_token()
    headers = {"Authorization": f"token {token}"}
    url = get_repo_url(repo_name) + f"/contents/{file_name}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json()["sha"]
        data = {"message": "delete file", "sha": sha}
        response = requests.delete(url, json=data, headers=headers)
        if response.status_code == 200:
            print(f"File {file_name} removed successfully from {repo_name}.")
        else:
            print(f"Error removing file: {response.json()}")
    else:
        print(f"Error finding file: {response.json()}")

def list_files(repo_name):
    token = load_github_token()
    headers = {"Authorization": f"token {token}"}
    url = get_repo_url(repo_name) + "/contents"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        files = response.json()
        for file in files:
            print(file["name"])
    else:
        print(f"Error listing files: {response.json()}")

def set_token(token):
    save_github_token(token)
    print("GitHub token saved successfully.")

def main():
    parser = argparse.ArgumentParser(description='GitHub Storage CLI')
    subparsers = parser.add_subparsers(dest='command')

    parser_create = subparsers.add_parser('create', help='Create a new repository')
    parser_create.add_argument('repo_name', type=str, help='Name of the repository')

    parser_add = subparsers.add_parser('add', help='Add a file to a repository')
    parser_add.add_argument('repo_name', type=str)
    parser_add.add_argument('file_path', type=str)

    parser_remove = subparsers.add_parser('remove', help='Remove a file from a repository')
    parser_remove.add_argument('repo_name', type=str)
    parser_remove.add_argument('file_name', type=str)

    parser_list = subparsers.add_parser('list', help='List files in a repository')
    parser_list.add_argument('repo_name', type=str)

    parser_token = subparsers.add_parser('token', help='Set GitHub token')
    parser_token.add_argument('token', type=str)

    args = parser.parse_args()

    if args.command == 'create':
        create_repo(args.repo_name)
    elif args.command == 'add':
        add_file(args.repo_name, args.file_path)
    elif args.command == 'remove':
        remove_file(args.repo_name, args.file_name)
    elif args.command == 'list':
        list_files(args.repo_name)
    elif args.command == 'token':
        set_token(args.token)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
