from setuptools import setup, find_packages

setup(
    name="mlflow-init",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mlflow-init=mlflow_init.cli:main',
        ],
    },
    author="SHARATH VN",
    description="MLflow project scaffolding CLI tool",
    install_requires=[],
    python_requires=">=3.6",
)
