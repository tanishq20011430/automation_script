import os
import time
import shutil
import logging
import json
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ======= Logging Setup ========
LOG_FILE = r"C:\Users\tswarnkar\script_new.log"

logging.basicConfig(
    level=logging.DEBUG,  # Capture all log levels
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, mode="w", encoding="utf-8"),  # Overwrite log each run
        logging.StreamHandler()
    ]
)

# Flush logs immediately
logging.info("Logging system initialized.")
logging.getLogger().handlers[0].flush()

# ======= Load Configuration ========
def load_config(config_path=r"C:\Working\tanishq_testing\testing\config.json"):
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        logging.info("Configuration file loaded successfully.")
        return config
    except FileNotFoundError:
        logging.error(f"Configuration file {config_path} not found. Using default paths.")
        return {
            "source_folder": r"C:\Users\tswarnkar\source_folder_test",
            "destination_folder": r"C:\Users\tswarnkar\destination_folder_test"
        }
    except json.JSONDecodeError:
        logging.error("Error reading the configuration file. Check the JSON format.")
        exit(1)

config = load_config()
SOURCE_FOLDER = config["source_folder"]
DEST_FOLDER = config["destination_folder"]

# ======= File Copy Function with Delay ========
def delayed_copy(file_path, source_folder, destination_folder, delay=20):
    """Handles delayed file copying asynchronously."""
    logging.info(f"Thread started for {file_path}. Waiting {delay} seconds before copying...")
    time.sleep(delay)

    logging.debug(f"Checking if file {file_path} is ready...")
    wait_for_file_to_be_ready(file_path)

    logging.info(f"Copying latest file from {source_folder} to {destination_folder}...")
    copy_latest_file(source_folder, destination_folder)

    logging.info(f"Thread completed for {file_path}.")

# ======= Watchdog Event Handler ========
class NewFileHandler(FileSystemEventHandler):
    def __init__(self, source_folder, destination_folder):
        self.source_folder = source_folder
        self.destination_folder = destination_folder

    def on_created(self, event):
        if not event.is_directory:
            logging.info(f"New file detected: {event.src_path}")
            threading.Thread(
                target=delayed_copy,
                args=(event.src_path, self.source_folder, self.destination_folder),
                daemon=True
            ).start()

    def on_modified(self, event):
        if not event.is_directory:
            logging.info(f"File modified: {event.src_path}")
            threading.Thread(
                target=delayed_copy,
                args=(event.src_path, self.source_folder, self.destination_folder),
                daemon=True
            ).start()

    def on_moved(self, event):
        if not event.is_directory:
            logging.info(f"File moved: {event.dest_path}")
            threading.Thread(
                target=delayed_copy,
                args=(event.dest_path, self.source_folder, self.destination_folder),
                daemon=True
            ).start()

# ======= Function to Wait Until File is Ready ========
def wait_for_file_to_be_ready(file_path, max_wait_time=60):
    """Wait until the file is completely written and stable."""
    last_size = -1
    start_time = time.time()

    while time.time() - start_time < max_wait_time:
        try:
            current_size = os.path.getsize(file_path)
            if current_size == last_size:
                logging.info(f"File {file_path} is stable and ready for copying.")
                break
            last_size = current_size
            time.sleep(0.5)
        except FileNotFoundError:
            logging.error(f"File {file_path} not found, skipping check...")
            break
    logging.debug(f"Finished checking readiness for {file_path}.")

# ======= Function to Copy the Latest File ========
def copy_latest_file(source_folder, destination_folder, additional_delay=2):
    if not os.path.exists(source_folder):
        logging.error(f"Source folder does not exist: {source_folder}")
        return
    
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    
    if not files:
        logging.info("No files found in source folder.")
        return
    
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(source_folder, f)))
    source_file_path = os.path.join(source_folder, latest_file)
    destination_file_path = os.path.join(destination_folder, latest_file)

    logging.info(f"Waiting for an additional {additional_delay} seconds before copying {latest_file}...")
    time.sleep(additional_delay)

    os.makedirs(destination_folder, exist_ok=True)
    
    try:
        shutil.copy2(source_file_path, destination_file_path)
        logging.info(f"Copied latest file: {latest_file} to {destination_folder}")
    except Exception as e:
        logging.error(f"Error copying {latest_file}: {e}")

# ======= Main Function ========
def main():
    try:
        logging.info("Starting the script...")

        if not os.path.exists(SOURCE_FOLDER):
            logging.error(f"Source folder does not exist: {SOURCE_FOLDER}")
            exit(1)

        if not os.path.exists(DEST_FOLDER):
            os.makedirs(DEST_FOLDER)
            logging.info(f"Created destination folder: {DEST_FOLDER}")

        event_handler = NewFileHandler(SOURCE_FOLDER, DEST_FOLDER)
        observer = Observer()
        observer.schedule(event_handler, path=SOURCE_FOLDER, recursive=False)
        observer.start()
        logging.info(f"Started monitoring folder: {SOURCE_FOLDER}")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Stopping folder monitoring...")
            observer.stop()

        observer.join()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
