import os


def create_file(filepath, content):
    """
    Utility to create a file with the specified content.
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)
    print(f"Generated: {filepath}")


def create_project_structure(base_dir):
    """
    Create the CLI tool structure with all necessary files.
    """
    # Define package structure and files
    package_dir = os.path.join(base_dir, "cloud_function_framework")
    tests_dir = os.path.join(base_dir, "tests")

    files = {
        # CLI Entry Point
        os.path.join(package_dir, "cli.py"): """\
import click
from cloud_function_framework.project_setup import setup_project


@click.group()
def cli():
    \"\"\"CLI Tool for Google Cloud Function Setup.\"\"\"
    pass


@cli.command()
@click.argument("project_name")
def bootstrap(project_name):
    \"\"\"Initialize a new project structure.\"\"\"
    click.echo(f"Initializing project: {project_name}")
    setup_project(project_name)


if __name__ == "__main__":
    cli()
""",
        # Project Setup Logic
        os.path.join(package_dir, "project_setup.py"): """\
import os
from cloud_function_framework.helpers import create_project_structure, generate_requirements, generate_scripts


def setup_project(project_name):
    \"\"\"Set up the project structure and generate necessary files.\"\"\"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(current_dir, "..", project_name)

    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
        print(f"Directory '{project_name}' created.")
    else:
        print(f"Directory '{project_name}' already exists.")

    create_project_structure(project_dir)
    generate_requirements(project_dir)
    generate_scripts(project_dir)
    print(f"Project setup complete. Navigate to '{project_dir}' to start working.")
""",
        # Helper Functions
        os.path.join(package_dir, "helpers.py"): """\
import os

def create_project_structure(project_dir):
    \"\"\"Create the simplified project structure with necessary files.\"\"\"
    files = {
        "main.py": \"\"\"\
import logging
from service import handle_request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hello_world(request):
    logger.info("Received a request")
    return handle_request(request)
\"\"\",
        "service.py": \"\"\"\
def handle_request(request):
    method = request.method
    name = request.args.get("name", "World")
    if method == "GET":
        return f"Hello, {name}!", 200
    else:
        return "Method not allowed", 405
\"\"\"
    }

    scripts_dir = os.path.join(project_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    for filename, content in files.items():
        file_path = os.path.join(project_dir, filename)
        with open(file_path, "w") as f:
            f.write(content)
    print(f"Project structure created at {project_dir}.")


def generate_requirements(project_dir):
    \"\"\"Generate a requirements.txt file for the project.\"\"\"
    requirements_path = os.path.join(project_dir, "requirements.txt")
    if not os.path.exists(requirements_path):
        with open(requirements_path, "w") as f:
            f.write("flask")
        print(f"requirements.txt generated at {requirements_path}.")
    else:
        print(f"requirements.txt already exists at {requirements_path}.")


def generate_scripts(project_dir):
    \"\"\"Generate test_local.py and deploy_to_gcp.py in the scripts directory.\"\"\"
    scripts_dir = os.path.join(project_dir, "scripts")
    os.makedirs(scripts_dir, exist_ok=True)

    # Generate test_local.py
    test_local_content = \"\"\"\
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
\"\"\"
    test_local_path = os.path.join(scripts_dir, "test_local.py")
    if not os.path.exists(test_local_path):
        with open(test_local_path, "w") as f:
            f.write(test_local_content)

    # Generate deploy_to_gcp.py
    deploy_to_gcp_content = \"\"\"\
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
\"\"\"
    deploy_to_gcp_path = os.path.join(scripts_dir, "deploy_to_gcp.py")
    if not os.path.exists(deploy_to_gcp_path):
        with open(deploy_to_gcp_path, "w") as f:
            f.write(deploy_to_gcp_content)

    print(f"Scripts generated in {scripts_dir}.")
""",
        # Setup Script
        os.path.join(base_dir, "setup.py"): """\
from setuptools import setup, find_packages

setup(
    name="cloud-function-framework",
    version="0.1.0",
    author="Your Name",
    author_email="your_email@example.com",
    description="A CLI tool to bootstrap Google Cloud Functions projects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/cloud-function-framework",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0.0",
        "flask>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cloud-function-framework=cloud_function_framework.cli:cli",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
"""
    }

    # Create all files
    for path, content in files.items():
        create_file(path, content)

    print(f"CLI tool structure generated at {base_dir}.")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(script_dir, "cloud_function_framework_tool")

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"Directory '{base_dir}' created.")

    create_project_structure(base_dir)

    print("CLI tool setup complete. Navigate to the directory and install the tool:")
    print(f"  cd {base_dir}")
    print("  pip install -e .")
