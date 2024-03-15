import sys


def update_project_excutable():
    python_executable = sys.executable
    project_path = python_executable.split("venv/bin/python")[0]
    sys.path.insert(0, project_path)
