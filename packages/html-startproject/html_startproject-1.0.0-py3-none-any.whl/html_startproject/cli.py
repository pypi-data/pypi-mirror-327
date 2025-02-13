import os
import shutil
import argparse
from pathlib import Path
import pkgutil

def create_project(project_name):
    try:
        # Create root directory
        project_path = Path(project_name)
        project_path.mkdir(exist_ok=False)
        
        # Create files directory structure
        files_dir = project_path / 'files'
        (files_dir / 'images').mkdir(parents=True)
        (files_dir / 'fonts').mkdir()
        (files_dir / 'video').mkdir()

        # Get template content
        template_data = pkgutil.get_data(__name__, 'templates/base/index.html')
        css_data = pkgutil.get_data(__name__, 'templates/base/style.css')
        
        # Create index.html with project name
        index_content = template_data.decode().replace('{{ project_name }}', project_name)
        (project_path / 'index.html').write_text(index_content)
        
        # Create style.css
        (project_path / 'style.css').write_text(css_data.decode())
        
        print(f"Successfully created project: {project_name}")
        print(f"Directory structure:\n"
              f"{project_name}/\n"
              f"├── files/\n"
              f"│   ├── images/\n"
              f"│   ├── fonts/\n"
              f"│   └── video/\n"
              f"├── index.html\n"
              f"└── style.css")

    except FileExistsError:
        print(f"Error: Directory '{project_name}' already exists!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Create a new HTML project with Bootstrap")
    parser.add_argument("project_name", help="Name of your project")
    args = parser.parse_args()
    create_project(args.project_name)