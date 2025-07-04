#!/usr/bin/env python3
"""
Setup script for Invoice Automation System
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "Invoice Automation System for extracting structured data from PDF invoices."

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="invoice-automation",
    version="1.0.0",
    author="Invoice Automation Team",
    author_email="support@invoice-automation.com",
    description="A comprehensive system for automating the extraction of structured data from PDF invoices",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/invoice-automation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Filters",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "invoice-parser=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="invoice pdf extraction automation parsing data",
    project_urls={
        "Bug Reports": "https://github.com/your-username/invoice-automation/issues",
        "Source": "https://github.com/your-username/invoice-automation",
        "Documentation": "https://github.com/your-username/invoice-automation#readme",
    },
) 