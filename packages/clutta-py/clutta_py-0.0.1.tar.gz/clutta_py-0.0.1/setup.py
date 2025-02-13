from setuptools import setup, find_packages

setup(
    name="clutta-py",
    version="0.0.1",
    description="Clutta-py is the official Python SDK for interacting with Clutta, a platform for observability and monitoring.",
    author="Sefas Technologies",
    author_email="support@clutta.io",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "python-dotenv",
        "urllib3"
    ]
)
