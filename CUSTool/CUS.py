import os
import time
import subprocess
import random
from pynput.keyboard import Controller, Key
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
OUTPUT_LOG_FILE = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\output.log"
POLL_INTERVAL = 5  # Polling interval in seconds
MAX_LOG_SIZE = 5000  # Maximum characters to capture for errors
NEW_ERRORS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSErrors"
SIMULATION_EVENTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSEvents"
SIMULATION_DICTIONARY_FILE = "simulation_dictionary.txt"
EXTERNAL_PROGRAM_CMD = ["path_to_external_program", "--output", OUTPUT_LOG_FILE]

# Initialize keyboard controller
keyboard = Controller()

# Extensibility: Load simulation dictionary from a configuration file
def load_simulation_dictionary():
    import json
    if not os.path.exists(SIMULATION_DICTIONARY_FILE):
        return {}
    with open(SIMULATION_DICTIONARY_FILE, "r") as file:
        try:
            return json.load(file)  # Load dictionary from JSON format
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in simulation dictionary file.")
            return {}

# Monitor log file for changes
class LogFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.simulation_dictionary = load_simulation_dictionary()

    # Enhanced CUS Monitoring Process Logic
    def process_log_content(self, log_content):
        for output, simulated_input in load_simulation_dictionary().items():
            if output in log_content:
                time.sleep(random.uniform(0, 0.2))  # Random delay between 0 to 0.2 seconds
                CoreLogic.simulate_input(simulated_input)
                log_simulation_event(output, simulated_input)
                return

        # If no matching output, assume error
        handle_error(log_content)

    # Update LogFileHandler to use process_log_content
    def on_modified(self, event):
        if event.src_path == OUTPUT_LOG_FILE:
            with open(OUTPUT_LOG_FILE, "r") as log_file:
                log_content = log_file.read()
            self.process_log_content(log_content)

LogFileHandler.on_modified = LogFileHandler.on_modified

# Modularize core logic
class CoreLogic:
    @staticmethod
    def simulate_input(input_sequence):
        for char in input_sequence:
            time.sleep(0.1)  # Add a small delay between key presses
            if char == "\n":
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
            else:
                keyboard.press(char)
                keyboard.release(char)

    @staticmethod
    def log_event(event_type, details):
        log_file = os.path.join(SIMULATION_EVENTS_PATH, f"CUS_{event_type}_{int(time.time())}.log")
        with open(log_file, "w") as file:
            file.write(details)

# Enhanced simulation event logging
def log_simulation_event(detected_output, simulated_input):
    os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
    event_file = os.path.join(SIMULATION_EVENTS_PATH, f"CUS_simulation_event_{int(time.time())}.txt")
    with open(event_file, "w") as file:
        file.write(f"Event ID: {int(time.time())}\n")
        file.write(f"Timestamp: {time.ctime()}\n")
        file.write(f"Detected Output: {detected_output}\n")
        file.write(f"Simulated Input: {simulated_input}\n")

    # Aggregate logs into a single file
    aggregate_file = os.path.join(SIMULATION_EVENTS_PATH, "CUS_simulation_events_aggregate.log")
    with open(aggregate_file, "a") as agg_file:
        agg_file.write(f"Event ID: {int(time.time())}\n")
        agg_file.write(f"Timestamp: {time.ctime()}\n")
        agg_file.write(f"Detected Output: {detected_output}\n")
        agg_file.write(f"Simulated Input: {simulated_input}\n\n")

# Configurable error patterns
ERROR_PATTERNS = ["ERROR", "CRITICAL", "FAIL"]

# Enhanced error handling logic
def is_error(log_content):
    for pattern in ERROR_PATTERNS:
        if pattern in log_content:
            return True
    return False

# Handle errors
def handle_error(log_content):
    if is_error(log_content):
        os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
        error_file = os.path.join(NEW_ERRORS_PATH, f"CUS_error_event_{int(time.time())}.txt")
        with open(error_file, "w") as file:
            file.write(log_content[-MAX_LOG_SIZE:])
        terminate_external_program()

# Terminate external program
def terminate_external_program():
    keyboard.press(Key.alt)
    keyboard.press(Key.f4)
    keyboard.release(Key.f4)
    keyboard.release(Key.alt)

# Verify and enhance external program launch logic
def launch_external_program():
    try:
        print(f"Launching external program with command: {EXTERNAL_PROGRAM_CMD}")
        subprocess.Popen(EXTERNAL_PROGRAM_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except Exception as e:
        print(f"Failed to launch external program: {e}")
        terminate_external_program()

# Fallback mechanism for file monitoring
USE_WATCHDOG = True

# Test fallback mechanism for file monitoring
def monitor_log_file():
    if USE_WATCHDOG:
        print("Using watchdog for file monitoring.")
        event_handler = LogFileHandler()
        observer = Observer()
        observer.schedule(event_handler, path=os.path.dirname(OUTPUT_LOG_FILE), recursive=False)
        observer.start()
        return observer
    else:
        print("Watchdog unavailable, using polling mechanism.")
        while True:
            time.sleep(POLL_INTERVAL)
            with open(OUTPUT_LOG_FILE, "r") as log_file:
                log_content = log_file.read()
            event_handler = LogFileHandler()
            event_handler.simulation_dictionary = load_simulation_dictionary()
            event_handler.on_modified(type('Event', (object,), {'src_path': OUTPUT_LOG_FILE}))

# Enhanced error folder monitoring logic
def monitor_error_folder():
    while True:
        if not os.listdir(NEW_ERRORS_PATH):
            print("NewErrorsPath is empty. Resuming operations.")
            return  # Exit monitoring if folder is empty
        print("NewErrorsPath is not empty. Checking again in 5 seconds.")
        time.sleep(5)  # Check every 5 seconds

# Automatically reload simulation dictionary every 15 minutes
def auto_reload_simulation_dictionary():
    while True:
        time.sleep(900)  # Reload every 15 minutes
        LogFileHandler.simulation_dictionary = load_simulation_dictionary()

# Start a background thread for auto-reloading
def start_auto_reload_thread():
    import threading
    reload_thread = threading.Thread(target=auto_reload_simulation_dictionary, daemon=True)
    reload_thread.start()

# Main function
def main():
    # Ensure necessary directories exist
    os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
    os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)

    # Start monitoring the log file
    observer = monitor_log_file()

    try:
        while True:
            time.sleep(POLL_INTERVAL)
            # Reload simulation dictionary if it changes
            observer.event_handler.simulation_dictionary = load_simulation_dictionary()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    observer = None
    try:
        observer = monitor_log_file()
        start_auto_reload_thread()  # Enable auto-reloading of simulation dictionary
        main()
    finally:
        if observer:
            observer.stop()
            observer.join()
