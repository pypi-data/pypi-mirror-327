from setuptools import setup, find_packages

setup(
    name="autoblock",
    version="1.0.0",  # Version number
    packages=find_packages(),
    description="Auto password changer for Django projects",
    long_description="This package changes user passwords and Django secret key on every request.",
    long_description_content_type="text/markdown",
    author="Parth",
    author_email="parth@kanhasoft.com",
    url="https://github.com/parth-kanhasoft/autoblock",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Django>4.0",
        "requests",
    ],
    python_requires=">=3.10",
)
