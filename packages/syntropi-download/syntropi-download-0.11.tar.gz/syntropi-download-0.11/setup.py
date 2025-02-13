from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="syntropi-download",
    version="0.11",
    py_modules=["cli.cli"],
    install_requires=[
        "click",
        "requests",
        "python-dotenv"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "syntropi-download=cli.cli:cli"
        ]
    },
)
