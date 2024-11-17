from setuptools import setup, find_packages

setup(
    name="cloud-function-framework",
    version="0.2.0",
    author="Mohamed Hammad & Mohamed Abulazm",
    author_email="hammad.mohamed1893@gmail.com",
    description="A CLI tool to bootstrap Google Cloud Functions projects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Lolo1883/cloud-function-framework.git",
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
