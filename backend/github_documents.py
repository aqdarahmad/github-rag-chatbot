import os
import requests
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


# ==========================================
# Repository information
# ==========================================

OWNER = "fastapi"
REPO = "fastapi"
BRANCH = "master"


# ==========================================
# Allowed file extensions
# ==========================================

ALLOWED_EXTENSIONS = {
    ".py",
    ".md",
    ".txt",
    ".js",
    ".ts",
    ".jsx",
    ".tsx"
}


# ==========================================
# Folders we don't need
# ==========================================

IGNORED_FOLDERS = {
    ".git",
    ".github",
    "node_modules",
    "__pycache__",
    ".venv",
    "img",
    "tests",
    "scripts"
}


# ==========================================
# Get repository tree from GitHub
# ==========================================

def get_repository_tree(owner, repo, branch):

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/git/trees/{branch}"
    )

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


# ==========================================
# Check if file should be included
# ==========================================

def is_allowed_file(path):

    parts = path.split("/")

    # Ignore unwanted folders
    for folder in IGNORED_FOLDERS:

        if folder in parts:
            return False

    # Only keep English documentation
    if path.startswith("docs/"):

        if not path.startswith("docs/en/"):
            return False

    # README
    if path == "README.md":
        return True

    # Check extension
    for extension in ALLOWED_EXTENSIONS:

        if path.endswith(extension):
            return True

    return False


# ==========================================
# Get useful files
# ==========================================

def get_useful_files(tree):

    files = []

    for item in tree["tree"]:

        # We only want files, not folders
        if item["type"] != "blob":
            continue

        path = item["path"]

        if is_allowed_file(path):

            files.append(item)

    return files


# ==========================================
# Download file content
# ==========================================

def get_file_content(download_url):

    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.raw+json"
    }

    response = requests.get(
        download_url,
        headers=headers,
        timeout=30
    )

    if response.status_code != 200:

        print(
            f"Could not download file: {download_url}"
        )

        return None

    return response.text


# ==========================================
# Main
# ==========================================

if __name__ == "__main__":

    # Check GitHub token
    if not GITHUB_TOKEN:

        raise Exception(
            "GITHUB_TOKEN was not found. "
            "Check your .env file."
        )


    print("Connecting to GitHub...")


    # --------------------------------------
    # Get repository tree
    # --------------------------------------

    tree = get_repository_tree(
        OWNER,
        REPO,
        BRANCH
    )


    # --------------------------------------
    # Get all useful files
    # --------------------------------------

    files = get_useful_files(tree)


    print(
        f"\nFound {len(files)} useful files.\n"
    )


    # ======================================
    # Files for our first RAG experiment
    # ======================================

    selected_paths = {

        "README.md",

        "fastapi/applications.py",
        "fastapi/routing.py",
        "fastapi/params.py",
        "fastapi/dependencies/utils.py",

        "docs/en/docs/about/index.md",
        "docs/en/docs/tutorial/first-steps.md",
        "docs/en/docs/tutorial/path-params.md",
        "docs/en/docs/tutorial/query-params.md",
        "docs/en/docs/tutorial/body.md",
        "docs/en/docs/tutorial/security/first-steps.md"
    }


    # Select only those files
    selected_files = [
        file
        for file in files
        if file["path"] in selected_paths
    ]


    print(
        f"Selected files: {len(selected_files)}\n"
    )


    # ======================================
    # Create data directory
    # ======================================

    data_directory = "../data"

    os.makedirs(
        data_directory,
        exist_ok=True
    )


    # ======================================
    # Download selected files
    # ======================================

    downloaded = 0


    for file in selected_files:

        path = file["path"]

        print(
            f"Downloading: {path}"
        )


        # Download content
        content = get_file_content(
            file["url"]
        )


        if content is None:

            continue


        # Create local path
        local_path = os.path.join(
            data_directory,
            path
        )


        # Create parent directories
        parent_directory = os.path.dirname(
            local_path
        )

        os.makedirs(
            parent_directory,
            exist_ok=True
        )


        # Save file
        with open(
            local_path,
            "w",
            encoding="utf-8"
        ) as output_file:

            output_file.write(content)


        downloaded += 1


    # ======================================
    # Final result
    # ======================================

    print("\n==============================")
    print(
        f"Downloaded files: {downloaded}"
    )
    print("==============================")