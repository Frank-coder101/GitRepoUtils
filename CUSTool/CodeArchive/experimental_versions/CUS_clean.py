import os
import time
import subprocess
import random
from pynput.keyboard import Controller, Key
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Production Configuration
SAFE_MODE = False  # Production mode - real keyboard simulation

# Configuration
OUTPUT_LOG_FILE = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\output.log"
POLL_INTERVAL = 5  # Polling interval in seconds
MAX_LOG_SIZE = 5000  # Maximum characters to capture for errors
NEW_ERRORS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSErrors"
SIMULATION_EVENTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSEvents"
SIMULATION_DICTIONARY_FILE = "simulation_dictionary.txt"

# Production external program command
EXTERNAL_PROGRAM_CMD = ["python", "C:\\Users\\gibea\\Documents\\GitRepos\\DeFiHuddleTradingSystem\\main.py", "--output", OUTPUT_LOG_FILE]

# Initialize keyboard controller for production
keyboard = Controller()

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

    def on_modified(self, event):
        if event.src_path == OUTPUT_LOG_FILE:
            process_log_file(self.simulation_dictionary)

# Check for watchdog availability
try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    USE_WATCHDOG = True
except ImportError:
    USE_WATCHDOG = False

# Process log file content
def process_log_file(simulation_dictionary):
    # Check if log file exists
    if not os.path.exists(OUTPUT_LOG_FILE):
        safe_print("Log file not found. No action taken.")
        return

    # Read log file content
    with open(OUTPUT_LOG_FILE, "r") as log_file:
        log_content = log_file.read()

    # Extract last MAX_LOG_SIZE characters
    if len(log_content) > MAX_LOG_SIZE:
        log_content = log_content[-MAX_LOG_SIZE:]

    # Check for errors in log content
    errors = ["error", "exception", "failed", "timeout", "critical"]
    for error in errors:
        if error.lower() in log_content.lower():
            safe_print(f"Error detected: {error}")
            log_error_event(error, log_content)
            return

    # Check for simulation triggers
    for trigger, action in simulation_dictionary.items():
        if trigger.lower() in log_content.lower():
            safe_print(f"Trigger detected: {trigger}")
            perform_action(action)
            log_simulation_event(trigger, action)

def log_error_event(error, log_content):
    """Log error events to a file"""
    timestamp = int(time.time())
    error_filename = f"CUS_error_event_{timestamp}.txt"
    error_filepath = os.path.join(NEW_ERRORS_PATH, error_filename)
    
    # Ensure directory exists
    os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
    
    with open(error_filepath, "w") as error_file:
        error_file.write(f"Error: {error}\\n")
        error_file.write(f"Timestamp: {timestamp}\\n")
        error_file.write(f"Log Content:\\n{log_content}")

def log_simulation_event(trigger, action):
    """Log simulation events to a file"""
    timestamp = int(time.time())
    event_filename = f"CUS_simulation_event_{timestamp}.txt"
    event_filepath = os.path.join(SIMULATION_EVENTS_PATH, event_filename)
    
    # Ensure directory exists
    os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
    
    with open(event_filepath, "w") as event_file:
        event_file.write(f"Trigger: {trigger}\\n")
        event_file.write(f"Action: {action}\\n")
        event_file.write(f"Timestamp: {timestamp}\\n")

def perform_action(action):
    """Perform the specified action"""
    if action == "press_enter":
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        safe_print("Pressed Enter key")
    elif action == "press_space":
        keyboard.press(Key.space)
        keyboard.release(Key.space)
        safe_print("Pressed Space key")
    elif action == "press_escape":
        keyboard.press(Key.esc)
        keyboard.release(Key.esc)
        safe_print("Pressed Escape key")
    elif action.startswith("type_"):
        text = action[5:]  # Extract text after "type_"
        keyboard.type(text)
        safe_print(f"Typed: {text}")
    elif action == "wait_random":
        wait_time = random.randint(1, 5)
        time.sleep(wait_time)
        safe_print(f"Waited {wait_time} seconds")
    else:
        safe_print(f"Unknown action: {action}")

def launch_external_program():
    """Launch the external program - COMMENTED OUT FOR MANUAL STARTUP"""
    # Commented out for debugging - start your external program manually
    # try:
    #     safe_print(f"Attempting to launch: {' '.join(EXTERNAL_PROGRAM_CMD)}")
    #     process = subprocess.Popen(EXTERNAL_PROGRAM_CMD, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #     safe_print("External program launched successfully")
    #     return process
    # except Exception as e:
    #     safe_print(f"Failed to launch external program: {e}")
    #     safe_print(f"Command was: {EXTERNAL_PROGRAM_CMD}")
    #     return None
    
    safe_print("External program launch is disabled for debugging.")
    safe_print("Please start your external program manually before running CUS.")
    return "dummy_process"  # Return something so we don't exit

