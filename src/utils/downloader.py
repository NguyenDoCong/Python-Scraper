import os
import sys
import csv
import time
import json
import shutil
import yt_dlp
import logging
import requests
import instaloader
from tqdm import tqdm
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from config import Config

# ---------------------------------
# Logging Setup
# ---------------------------------
logging.basicConfig(
    filename="downloader.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ---------------------------------
# Load Configuration
# ---------------------------------
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {
    "default_format": "show_all",
    "download_directory": "media",
    "history_file": "download_history.csv",
    "mp3_quality": "192",
}


def load_config():
    """Load or create configuration file safely."""
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)

    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        logging.error("Invalid config file. Resetting to defaults.")
        with open(CONFIG_FILE, "w") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4)
        return DEFAULT_CONFIG


config = load_config()
download_directory = config["download_directory"]
history_file = config["history_file"]
mp3_quality = config["mp3_quality"]

os.makedirs(download_directory, exist_ok=True)  # Ensure download directory exists


# ---------------------------------
# Utility Functions
# ---------------------------------
def check_internet_connection():
    """Check if the system has an active internet connection."""
    try:
        requests.head("https://www.google.com", timeout=5)
        return True
    except requests.ConnectionError:
        return False


def ensure_internet_connection():
    """Ensure that an internet connection is active before proceeding."""
    while not check_internet_connection():
        print("\nNo internet connection. Retrying in 5 seconds...")
        time.sleep(5)
    print("Internet connection detected. Proceeding...")


def log_download(url, status):
    """Log the download status in history and log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(history_file, "a+", newline="") as f:
        csv.writer(f).writerow([url, status, timestamp])
    logging.info(f"Download status for {url}: {status}")


def get_unique_filename(filename):
    """Ensure downloaded files are renamed if duplicates exist."""
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(filename):
        filename = f"{base} ({counter}){ext}"
        counter += 1
    return filename

def batch_download_from_file(file_path):
    """Read URLs from a text file and download them concurrently."""
    print(f"Reading URLs from {file_path}...")

    # Read all lines and clean up empty lines
    with open(file_path, "r") as file:
        urls = [line.strip() for line in file.readlines() if line.strip()]

    if not urls:
        print("No URLs found in the file.")
        return

    print("Starting batch download...")

    with ThreadPoolExecutor() as executor:
            list(
                tqdm(
                    executor.map(download_video, urls),
                    total=len(urls),
                    desc="Facebook/Youtube/Tiktok/Instagram Batch",
                )
            )

    print("Download complete.")

def download_video(url):
    """Download a YouTube or TikTok video with user-selected format (ensuring video has audio)."""
    ensure_internet_connection()
    
    try:        
        ydl_opts = {"listformats": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        id = info.get("id")
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(download_directory, f"{id}"),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                },
            ],
        }

        # Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            log_download(url, "Success")
            print(f"\n\033[1;32mDownloaded successfully:\033[0m {id}")

    except Exception as e:
        log_download(url, f"Failed: {str(e)}")
        logging.error(f"Error downloading video from {url}: {str(e)}")
        print(f"\033[1;31mError downloading video:\033[0m {str(e)}")
        
        TIKTOK_ERROR_FILE_PATH = "scraped_data/tiktok_error.txt"

        with open(TIKTOK_ERROR_FILE_PATH, "a") as error_file:
            error_file.write(f"{url}\n")
        print(f"Error logged in error.txt")

if __name__ == "__main__":
    download_video("https://www.tiktok.com/@beatvn_official/video/7486075232663440656")