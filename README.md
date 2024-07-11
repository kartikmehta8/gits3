# GitHub Storage Tool

A CLI tool to use GitHub as storage.

## Commands

- `create <repo_name> [--private]`: Create a new repository (optionally private).
- `add <repo_name> <file_path>`: Add a file to a repository.
- `remove <repo_name> <file_name>`: Remove a file from a repository.
- `list <repo_name>`: List files in a repository.
- `download <repo_name> <file_name> <download_path>`: Download a file from a repository.
- `visibility <repo_name> (--private | --public)`: Set repository visibility.
- `token <token>`: Set GitHub token.

## Usage

1. Set your GitHub username as an environment variable:
   ```sh
   export GITHUB_USER=your_username