def monitor_log_file():
    """Monitor log file for changes"""
    if USE_WATCHDOG:
        print("Using watchdog for file monitoring.")
        event_handler = LogFileHandler()
        observer = Observer()
        observer.schedule(event_handler, path=os.path.dirname(OUTPUT_LOG_FILE), recursive=False)
        observer.start()
        # Store reference to event handler for later access
        observer._event_handler = event_handler
        return observer
    else:
        print("Watchdog unavailable, using polling mechanism.")
        # For polling mode, we'll handle it differently
        return None

# Enhanced error folder monitoring logic
def monitor_error_folder():
    """Monitor error folder and pause operations if errors are present"""
    while True:
        if not os.path.exists(NEW_ERRORS_PATH) or not os.listdir(NEW_ERRORS_PATH):
            safe_print("NewErrorsPath is empty. Resuming operations.")
            return  # Exit monitoring if folder is empty
        safe_print("NewErrorsPath is not empty. Checking again in 5 seconds.")
        time.sleep(5)  # Check every 5 seconds

# Automatically reload simulation dictionary every 15 minutes
def auto_reload_simulation_dictionary():
    """Auto-reload simulation dictionary periodically"""
    while True:
        time.sleep(900)  # Reload every 15 minutes
        safe_print("Reloading simulation dictionary...")
        return load_simulation_dictionary()

def start_auto_reload_thread():
    """Start the auto-reload thread"""
    import threading
    thread = threading.Thread(target=auto_reload_simulation_dictionary, daemon=True)
    thread.start()

def main():
    """Main function to run the CUS system"""
    try:
        print("=== CUS STARTING UP ===")
        safe_print("Starting CLI User Simulator...")
        
        # Add startup delay as suggested
        safe_print("Initializing... (3 second delay)")
        time.sleep(3)
        
        safe_print(f"Watchdog available: {USE_WATCHDOG}")
        
        # Create required directories
        safe_print("Creating directories...")
        os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
        os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
        os.makedirs(os.path.dirname(OUTPUT_LOG_FILE), exist_ok=True)
        safe_print("Directories created successfully")
        
        # Load simulation dictionary
        safe_print("Loading simulation dictionary...")
        simulation_dictionary = load_simulation_dictionary()
        safe_print(f"Loaded {len(simulation_dictionary)} simulation rules")
        
        # Launch external program (disabled for debugging)
        safe_print("External program handling...")
        process = launch_external_program()
        if not process:
            safe_print("Failed to launch external program. Exiting.")
            return
        
        safe_print("External program launch completed. Starting monitoring...")
        
        # Start monitoring
        observer = monitor_log_file()
        safe_print("File monitoring started")
        
        try:
            if USE_WATCHDOG and observer:
                # Watchdog mode
                safe_print("Running in watchdog mode")
                loop_count = 0
                while True:
                    time.sleep(POLL_INTERVAL)
                    loop_count += 1
                    
                    # Update simulation dictionary in the event handler
                    if hasattr(observer, '_event_handler'):
                        observer._event_handler.simulation_dictionary = load_simulation_dictionary()
                    
                    # Monitor error folder
                    monitor_error_folder()
                    
                    if loop_count % 10 == 0:  # Print status every 50 seconds
                        safe_print(f"CUS running... (loop {loop_count})")
            else:
                # Polling mode
                safe_print("Running in polling mode")
                loop_count = 0
                while True:
                    time.sleep(POLL_INTERVAL)
                    loop_count += 1
                    
                    # Manual polling
                    simulation_dictionary = load_simulation_dictionary()
                    if os.path.exists(OUTPUT_LOG_FILE):
                        process_log_file(simulation_dictionary)
                    
                    # Monitor error folder
                    monitor_error_folder()
                    
                    if loop_count % 10 == 0:  # Print status every 50 seconds
                        safe_print(f"CUS running... (loop {loop_count})")
                        
        except KeyboardInterrupt:
            safe_print("Interrupted by user. Stopping CUS...")
        finally:
            if observer:
                observer.stop()
                observer.join()
            if process and process != "dummy_process":
                process.terminate()
            safe_print("CUS stopped.")
    except Exception as e:
        safe_print(f"Error in main function: {e}")
        import traceback
        safe_print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    print("=== CUS PYTHON SCRIPT STARTING ===")
    print("[CUS] Script is being executed directly")
    
    try:
        print("[CUS] About to start auto-reload thread")
        start_auto_reload_thread()  # Enable auto-reloading of simulation dictionary
        print("[CUS] About to call main()")
        main()
        print("[CUS] Main function completed")
    except Exception as e:
        print(f"[CUS] Fatal error: {e}")
        import traceback
        print(f"[CUS] Traceback: {traceback.format_exc()}")
        exit(1)
