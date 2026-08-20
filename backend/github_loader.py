import os
import requests
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()

# Get GitHub token from .env
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# Repository information
OWNER = "fastapi"
REPO = "fastapi"
BRANCH = "master"


# File types that we want for our RAG
ALLOWED_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".js",
    ".ts",
    ".jsx",
    ".tsx"
}


# Folders that we don't need
IGNORED_FOLDERS = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
    ".venv",
    "img",
    "tests"
}

def get_repository_tree(owner, repo, branch):

    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}"

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    params = {
        "recursive": "1"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        raise Exception(
            f"GitHub API error: {response.status_code}\n"
            f"{response.text}"
        )

    return response.json()


def is_allowed_file(path):

    # Split path into folders/files
    parts = path.split("/")

    # Check if path contains an ignored folder
    for folder in IGNORED_FOLDERS:

        if folder in parts:
            return False

    # Check file extension
    for extension in ALLOWED_EXTENSIONS:

        if path.endswith(extension):
            return True

    return False


def get_useful_files(tree):

    files = []

    for item in tree["tree"]:

        # blob means file
        if item["type"] != "blob":
            continue

        path = item["path"]

        if is_allowed_file(path):
            files.append(item)

    return files


if __name__ == "__main__":

    # Make sure token exists
    if not GITHUB_TOKEN:

        raise Exception(
            "GITHUB_TOKEN was not found. "
            "Make sure you created a .env file "
            "and added GITHUB_TOKEN=your_token"
        )


    print("Connecting to GitHub...")


    # Get complete repository tree
    tree = get_repository_tree(
        OWNER,
        REPO,
        BRANCH
    )


    # Filter useful files
    files = get_useful_files(tree)


    print("\n============================")
    print(f"Total useful files: {len(files)}")
    print("============================\n")


    # Display files
    for file in files:

        print(file["path"])