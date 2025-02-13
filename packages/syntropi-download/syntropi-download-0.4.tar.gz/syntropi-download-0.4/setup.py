from setuptools import setup, find_packages

setup(
    name="syntropi-download",
    version="0.4",
    py_modules=["cli.cli"],
    install_requires=[
        "click",
        "requests",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "syntropi-download=cli.cli:cli"
        ]
    },
)
