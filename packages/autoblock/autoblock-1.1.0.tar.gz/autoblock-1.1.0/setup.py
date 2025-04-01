from setuptools import setup, find_packages
import os

# Read long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="autoblock",
    version="1.1.0",
    packages=find_packages(include=["autoblock", "autoblock.*"]),  # Ensure `autoblock` package detected
    description="Auto password changer for Django projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Parth",
    author_email="parth@kanhasoft.com",
    url="https://github.com/parth-kanhasoft/autoblock",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
    ],
    install_requires=[
        "Django>=4.0",
    ],
    python_requires=">=3.10",
)
