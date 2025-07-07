import os
import time
import subprocess
import random
from pynput.keyboard import Controller, Key
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# SAFE MODE Configuration - prevents VS Code crashes
SAFE_MODE = True  # Set to False for production use

# Configuration
OUTPUT_LOG_FILE = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\output.log"
POLL_INTERVAL = 5  # Polling interval in seconds
MAX_LOG_SIZE = 5000  # Maximum characters to capture for errors
NEW_ERRORS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSErrors"
SIMULATION_EVENTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSEvents"
SIMULATION_DICTIONARY_FILE = "simulation_dictionary.txt"

# Safe external program command for testing
if SAFE_MODE:
    EXTERNAL_PROGRAM_CMD = ["python", "--version"]  # Safe command for testing
else:
    EXTERNAL_PROGRAM_CMD = ["C:\\Users\\gibea\\Documents\\GitRepos\\DeFiHuddleTradingSystem\\main.py", "--output", OUTPUT_LOG_FILE]

# Initialize keyboard controller (only if not in safe mode)
if not SAFE_MODE:
    keyboard = Controller()
else:
    keyboard = None

def safe_print(message):
    """Safe printing that won't cause issues"""
    print(f"[CUS] {message}")

# Extensibility: Load simulation dictionary from a configuration file
def load_simulation_dictionary():
    import json
    if not os.path.exists(SIMULATION_DICTIONARY_FILE):
        return {}
    with open(SIMULATION_DICTIONARY_FILE, "r") as file:
        try:
            return json.load(file)  # Load dictionary from JSON format
        except json.JSONDecodeError:
            safe_print("Error: Invalid JSON format in simulation dictionary file.")
            return {}

# Monitor log file for changes
class LogFileHandler(FileSystemEventHandler):
    def __init__(self):
        self.simulation_dictionary = load_simulation_dictionary()

    # Enhanced CUS Monitoring Process Logic
    def process_log_content(self, log_content):
        safe_print(f"Processing log content: {len(log_content)} characters")
        for output, simulated_input in load_simulation_dictionary().items():
            if output in log_content:
                if not SAFE_MODE:
                    time.sleep(random.uniform(0, 0.2))  # Random delay between 0 to 0.2 seconds
                    CoreLogic.simulate_input(simulated_input)
                else:
                    safe_print(f"SAFE MODE: Would simulate input for '{output}' -> '{simulated_input}'")
                log_simulation_event(output, simulated_input)
                return

        # If no matching output, assume error
        handle_error(log_content)

    # Update LogFileHandler to use process_log_content
    def on_modified(self, event):
        if event.src_path == OUTPUT_LOG_FILE:
            try:
                with open(OUTPUT_LOG_FILE, "r") as log_file:
                    log_content = log_file.read()
                self.process_log_content(log_content)
            except Exception as e:
                safe_print(f"Error reading log file: {e}")

# Modularize core logic
class CoreLogic:
    @staticmethod
    def simulate_input(input_sequence):
        if SAFE_MODE or keyboard is None:
            safe_print(f"SAFE MODE: Would simulate input: {input_sequence}")
            return
            
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
        os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
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
        safe_print(f"Error detected in log content")
        os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
        error_file = os.path.join(NEW_ERRORS_PATH, f"CUS_error_event_{int(time.time())}.txt")
        with open(error_file, "w") as file:
            file.write(log_content[-MAX_LOG_SIZE:])
        if not SAFE_MODE:
            terminate_external_program()
        else:
            safe_print("SAFE MODE: Would terminate external program")

# Terminate external program
def terminate_external_program():
    if SAFE_MODE or keyboard is None:
        safe_print("SAFE MODE: Would terminate external program with Alt+F4")
        return
        
    keyboard.press(Key.alt)
    keyboard.press(Key.f4)
    keyboard.release(Key.f4)
    keyboard.release(Key.alt)

