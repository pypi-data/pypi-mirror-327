from setuptools import setup, find_packages

setup(
    name="dep-manager-cli",
    version="0.1.1",
    packages=find_packages(),
    install_requires=["typer[all]", "rich", "requests", "tqdm"],
    entry_points={
        "console_scripts": [
            "dep-manager=dep_manager.cli:app",  
        ],
    },
)
