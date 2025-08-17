#!/usr/bin/env python3
"""
Setup script for GPT-Tokenizer package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gpt-tokenizer",
    version="1.0.0",
    author="GPT-Tokenizer Contributors",
    author_email="",
    description="A comprehensive implementation of tokenization algorithms used in Large Language Models",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/DeconvFFT/GPT-tokenizer",
    project_urls={
        "Bug Reports": "https://github.com/DeconvFFT/GPT-tokenizer/issues",
        "Source": "https://github.com/DeconvFFT/GPT-tokenizer",
        "Documentation": "https://gpt-tokenizer.readthedocs.io/",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "sphinx-autodoc-typehints>=1.12",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
            "sphinx-autodoc-typehints>=1.12",
            "myst-parser>=0.15",
        ],
        "notebook": [
            "jupyter>=1.0",
            "ipykernel>=6.0",
            "matplotlib>=3.3",
            "pandas>=1.3",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.rst"],
    },
    entry_points={
        "console_scripts": [
            "gpt-tokenizer=gpt_tokenizer.cli:main",
        ],
    },
    keywords="tokenizer, bpe, gpt, nlp, machine learning, ai",
    zip_safe=False,
)
