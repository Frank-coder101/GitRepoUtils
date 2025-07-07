print("=== CUS STARTING - SIMPLE SCREEN CAPTURE VERSION ===")
import os
import time
import subprocess
import random

try:
    from pynput.keyboard import Controller, Key
    print("pynput imported successfully")
except Exception as e:
    print(f"pynput import failed: {e}")
    exit(1)

try:
    import pyautogui
    from PIL import ImageGrab
    print("Screen capture libraries imported successfully")
except Exception as e:
    print(f"Screen capture libraries import failed: {e}")
    exit(1)

print("=== ALL IMPORTS SUCCESSFUL ===")

# Production Configuration
SAFE_MODE = False  # Production mode - real keyboard simulation
POLL_INTERVAL = 2  # Screen capture interval in seconds
SIMULATION_EVENTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSEvents"
SIMULATION_DICTIONARY_FILE = "simulation_dictionary.txt"
SCREENSHOTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\Screenshots"

# Initialize keyboard controller
print("=== INITIALIZING KEYBOARD CONTROLLER ===")
try:
    keyboard = Controller()
    print("Keyboard controller initialized successfully")
except Exception as e:
    print(f"Keyboard controller initialization failed: {e}")
    exit(1)

def safe_print(message):
    print(f"[CUS] {message}")

def load_simulation_dictionary():
    import json
    if not os.path.exists(SIMULATION_DICTIONARY_FILE):
        return {}
    with open(SIMULATION_DICTIONARY_FILE, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            safe_print("Error: Invalid JSON format in simulation dictionary file.")
            return {}

def capture_screen():
    """Capture screen and save for debugging"""
    try:
        screenshot = ImageGrab.grab()
        timestamp = int(time.time())
        screenshot_path = os.path.join(SCREENSHOTS_PATH, f"screenshot_{timestamp}.png")
        os.makedirs(SCREENSHOTS_PATH, exist_ok=True)
        screenshot.save(screenshot_path)
        safe_print(f"Screenshot saved: {screenshot_path}")
        return screenshot, screenshot_path
    except Exception as e:
        safe_print(f"Error capturing screen: {e}")
        return None, None

def simulate_trigger_detection():
    """Simulate trigger detection for testing - replace with actual OCR later"""
    # For now, just capture screenshots and simulate finding triggers
    screenshot, screenshot_path = capture_screen()
    if screenshot:
        # Simulate that we found a trigger every few screenshots
        if random.randint(1, 3) == 1:  # 1 in 3 chance
            return "Select an option:"
    return None

def perform_action(action):
    """Perform the specified action"""
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
        text = action[5:]
        safe_print(f"About to type: '{text}'")
        
        for char in text:
            keyboard.type(char)
            time.sleep(0.1)
        
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

def log_simulation_event(trigger, action):
    """Log simulation events to a file"""
    timestamp = int(time.time())
    event_filename = f"CUS_simulation_event_{timestamp}.txt"
    event_filepath = os.path.join(SIMULATION_EVENTS_PATH, event_filename)
    
    os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
    
    with open(event_filepath, "w") as event_file:
        event_file.write(f"Trigger: {trigger}\n")
        event_file.write(f"Action: {action}\n")
        event_file.write(f"Timestamp: {timestamp}\n")
        event_file.write(f"Detection Method: Screen Capture (Test Mode)\n")

def main():
    """Main function"""
    try:
        safe_print("Starting CLI User Simulator with Screen Capture (Test Mode)...")
        time.sleep(3)
        
        os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
        os.makedirs(SCREENSHOTS_PATH, exist_ok=True)
        
        simulation_dictionary = load_simulation_dictionary()
        safe_print(f"Loaded {len(simulation_dictionary)} simulation rules")
        
        safe_print("Starting screen monitoring...")
        
        loop_count = 0
        while True:
            time.sleep(POLL_INTERVAL)
            loop_count += 1
            
            # Simulate trigger detection
            trigger = simulate_trigger_detection()
            
            if trigger and trigger in simulation_dictionary:
                action = simulation_dictionary[trigger]
                safe_print(f"Trigger detected: {trigger}")
                safe_print(f"Performing action: {action}")
                perform_action(action)
                log_simulation_event(trigger, action)
            
            if loop_count % 10 == 0:
                safe_print(f"CUS running... (loop {loop_count}) - Taking screenshots every {POLL_INTERVAL}s")
                
    except KeyboardInterrupt:
        safe_print("Interrupted by user. Stopping CUS...")
    except Exception as e:
        safe_print(f"Error: {e}")
        import traceback
        safe_print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()
