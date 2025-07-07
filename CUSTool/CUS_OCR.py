print("=== CUS STARTING - IMPORT PHASE ===")
import os
print("os imported")
import time
print("time imported")
import subprocess
print("subprocess imported")
import random
print("random imported")

try:
    from pynput.keyboard import Controller, Key
    print("pynput imported successfully")
except Exception as e:
    print(f"pynput import failed: {e}")
    exit(1)

try:
    import pyautogui
    print("pyautogui imported successfully")
except Exception as e:
    print(f"pyautogui import failed: {e}")
    exit(1)

try:
    import pytesseract
    from PIL import Image, ImageGrab
    print("OCR libraries imported successfully")
except Exception as e:
    print(f"OCR libraries import failed: {e}")
    exit(1)

print("=== ALL IMPORTS SUCCESSFUL ===")
print("=== INITIALIZING CONFIGURATION ===")

# Production Configuration
SAFE_MODE = False  # Production mode - real keyboard simulation

# Configuration
POLL_INTERVAL = 3  # Screen capture interval in seconds
MAX_LOG_SIZE = 5000  # Maximum characters to capture for errors
NEW_ERRORS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSErrors"
SIMULATION_EVENTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSEvents"
SIMULATION_DICTIONARY_FILE = "simulation_dictionary.txt"
SCREENSHOTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\Screenshots"

# Screen capture configuration
SCREEN_REGION = None  # None means full screen, or (x, y, width, height) for specific region
CONSOLE_WINDOW_TITLE = "DeFi Huddle Trading System"  # Title to look for in window titles

# Initialize keyboard controller for production
print("=== INITIALIZING KEYBOARD CONTROLLER ===")
try:
    keyboard = Controller()
    print("Keyboard controller initialized successfully")
except Exception as e:
    print(f"Keyboard controller initialization failed: {e}")
    exit(1)

print("=== KEYBOARD CONTROLLER READY ===")
print("=== DEFINING FUNCTIONS ===")

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

# Screen capture and OCR functions
def capture_screen():
    """Capture screen or specific window"""
    try:
        if SCREEN_REGION:
            # Capture specific region
            screenshot = ImageGrab.grab(bbox=SCREEN_REGION)
        else:
            # Capture full screen
            screenshot = ImageGrab.grab()
        
        # Save screenshot for debugging
        timestamp = int(time.time())
        screenshot_path = os.path.join(SCREENSHOTS_PATH, f"screenshot_{timestamp}.png")
        os.makedirs(SCREENSHOTS_PATH, exist_ok=True)
        screenshot.save(screenshot_path)
        
        return screenshot, screenshot_path
    except Exception as e:
        safe_print(f"Error capturing screen: {e}")
        return None, None

def extract_text_from_image(image):
    """Extract text from image using OCR"""
    try:
        # Use pytesseract to extract text
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        safe_print(f"Error extracting text from image: {e}")
        return ""

def process_screen_content(simulation_dictionary, current_text, previous_text):
    """Process screen content for triggers"""
    if not current_text:
        return
    
    # Check if content has changed
    if current_text == previous_text:
        return  # No change, skip processing
    
    safe_print(f"Screen content changed. New text length: {len(current_text)}")
    
    # Extract last MAX_LOG_SIZE characters for processing
    if len(current_text) > MAX_LOG_SIZE:
        text_to_process = current_text[-MAX_LOG_SIZE:]
    else:
        text_to_process = current_text
    
    # Check for errors in screen content
    errors = ["error", "exception", "failed", "timeout", "critical"]
    for error in errors:
        if error.lower() in text_to_process.lower():
            safe_print(f"Error detected on screen: {error}")
            log_error_event(error, text_to_process)
            return
    
    # Check for simulation triggers
    for trigger, action in simulation_dictionary.items():
        if trigger.lower() in text_to_process.lower():
            safe_print(f"Trigger detected on screen: {trigger}")
            perform_action(action)
            log_simulation_event(trigger, action)
            return  # Only process first matching trigger

def log_error_event(error, screen_content):
    """Log error events detected from screen to a file"""
    timestamp = int(time.time())
    error_filename = f"CUS_error_event_{timestamp}.txt"
    error_filepath = os.path.join(NEW_ERRORS_PATH, error_filename)
    
    # Ensure directory exists
    os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
    
    with open(error_filepath, "w") as error_file:
        error_file.write(f"Error: {error}\n")
        error_file.write(f"Timestamp: {timestamp}\n")
        error_file.write(f"Screen Content:\n{screen_content}")

