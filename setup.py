from __future__ import annotations

from pathlib import Path

from setuptools import find_packages, setup

ROOT = Path(__file__).parent
README_PATH = ROOT / "README.md"

setup(
    name="sqlalchemy-llm-agent",
    version="0.1.3",
    description="LLM-powered helper utilities for building SQLAlchemy agents.",
    long_description=README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else "LLM helpers for SQLAlchemy.",
    long_description_content_type="text/markdown",
    url="https://github.com/org/sqlalchemy-llm-agent",
    packages=find_packages(exclude=("tests", "tests.*", "examples", "examples.*")),
    include_package_data=True,
    python_requires=">=3.8",
    install_requires=[
        "langchain[openai]>=1.0.5",
        "sqlalchemy>=2.0.44",
    ],
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
