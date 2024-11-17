import os


def create_project_structure(project_dir):
    """Create the simplified project structure with necessary files."""
    files = {
        "main.py": """\
import logging
from service import handle_request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hello_world(request):
    logger.info("Received a request")
    return handle_request(request)
""",
        "service.py": """\
def handle_request(request):
    method = request.method
    name = request.args.get("name", "World")
    if method == "GET":
        return f"Hello, {name}!", 200
    else:
        return "Method not allowed", 405
"""
    }

    # Create scripts directory
    scripts_dir = os.path.join(project_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    # Write main.py and service.py
    for filename, content in files.items():
        file_path = os.path.join(project_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
    print(f"Project structure created at {project_dir}.")


def generate_requirements(project_dir):
    """Generate a requirements.txt file for the project."""
    requirements_path = os.path.join(project_dir, "requirements.txt")
    if not os.path.exists(requirements_path):
        with open(requirements_path, "w") as f:
            f.write("flask\n")
        print(f"requirements.txt generated at {requirements_path}.")
    else:
        print(f"requirements.txt already exists at {requirements_path}.")


def generate_scripts(project_dir):
    """Generate test_local.py and deploy_to_gcp.py in the scripts directory."""
    scripts_dir = os.path.join(project_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    # Generate test_local.py
    test_local_content = """\
import os
import sys
from flask import Flask, request

# Dynamically add the project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, project_root)

from main import hello_world

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def local_test():
    \"\"\"Test the Cloud Function locally.\"\"\"
    response, status_code = hello_world(request)
    return response, status_code

if __name__ == "__main__":
    print("Starting local server for testing...")
    app.run(host="127.0.0.1", port=8080)
"""
    test_local_path = os.path.join(scripts_dir, "test_local.py")
    if not os.path.exists(test_local_path):
        with open(test_local_path, "w") as f:
            f.write(test_local_content)

    # Generate deploy_to_gcp.py
    deploy_to_gcp_content = """\
import os
import subprocess
import sys

def deploy_function(project_dir, function_name="hello_world", region="us-central1"):
    \"\"\"Deploy the Google Cloud Function using gcloud CLI.\"\"\"
    requirements_path = os.path.join(project_dir, "requirements.txt")
    if not os.path.exists(requirements_path):
        print("Error: requirements.txt not found.")
        sys.exit(1)

    main_path = os.path.join(project_dir, "main.py")
    if not os.path.exists(main_path):
        print(f"Error: main.py not found in {project_dir}.")
        sys.exit(1)

    cmd = [
        "gcloud",
        "functions",
        "deploy",
        function_name,
        "--runtime", "python310",
        "--trigger-http",
        "--allow-unauthenticated",
        "--region", region,
        "--source", project_dir,
        "--entry-point", "hello_world",
    ]

    print(f"Deploying function '{function_name}' from {project_dir}...")
    try:
        subprocess.run(cmd, check=True)
        print(f"Function '{function_name}' deployed successfully!")
    except subprocess.CalledProcessError as e:
        print("Error during deployment.")
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.abspath(os.path.join(script_dir, ".."))

    deploy_function(project_dir)
"""
    deploy_to_gcp_path = os.path.join(scripts_dir, "deploy_to_gcp.py")
    if not os.path.exists(deploy_to_gcp_path):
        with open(deploy_to_gcp_path, "w") as f:
            f.write(deploy_to_gcp_content)
        print(f"Created: {deploy_to_gcp_path}")
    else:
        print(f"Skipped (already exists): {deploy_to_gcp_path}")

    print(f"Scripts generated in {scripts_dir}.")


if __name__ == "__main__":
    project_directory = "my_project"
    os.makedirs(project_directory, exist_ok=True)
    create_project_structure(project_directory)
    generate_requirements(project_directory)
    generate_scripts(project_directory)
    print("Project setup complete.")
