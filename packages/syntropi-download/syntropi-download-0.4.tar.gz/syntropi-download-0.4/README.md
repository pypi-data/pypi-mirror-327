# SYNTROPI CLI

## Overview
SYNTROPI CLI is a command-line tool that allows users to interact with the SYNTROPI API for downloading data.

## Installation
To install SYNTROPI CLI, follow these steps:

### Prerequisites
- Ensure you have Python 3 installed.

### Install the Package
```
pip install syntropi-cli
```

### Configuration
Before using SYNTROPI CLI, you must configure your API credentials.

#### Set Environment Variables
Run the following command to set up your secret key
```
syntropi-download set-env SYNTROPI_SECRET_KEY your_secret_key
```

### Usage
To see available commands, run:
```
syntropi-download --help
```

#### Download Data
```
syntropi download --destination-folder /path/to/folder --threads number_of_threads
```

Options:
* --destination-folder: Directory to save the downloaded files (default: current directory).
* --threads: Number of threads to use for downloading (default: 4).

### Logging
Logs are stored in /var/logs/syntropi-download/downloads.log by default, but can be changed via LOG_DIR in the .env file

### Troubleshooting
* Ensure SYNTROPI_SECRET_KEY and SYNTROPI_API_URL are set before running commands.
* Use source .env if environment variables are not loading.
* Check /var/logs/syntropi-download/downloads.log for error messages.
