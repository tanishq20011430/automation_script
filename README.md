File Monitoring and Auto-Copy Script

Overview

This Python script monitors a specified folder for new or modified files and automatically copies them to a destination folder after a short delay. It utilizes the watchdog library to detect file changes and handles file copying in a thread-safe manner with proper logging.

Features

Monitors a source folder for new, modified, or moved files.

Waits for a short delay before copying to ensure the file is fully written.

Copies the most recently modified file to the destination folder.

Logs all operations for debugging and tracking.

Runs continuously in the background.

Requirements

Python 3.x

Required libraries:

watchdog

logging

shutil

json

os

time

threading

You can install the necessary package using:

pip install watchdog

Configuration

The script reads configuration settings from a JSON file.

Default Configuration Path

C:\Working\tanishq_testing\testing\config.json

Configuration File Format

{
    "source_folder": "C:\\Users\\tswarnkar\\source_folder_test",
    "destination_folder": "C:\\Users\\tswarnkar\\destination_folder_test"
}

If the configuration file is missing or contains errors, the script falls back to default values.

Usage

Run the script using:

python script.py

How It Works

Logging Setup: Logs all operations in C:\Users\tswarnkar\script_new.log.

Load Configuration: Reads source and destination paths from config.json.

Monitor Folder: Uses watchdog to track changes in the source folder.

Handle File Events:

On file creation, modification, or move, starts a delayed copying process.

Ensures the file is fully written before copying.

Copy Files: Moves the latest file from the source to the destination folder.

Continuous Monitoring: Runs indefinitely until manually stopped.

Logs

Logs are stored in C:\Users\tswarnkar\script_new.log and include timestamps, event details, and errors.

Stopping the Script

Press CTRL+C in the terminal to stop monitoring safely.

Error Handling

Logs missing configuration file errors and uses default paths.

Handles file read/write errors gracefully.

Ensures the script does not crash due to unexpected file system issues.

License

This script is provided as-is for automation purposes. Modify as needed for personal or professional use.

Author

Tanishq Swarnkar

