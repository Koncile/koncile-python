from setuptools import setup, find_packages

# Read the contents of README file
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="koncile",
    version="0.1.0",
    author="Koncile",
    author_email="support@koncile.ai",
    description="Official Python SDK for Koncile API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koncile/koncile-sdk",
    packages=find_packages(exclude=["examples*", "tests*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.25.0",
    ],
    project_urls={
        "Documentation": "https://docs.koncile.ai",
        "Source": "https://github.com/koncile/koncile-sdk",
        "Issue Tracker": "https://github.com/koncile/koncile-sdk/issues",
    },
)
