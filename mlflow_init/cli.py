"""
Author : SHARATH VN

"""
import os
import sys

TOP_LEVEL_FILES = {
    "README.md": "# MLflow Project Template\n\nGenerated with mlflow-init.\n",
    "conda.yaml": "# Example conda environment\nname: mlflow-env\ndependencies:\n  - python=3.8\n  - pip\n  - pip:\n    - mlflow\n",
    "run.sh": "#!/bin/bash\n\nmlflow run . -P epochs=3 -P batch_size=64\n"
}

MLPROJECT_CONTENT = """\
name: mlflow-image-project

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      epochs: {type: int, default: 5}
      batch_size: {type: int, default: 32}
    command: >
      python src/train.py --epochs {epochs} --batch_size {batch_size}
"""

SRC_FILES = {
    "train.py": '''\
import argparse

def main(epochs, batch_size):
    print(f"Training model for {epochs} epochs with batch size {batch_size}")
    # Add your training code here

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch_size", type=int, default=32)
    args = parser.parse_args()
    main(args.epochs, args.batch_size)
''',
    "validation.py": "# src/validation.py - Add validation logic here\n",
    "deployment.py": "# src/deployment.py - Add deployment logic (Flask/FastAPI) here\n"
}

NOTEBOOK_FILES = {
    "train_and_log.ipynb": """{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# MLflow Training Notebook"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# Start coding here"
   ]
  }
 ],
 "metadata": {},
 "nbformat": 4,
 "nbformat_minor": 2
}"""
}

UTIL_FILES = {
    "__init__.py": "# utils/__init__.py - Add helper functions here\n"
}

EXTRA_DIRS = {
    "src/data": ["__init__.py"],
    "src/models": ["__init__.py"],
    "tests": [
        "__init__.py",
        "test_train.py",
        "test_validation.py",
        "test_deployment.py",
    ],
    "configs": ["default.yaml"],
    "scripts": ["download_data.sh"],
    "docker": ["Dockerfile", "k8s_deployment.yaml"],
}

def create_file(path, content=""):
    with open(path, "w") as f:
        f.write(content)
    if path.endswith(".sh"):
        os.chmod(path, 0o755)

def create_project(project_name):
    if os.path.exists(project_name):
        print(f"❌ Project '{project_name}' already exists.")
        sys.exit(1)

    print(f"🚀 Creating MLOps-ready MLflow project structure in: {project_name}")
    os.makedirs(project_name)

    # MLproject file
    create_file(os.path.join(project_name, "MLproject"), MLPROJECT_CONTENT)

    # Top-level files
    for filename, content in TOP_LEVEL_FILES.items():
        create_file(os.path.join(project_name, filename), content)

    # notebooks/
    notebooks_path = os.path.join(project_name, "notebooks")
    os.makedirs(notebooks_path)
    for filename, content in NOTEBOOK_FILES.items():
        create_file(os.path.join(notebooks_path, filename), content)

    # src/
    src_path = os.path.join(project_name, "src")
    os.makedirs(src_path)
    for filename, content in SRC_FILES.items():
        create_file(os.path.join(src_path, filename), content)

    # utils/
    utils_path = os.path.join(project_name, "utils")
    os.makedirs(utils_path)
    for filename, content in UTIL_FILES.items():
        create_file(os.path.join(utils_path, filename), content)

    # ml_models/
    ml_models_path = os.path.join(project_name, "ml_models")
    os.makedirs(ml_models_path)

    # extra dirs and files
    for dir_path, files in EXTRA_DIRS.items():
        full_dir_path = os.path.join(project_name, dir_path)
        os.makedirs(full_dir_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(full_dir_path, file)
            # Provide starter content for some files
            if file == "default.yaml":
                content = "# Default config file\nparameters:\n  learning_rate: 0.001\n  batch_size: 32\n"
            elif file == "download_data.sh":
                content = "#!/bin/bash\n# Script to download datasets\n\necho \"Downloading data...\"\n"
            elif file == "Dockerfile":
                content = (
                    "FROM python:3.8-slim\n"
                    "WORKDIR /app\n"
                    "COPY . /app\n"
                    "RUN pip install mlflow\n"
                    "CMD [\"mlflow\", \"run\", \".\"]\n"
                )
            elif file == "k8s_deployment.yaml":
                content = (
                    "apiVersion: apps/v1\n"
                    "kind: Deployment\n"
                    "metadata:\n"
                    "  name: mlflow-deployment\n"
                    "spec:\n"
                    "  replicas: 1\n"
                    "  selector:\n"
                    "    matchLabels:\n"
                    "      app: mlflow\n"
                    "  template:\n"
                    "    metadata:\n"
                    "      labels:\n"
                    "        app: mlflow\n"
                    "    spec:\n"
                    "      containers:\n"
                    "      - name: mlflow\n"
                    "        image: your-image:latest\n"
                    "        ports:\n"
                    "        - containerPort: 5000\n"
                )
            else:
                content = ""
            create_file(file_path, content)

    print(f"✅ MLOps-ready MLflow project '{project_name}' created successfully!")

def main():
    if len(sys.argv) != 2:
        print("❗ Usage: mlflow-init <project-name>")
        sys.exit(1)

    project_name = sys.argv[1]
    create_project(project_name)


if __name__ == "__main__":
    main()
