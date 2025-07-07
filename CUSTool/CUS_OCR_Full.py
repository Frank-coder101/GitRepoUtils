print("=== CUS STARTING - OCR VERSION WITH TESSERACT ===")
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

try:
    import pytesseract
    # Configure Tesseract path
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print("OCR libraries imported and configured successfully")
except Exception as e:
    print(f"OCR libraries import failed: {e}")
    exit(1)

print("=== ALL IMPORTS SUCCESSFUL ===")

# Production Configuration
SAFE_MODE = False  # Production mode - real keyboard simulation
POLL_INTERVAL = 3  # Screen capture interval in seconds
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
        return screenshot, screenshot_path
    except Exception as e:
        safe_print(f"Error capturing screen: {e}")
        return None, None

def extract_text_from_image(image):
    """Extract text from image using OCR"""
    try:
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        safe_print(f"Error extracting text from image: {e}")
        return ""

def detect_triggers(text, simulation_dictionary):
    """Detect triggers in the extracted text"""
    if not text:
        return None, None
    
    for trigger, action in simulation_dictionary.items():
        if trigger.lower() in text.lower():
            return trigger, action
    
    return None, None

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

def log_simulation_event(trigger, action, extracted_text):
    """Log simulation events to a file"""
    timestamp = int(time.time())
    event_filename = f"CUS_simulation_event_{timestamp}.txt"
    event_filepath = os.path.join(SIMULATION_EVENTS_PATH, event_filename)
    
    os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
    
    with open(event_filepath, "w") as event_file:
        event_file.write(f"Trigger: {trigger}\n")
        event_file.write(f"Action: {action}\n")
        event_file.write(f"Timestamp: {timestamp}\n")
        event_file.write(f"Detection Method: Screen Capture + Tesseract OCR\n")
        event_file.write(f"Extracted Text:\n{extracted_text}\n")

def main():
    """Main function"""
    try:
        safe_print("Starting CLI User Simulator with Real OCR...")
        time.sleep(3)
        
        os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
        os.makedirs(SCREENSHOTS_PATH, exist_ok=True)
        
        simulation_dictionary = load_simulation_dictionary()
        safe_print(f"Loaded {len(simulation_dictionary)} simulation rules")
        
        safe_print("Starting screen monitoring with OCR...")
        
        loop_count = 0
        previous_text = ""
        
        while True:
            time.sleep(POLL_INTERVAL)
            loop_count += 1
            
            # Capture screen and extract text
            screenshot, screenshot_path = capture_screen()
            if screenshot:
                current_text = extract_text_from_image(screenshot)
                
                if current_text and current_text != previous_text:
                    safe_print(f"Screen text changed. Length: {len(current_text)}")
                    safe_print(f"Extracted text preview: {current_text[:100]}...")
                    
                    # Check for triggers
                    trigger, action = detect_triggers(current_text, simulation_dictionary)
                    
                    if trigger and action:
                        safe_print(f"TRIGGER DETECTED: {trigger}")
                        safe_print(f"Performing action: {action}")
                        perform_action(action)
                        log_simulation_event(trigger, action, current_text)
                    
                    previous_text = current_text
            
            if loop_count % 10 == 0:
                safe_print(f"CUS running... (loop {loop_count}) - OCR monitoring active")
                
    except KeyboardInterrupt:
        safe_print("Interrupted by user. Stopping CUS...")
    except Exception as e:
        safe_print(f"Error: {e}")
        import traceback
        safe_print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()