def log_simulation_event(trigger, action):
    """Log simulation events to a file"""
    timestamp = int(time.time())
    event_filename = f"CUS_simulation_event_{timestamp}.txt"
    event_filepath = os.path.join(SIMULATION_EVENTS_PATH, event_filename)
    
    # Ensure directory exists
    os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
    
    with open(event_filepath, "w") as event_file:
        event_file.write(f"Trigger: {trigger}\n")
        event_file.write(f"Action: {action}\n")
        event_file.write(f"Timestamp: {timestamp}\n")
        event_file.write(f"Detection Method: Screen Capture + OCR\n")

def perform_action(action):
    """Perform the specified action"""
    # Add a small delay before performing action to ensure target window is ready
    time.sleep(0.5)
    
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
        safe_print(f"About to type: '{text}'")
        
        # Type each character with a small delay for better reliability
        for char in text:
            keyboard.type(char)
            time.sleep(0.1)  # Small delay between characters
        
        # Press Enter after typing
        time.sleep(0.2)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        safe_print(f"Typed: '{text}' and pressed Enter")
    elif action == "wait_random":
        wait_time = random.randint(1, 5)
        time.sleep(wait_time)
        safe_print(f"Waited {wait_time} seconds")
    else:
        safe_print(f"Unknown action: {action}")

def launch_external_program():
    """Launch the external program - COMMENTED OUT FOR DEBUGGING"""
    safe_print("External program launch is disabled.")
    safe_print("Please start your external program manually before running CUS.")
    return "dummy_process"  # Return something so we don't exit

def monitor_screen():
    """Monitor screen for changes using OCR"""
    safe_print("Using screen capture + OCR for monitoring.")
    return True  # Always available

def capture_and_process_screen(simulation_dictionary, previous_text=""):
    """Capture screen and process for triggers"""
    screenshot, screenshot_path = capture_screen()
    if not screenshot:
        return previous_text
    
    # Extract text from screenshot
    current_text = extract_text_from_image(screenshot)
    
    # Process the extracted text
    process_screen_content(simulation_dictionary, current_text, previous_text)
    
    return current_text

# Enhanced error folder monitoring logic
def monitor_error_folder():
    """Monitor error folder and pause operations if errors are present"""
    # Check if error folder exists and has files
    if os.path.exists(NEW_ERRORS_PATH) and os.listdir(NEW_ERRORS_PATH):
        safe_print("NewErrorsPath contains errors. Pausing operations...")
        while True:
            if not os.path.exists(NEW_ERRORS_PATH) or not os.listdir(NEW_ERRORS_PATH):
                safe_print("NewErrorsPath is now empty. Resuming operations.")
                return  # Exit monitoring if folder is empty
            safe_print("NewErrorsPath still contains errors. Checking again in 5 seconds.")
            time.sleep(5)  # Check every 5 seconds
    # If no errors, just return silently (don't spam the output)

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
        safe_print("Starting CLI User Simulator with Screen Capture...")
        
        # Add startup delay as suggested
        safe_print("Initializing... (3 second delay)")
        time.sleep(3)
        
        safe_print("Using screen capture + OCR for monitoring")
        
        # Create required directories
        safe_print("Creating directories...")
        os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
        os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
        os.makedirs(SCREENSHOTS_PATH, exist_ok=True)
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
        
        safe_print("External program launch completed. Starting screen monitoring...")
        
        # Start monitoring
        monitor_available = monitor_screen()
        safe_print("Screen monitoring started")
        
        try:
            # Screen capture mode
            safe_print("Running in screen capture mode")
            loop_count = 0
            previous_text = ""
            
            while True:
                time.sleep(POLL_INTERVAL)
                loop_count += 1
                
                # Reload simulation dictionary periodically
                if loop_count % 5 == 0:  # Reload every 5 cycles
                    simulation_dictionary = load_simulation_dictionary()
                
                # Capture and process screen
                previous_text = capture_and_process_screen(simulation_dictionary, previous_text)
                
                # Monitor error folder
                monitor_error_folder()
                
                if loop_count % 10 == 0:  # Print status every 30 seconds (3s * 10)
                    safe_print(f"CUS running... (loop {loop_count})")
                        
        except KeyboardInterrupt:
            safe_print("Interrupted by user. Stopping CUS...")
        finally:
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
