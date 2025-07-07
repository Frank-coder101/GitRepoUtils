import os
import time
from pynput.keyboard import Controller, Key
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
OUTPUT_LOG_FILE = "C:\\Users\\gibea\\Documents\\Personal Finance\\PromptHandler\\CUSTool\\output.log"
POLL_INTERVAL = 5  # Polling interval in seconds
MAX_LOG_SIZE = 5000  # Maximum characters to capture for errors
NEW_ERRORS_PATH = "C:\\Users\\gibea\\Documents\\GitRepos\\DeFiHuddleTradingSystem\\CUSErrors"
SIMULATION_EVENTS_PATH = "C:\\Users\\gibea\\Documents\\Personal Finance\\PromptHandler\\CUSTool\\CUSEvents"
SIMULATION_DICTIONARY_FILE = "simulation_dictionary.txt"

# Initialize keyboard controller
keyboard = Controller()

# Load simulation dictionary
def load_simulation_dictionary():
    if not os.path.exists(SIMULATION_DICTIONARY_FILE):
        return {}
    with open(SIMULATION_DICTIONARY_FILE, "r") as file:
        return dict(line.strip().split("=") for line in file if "=" in line)

# Monitor log file for changes
class LogFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.simulation_dictionary = load_simulation_dictionary()

    def on_modified(self, event):
        if event.src_path == OUTPUT_LOG_FILE:
            with open(OUTPUT_LOG_FILE, "r") as log_file:
                log_content = log_file.read()

            # Process new log content
            for output, simulated_input in self.simulation_dictionary.items():
                if output in log_content:
                    simulate_input(simulated_input)
                    log_simulation_event(output, simulated_input)
                    return

            # Handle errors
            if "ERROR" in log_content:
                handle_error(log_content)

# Simulate keyboard input
def simulate_input(input_sequence):
    for char in input_sequence:
        time.sleep(0.1)  # Add a small delay between key presses
        if char == "\n":
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
        else:
            keyboard.press(char)
            keyboard.release(char)

# Log simulation events
def log_simulation_event(detected_output, simulated_input):
    os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
    event_file = os.path.join(SIMULATION_EVENTS_PATH, f"CUS_simulation_event_{int(time.time())}.txt")
    with open(event_file, "w") as file:
        file.write(f"Detected Output: {detected_output}\nSimulated Input: {simulated_input}\n")

# Handle errors
def handle_error(log_content):
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

# Main function
def main():
    # Ensure necessary directories exist
    os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
    os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)

    # Start monitoring the log file
    event_handler = LogFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(OUTPUT_LOG_FILE), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(POLL_INTERVAL)
            # Reload simulation dictionary if it changes
            event_handler.simulation_dictionary = load_simulation_dictionary()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