# Verify and enhance external program launch logic
def launch_external_program():
    try:
        safe_print(f"Launching external program with command: {EXTERNAL_PROGRAM_CMD}")
        if SAFE_MODE:
            # In safe mode, just test the command without redirecting output
            result = subprocess.run(EXTERNAL_PROGRAM_CMD, capture_output=True, text=True, timeout=10)
            safe_print(f"SAFE MODE: Command output: {result.stdout.strip()}")
            safe_print(f"SAFE MODE: Command completed successfully")
        else:
            subprocess.Popen(EXTERNAL_PROGRAM_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            safe_print("External program launched successfully")
    except Exception as e:
        safe_print(f"Failed to launch external program: {e}")
        if not SAFE_MODE:
            terminate_external_program()

# Fallback mechanism for file monitoring
USE_WATCHDOG = True

# Test fallback mechanism for file monitoring
def monitor_log_file():
    if USE_WATCHDOG:
        safe_print("Using watchdog for file monitoring.")
        try:
            event_handler = LogFileHandler()
            observer = Observer()
            observer.schedule(event_handler, path=os.path.dirname(OUTPUT_LOG_FILE), recursive=False)
            observer.start()
            return observer
        except Exception as e:
            safe_print(f"Watchdog failed: {e}, falling back to polling")
            return None
    else:
        safe_print("Watchdog unavailable, using polling mechanism.")
        return None

# Enhanced error folder monitoring logic
def monitor_error_folder():
    while True:
        try:
            if not os.path.exists(NEW_ERRORS_PATH):
                os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
            
            if not os.listdir(NEW_ERRORS_PATH):
                safe_print("NewErrorsPath is empty. Resuming operations.")
                return  # Exit monitoring if folder is empty
            safe_print("NewErrorsPath is not empty. Checking again in 5 seconds.")
            time.sleep(5)  # Check every 5 seconds
        except Exception as e:
            safe_print(f"Error monitoring error folder: {e}")
            time.sleep(5)

# Automatically reload simulation dictionary every 15 minutes
def auto_reload_simulation_dictionary():
    while True:
        try:
            time.sleep(900)  # Reload every 15 minutes
            new_dict = load_simulation_dictionary()
            safe_print("Simulation dictionary reloaded")
        except Exception as e:
            safe_print(f"Error reloading simulation dictionary: {e}")

# Start a background thread for auto-reloading
def start_auto_reload_thread():
    import threading
    reload_thread = threading.Thread(target=auto_reload_simulation_dictionary, daemon=True)
    reload_thread.start()
    safe_print("Auto-reload thread started")

# Main function
def main():
    safe_print(f"Starting CUS in {'SAFE' if SAFE_MODE else 'PRODUCTION'} mode")
    
    # Ensure necessary directories exist
    os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
    os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)

    # Launch external program first
    launch_external_program()

    # Start monitoring the log file
    observer = monitor_log_file()

    try:
        safe_print("Starting main monitoring loop...")
        loop_count = 0
        while True:
            time.sleep(POLL_INTERVAL)
            loop_count += 1
            if loop_count % 12 == 0:  # Every minute
                safe_print(f"CUS running... (loop {loop_count})")
            
            # Reload simulation dictionary if it changes
            if observer and hasattr(observer, 'event_handler'):
                observer.event_handler.simulation_dictionary = load_simulation_dictionary()
    except KeyboardInterrupt:
        safe_print("Received keyboard interrupt, shutting down...")
        if observer:
            observer.stop()
    except Exception as e:
        safe_print(f"Error in main loop: {e}")
    finally:
        if observer:
            try:
                observer.join()
            except:
                pass
        safe_print("CUS shutdown complete")

if __name__ == "__main__":
    safe_print("=== CLI User Simulator (CUS) Starting ===")
    observer = None
    try:
        start_auto_reload_thread()  # Enable auto-reloading of simulation dictionary
        main()
    except Exception as e:
        safe_print(f"Fatal error: {e}")
    finally:
        safe_print("=== CUS Terminated ===")
