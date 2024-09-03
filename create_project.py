import os
import shutil
import subprocess
import json
import venv

def create_project(project_name):
    base_path = os.path.dirname(os.path.abspath(__file__))  # Gets the SoloDevJourney directory
    template_path = os.path.join(base_path, "ProjectTemplate")
    project_path = os.path.join(base_path, project_name)

    # Copy template to new project directory
    shutil.copytree(template_path, project_path)

    # Update VS Code workspace file
    workspace_file = os.path.join(project_path, "project.code-workspace")
    with open(workspace_file, 'r') as f:
        workspace_data = json.load(f)
    
    workspace_data["folders"][0]["name"] = project_name
    
    with open(workspace_file, 'w') as f:
        json.dump(workspace_data, f, indent=4)

    # Update README.md
    readme_path = os.path.join(project_path, "README.md")
    with open(readme_path, 'r') as f:
        readme_content = f.read()
    
    readme_content = readme_content.replace("Project Name", project_name)
    readme_content = readme_content.replace("project-name", project_name.lower())
    
    with open(readme_path, 'w') as f:
        f.write(readme_content)

    # Create virtual environment
    venv.create(os.path.join(project_path, '.venv'), with_pip=True)

    # Install dependencies
    venv_python = os.path.join(project_path, '.venv', 'Scripts', 'python')
    subprocess.run([venv_python, '-m', 'pip', 'install', '-r', 'requirements.txt'], cwd=project_path)
    subprocess.run([venv_python, '-m', 'pip', 'install', '-r', 'requirements-dev.txt'], cwd=project_path)

    # Initialize git repository
    subprocess.run(["git", "init"], cwd=project_path)

    # Create initial commit
    subprocess.run(["git", "add", "."], cwd=project_path)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=project_path)

    print(f"Project {project_name} created at {project_path}")
    print(f"To open in VS Code, run: code {os.path.join(project_path, 'project.code-workspace')}")
    print("Virtual environment and dependencies set up")
    print("Use 'invoke' to run tasks: test, lint, format, check, run")

if __name__ == "__main__":
    project_name = input("Enter project name: ")
    create_project(project_name)