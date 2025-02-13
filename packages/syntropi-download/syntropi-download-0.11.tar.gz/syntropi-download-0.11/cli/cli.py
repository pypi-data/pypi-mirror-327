#!/usr/bin/env python3

import os
import logging
import click
import requests
import concurrent.futures
import threading
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

progress_lock = threading.Lock()

SECRET_KEY = os.getenv("SYNTROPI_SECRET_KEY")
API_URL = os.getenv("SYNTROPI_API_URL")

def get_headers():
    if not SECRET_KEY:
        click.echo("Error: SYNTROPI_SECRET_KEY is not set.", err=True)
        exit(1)
    return {"Authorization": f"Bearer {SECRET_KEY}"}

@click.group()
def cli():
    """SYNTROPI CLI - A tool to interact with the API."""
    pass

@click.command()
def test():
    """Test command."""
    click.echo("Command works!")
    
def set_env_command(key, value):
    env_file = ".env"
    env_lines = []
    
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            env_lines = f.readlines()

    key_exists = False

    for i, line in enumerate(env_lines):
        if line.startswith(f"{key}="):
            env_lines[i] = f"{key}={value}\n"
            key_exists = True
            break

    if not key_exists:
        env_lines.append(f"{key}={value}\n")

    with open(env_file, "w") as f:
        f.writelines(env_lines)

    load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))

    click.echo(f"Saved {key}={value} in .env file.")
    click.echo("To apply changes globally, restart your terminal or run 'source .env'.")

@click.command()
@click.argument("key")
@click.argument("value")
def set_env(key, value):
    """Set an environment variable persistently in the .env file."""
    set_env_command(key, value)

@click.command()
@click.argument("value")
def set_secret_key(value):
    """Set your secret key persistently in the .env file."""
    key = "SYNTROPI_SECRET_KEY"
    set_env_command(key, value)
    
@click.command()
@click.option("--destination-folder", default=os.getcwd(), show_default=True, help="Folder to download files to (default: current directory).")
@click.option("--threads", default=4, show_default=True, help="Number of threads to use for downloading (default: 4)")
def download(destination_folder, threads):
    """Fetch and download data from Syntropi."""
    SECRET_KEY = os.getenv("SYNTROPI_SECRET_KEY")
    API_URL = os.getenv("SYNTROPI_API_URL")

    if not SECRET_KEY:
        click.echo("Please add your secret key by running syntropi-download set-secret-key ")
        return
    
    click.echo("Start download")
    start_download(destination_folder, threads)
        
def progress_bar(iteration, total, bar_length=50):
    percent = "{0:.2f}".format(100 * (iteration / float(total)))
    filled_length = int(bar_length * iteration // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    
    click.echo(f'\rProgress: [{bar}] {percent}% Complete', nl=False, err=False)
    
    if iteration >= total:
        click.echo()


def download_video(video_object, destination_folder):
    try:
        video_signed_url = video_object.get('videoUrl')
        locations_signed_url = video_object.get('locationsUrl')
        metadata_signed_url = video_object.get('metadataUrl')

        video_folder = os.path.join(destination_folder, video_object.get('id'))
        os.makedirs(video_folder, exist_ok=True)

        download_file(video_signed_url, os.path.join(video_folder, video_object.get('id') + '.mp4'))
        download_file(locations_signed_url, os.path.join(video_folder, video_object.get('id') + '.json'))
        download_file(metadata_signed_url, os.path.join(video_folder, video_object.get('id') + '_metadata.json'))

        logging.info(f"Downloaded {video_object.get('id')}")
        return video_folder

    except Exception as e:
        logging.error(f"Error downloading {video_object.get('id')}: {e}")
        return f"Error downloading {video_object.get('id')}: {e}"


def download_file(url, destination_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get("content-length", 0))
        downloaded_size = 0

        with open(destination_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
                    downloaded_size += len(chunk)

        if downloaded_size < total_size:
            logging.error(f"Incomplete file: {downloaded_size}/{total_size} bytes downloaded.")
            raise Exception(f"Incomplete file: {downloaded_size}/{total_size} bytes downloaded.")

        return destination_path

    except Exception as e:
        logging.error(f"Error downloading {url}: {e}")
        return f"Error downloading {url}: {e}"


def start_download(destination_folder, threads):
    LOG_DIR = os.getenv("LOG_DIR", os.path.join(os.getcwd(), "logs"))
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)
    LOG_FILE = os.path.join(LOG_DIR, "downloads.log")

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)

    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    video_results = []
    limit = 1000
    offset = 0

    if not API_URL:
        logging.info("API_URL environment variable not set.")
        click.echo("API_URL environment variable not set.")
        return

    url = f"{API_URL}/admin/clients/video-downloads?limit={limit}&offset={offset}&secret_key={SECRET_KEY}"

    logging.info("Fetching downloadable videos...")
    click.echo("Fetching downloadable videos...")
    response = requests.get(url)
    if response.status_code != 200:
        logging.info(f"Failed to retrieve videos: {response.status_code} - {response.text}")
        click.echo(f"Failed to retrieve videos: {response.status_code} - {response.text}")
        return

    data = response.json()
    total_videos = data.get("count", 0)

    if total_videos == 0:
        logging.info("No videos found.")
        click.echo("No videos found.")
        return
    logging.info(f"Total videos: {total_videos}")
    click.echo(f"Total videos: {total_videos}")

    video_results.extend(data.get("results", []))
    offset += len(data.get("results", []))
    progress_bar(offset, total_videos)

    while data.get("next"):
        response = requests.get(data["next"])
        if response.status_code == 200:
            data = response.json()
            video_results.extend(data.get("results", []))
            offset += len(data.get("results", []))
            progress_bar(offset, total_videos)
        else:
            logging.info(f"\nFailed to retrieve data: {response.status_code}")
            click.echo(f"\nFailed to retrieve data: {response.status_code}")
            break

    logging.info("Downloading videos")
    click.echo("Downloading videos")
    download_iteration = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=int(threads)) as executor:
        future_to_video = {
            executor.submit(download_video, video, destination_folder): video
            for video in video_results
        }

        for future in concurrent.futures.as_completed(future_to_video):
            try:
                result = future.result()

                with progress_lock:
                    download_iteration += 1
                    progress_bar(download_iteration, total_videos)

            except Exception as e:
                logging.info(f"\nError downloading {future_to_video[future]}: {e}")
                click.echo(f"\nError downloading {future_to_video[future]}: {e}")

    # logging.info("\nDownload complete!")
    click.echo("\nDownload complete!")

cli.add_command(set_secret_key)
cli.add_command(set_env)
cli.add_command(test)
cli.add_command(download)

if __name__ == "__main__":
    cli()
