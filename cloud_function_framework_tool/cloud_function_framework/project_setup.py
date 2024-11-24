import os
from cloud_function_framework.helpers import create_project_structure, generate_requirements, generate_scripts


def setup_project(project_name):
   """Set up the project structure and generate necessary files."""
   # Get the current working directory
   current_dir = os.getcwd()

   # Create the project directory inside the current working directory
   project_dir = os.path.join(current_dir, project_name)

   if not os.path.exists(project_dir):
      os.makedirs(project_dir)
      print(f"Directory '{project_name}' created at {project_dir}.")
   else:
      print(f"Directory '{project_name}' already exists at {project_dir}.")
 

   create_project_structure(project_dir)
   generate_requirements(project_dir)
   generate_scripts(project_dir)
   print(f"Project setup complete. Navigate to '{project_dir}' to start working.")
