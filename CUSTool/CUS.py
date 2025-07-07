print("=== CUS STARTING - IMPORT PHASE ===", flush=True)
print("*** CORRECTED CUS.PY WITH ALT+TAB FOCUS - NO WATCHDOG ***", flush=True)
import os
print("os imported", flush=True)
import time
print("time imported", flush=True)
from datetime import datetime
print("datetime imported", flush=True)
import subprocess
print("subprocess imported", flush=True)
import random
print("random imported", flush=True)

# Import required Windows API and system modules
try:
    import psutil
    import pygetwindow as gw
    import pyautogui
    import win32gui
    import win32con
    import win32process
    import win32api
    import win32clipboard
    import re
    import logging
    from PIL import ImageGrab
    import threading
    import queue
    import sys
    import json
    print("System and Windows API modules imported successfully", flush=True)
except Exception as e:
    print(f"System modules import failed: {e}", flush=True)
    exit(1)

try:
    from pynput.keyboard import Controller, Key
    print("pynput imported successfully", flush=True)
except Exception as e:
    print(f"pynput import failed: {e}", flush=True)
    exit(1)

try:
    import pyautogui
    import pygetwindow as gw
    print("pyautogui and window management imported successfully", flush=True)
    # Enable pyautogui window management features
    pyautogui.FAILSAFE = False  # Disable failsafe for automated operation
except Exception as e:
    print(f"pyautogui/window management import failed: {e}", flush=True)
    exit(1)

try:
    import pytesseract
    from PIL import Image, ImageGrab
    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    print("OCR libraries imported successfully", flush=True)
except Exception as e:
    print(f"OCR libraries import failed: {e}", flush=True)
    exit(1)

# Import IssuePromptGenerator for defect reporting
try:
    from IssuePromptGenerator import IssuePromptGenerator, IssueSeverity, FailureType
    ISSUE_PROMPT_AVAILABLE = True
    print("IssuePromptGenerator imported successfully", flush=True)
except ImportError:
    ISSUE_PROMPT_AVAILABLE = False
    print("Warning: IssuePromptGenerator not available - defect prompt generation disabled", flush=True)

print("=== ALL IMPORTS SUCCESSFUL ===", flush=True)
print("=== INITIALIZING CONFIGURATION ===", flush=True)

# Production Configuration
SAFE_MODE = False  # Production mode - real keyboard simulation
ENABLE_ERROR_DETECTION = True  # Enable smart error detection

# Configuration
POLL_INTERVAL = 3  # Screen capture interval in seconds
MAX_LOG_SIZE = 5000  # Maximum characters to capture for errors
NEW_ERRORS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\NewErrors"
SIMULATION_EVENTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSEvents"
SIMULATION_DICTIONARY_FILE = "simulation_dictionary.txt"
SCREENSHOTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\Screenshots"

# Screen capture configuration
SCREEN_REGION = None  # None means full screen, or (x, y, width, height) for specific region
CONSOLE_WINDOW_TITLE = "DeFi Huddle Trading System"  # Title to look for in window titles

# Initialize keyboard controller for production
print("=== INITIALIZING KEYBOARD CONTROLLER ===", flush=True)
try:
    keyboard = Controller()
    print("Keyboard controller initialized successfully", flush=True)
except Exception as e:
    print(f"Keyboard controller initialization failed: {e}", flush=True)
    exit(1)

print("=== KEYBOARD CONTROLLER READY ===", flush=True)
print("=== DEFINING FUNCTIONS ===", flush=True)

def safe_print(message):
    """Safe printing that won't cause issues"""
    print(f"[CUS] {message}", flush=True)

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
        safe_print("OCR functionality disabled - continuing without text extraction")
        # Return empty string to continue operation without OCR
        return ""

# Global variables for action tracking
last_action_time = 0
last_action_type = ""
action_repeat_count = 0

# Global variables for target window tracking
target_window = None
target_window_title = ""
target_window_hwnd = None
target_window_process_id = None

# Global flag for Alt+Tab focus mode
use_alt_tab_focus = False

# Global variables for target window tracking
target_window = None
target_window_title = ""
target_window_hwnd = None

def process_screen_content(simulation_dictionary, current_text, previous_text):
    """Process screen content for triggers"""
    global last_action_time, last_action_type, action_repeat_count
    
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
    
    # SMART ERROR DETECTION: Check if ExtP is showing a menu/input prompt first
    # Menu prompts are typically at the bottom of the screen text
    menu_indicators = [
        "enter your choice:",
        "select an option:",
        "press enter to",
        "type y/n:",
        "continue (y/n)",
        "press any key",
        "choose:",
        "select:",
        "[y/n]",
        "(y/n)",
        "enter to continue",
        "press enter",
        "menu:",
        "options:",
        "1.",  # Numbered menu items
        "2.", 
        "3.",
        ">>>",  # Command prompt
        ">>",
        ">",
        "waiting for input",
        "please select",
        "make your choice"
    ]
    
    # Check the last 500 characters (bottom of screen) for menu indicators
    text_bottom = text_to_process[-500:].lower()
    is_showing_menu = any(indicator in text_bottom for indicator in menu_indicators)
    
    if is_showing_menu:
        safe_print("ExtP appears to be showing a menu or waiting for input - skipping error detection")
    else:
        # Only check for errors if NOT showing a menu
        if ENABLE_ERROR_DETECTION:
            # Look for patterns that indicate REAL errors, not menu text
            actual_error_patterns = [
                "error:",
                "exception:",
                "failed to",
                "could not",
                "timeout occurred",
                "critical error",
                "fatal error",
                "runtime error",
                "traceback (most recent call last)",
                "stack trace",
                "connection failed",
                "file not found",
                "access denied",
                "permission denied",
                "out of memory",
                "disk full",
                "network error",
                "database error",
                "syntax error",
                "import error",
                "module not found",
                "assertion error",
                "value error",
                "type error",
                "key error",
                "index error"
            ]
            
            text_lower = text_to_process.lower()
            for error_pattern in actual_error_patterns:
                if error_pattern in text_lower:
                    # Double-check this isn't part of a menu option or help text
                    error_context = get_error_context(text_lower, error_pattern)
                    if is_real_error(error_context):
                        safe_print(f"Actual error detected: {error_pattern}")
                        safe_print(f"Error context: {error_context}")
                        log_error_event(error_pattern, text_to_process)
                        return
    
    # Check for simulation triggers
    for trigger, action in simulation_dictionary.items():
        if trigger.lower() in text_to_process.lower():
            safe_print(f"Trigger detected on screen: {trigger}")
            
            # Check for repetitive actions (indicating action failure)
            current_time = time.time()
            if action == last_action_type and (current_time - last_action_time) < 30:  # Same action within 30 seconds
                action_repeat_count += 1
                if action_repeat_count >= 3:  # 3 repetitions indicate failure
                    safe_print(f"Action '{action}' repeated {action_repeat_count} times - possible failure")
                    generate_action_failure_prompt(trigger, action, text_to_process)
                    action_repeat_count = 0  # Reset counter
                    return
            else:
                action_repeat_count = 0  # Reset if different action or too much time passed
            
            last_action_time = current_time
            last_action_type = action
            
            perform_action(action)
            log_simulation_event(trigger, action)
            return  # Only process first matching trigger

def get_error_context(text, error_pattern):
    """Get context around an error pattern to help determine if it's a real error"""
    try:
        error_index = text.find(error_pattern)
        if error_index == -1:
            return ""
        
        # Get 100 characters before and after the error
        start = max(0, error_index - 100)
        end = min(len(text), error_index + len(error_pattern) + 100)
        context = text[start:end]
        return context.strip()
    except:
        return ""

def is_real_error(error_context):
    """Determine if an error context indicates a real error vs menu/help text"""
    if not error_context:
        return True  # If we can't get context, assume it's real
    
    # These phrases suggest it's NOT a real error, but menu/help text
    false_positive_indicators = [
        "if you see an error",
        "in case of error",
        "error handling",
        "error codes:",
        "error messages:",
        "troubleshooting errors",
        "common errors:",
        "error description",
        "error type:",
        "error log",
        "error options",
        "error menu",
        "help with errors",
        "error information",
        "error details",
        "select error",
        "choose error",
        "error category"
    ]
    
    error_lower = error_context.lower()
    for indicator in false_positive_indicators:
        if indicator in error_lower:
            return False  # This is likely menu/help text, not a real error
    
    # These patterns suggest it IS a real error
    real_error_indicators = [
        "occurred",
        "failed",
        "cannot",
        "unable to",
        "not found",
        "denied",
        "timeout",
        "crashed",
        "terminated",
        "aborted",
        "interrupted",
        "corrupted",
        "invalid",
        "unexpected"
    ]
    
    for indicator in real_error_indicators:
        if indicator in error_lower:
            return True  # This looks like a real error
    
    # Default to treating it as a real error if unsure
    return True

def generate_action_failure_prompt(trigger, action, screen_content):
    """Generate defect prompt for action failures"""
    if issue_prompt_generator:
        try:
            from IssuePromptGenerator import TestCaseContext, DocumentationReference
            safe_print(f"Generating defect prompt for action failure: {action}")
            
            test_context = TestCaseContext(
                test_case_name="Action Effectiveness Failure",
                test_sequence_id=f"ACTION_FAILURE_{int(time.time())}",
                expected_behavior=f"Action '{action}' should change screen content after trigger '{trigger}'",
                actual_behavior=f"Action '{action}' repeated multiple times without expected result",
                failure_step=1,
                reproduction_steps=[
                    f"Wait for trigger: {trigger}",
                    f"Perform action: {action}",
                    "Observe screen content",
                    "Action repeats without progress"
                ],
                documentation_refs=[
                    DocumentationReference(
                        file_path="simulation_dictionary.txt",
                        reference_type="requirement",
                        reference_id="CUS-DICT",
                        section_title="CUS Action Dictionary"
                    )
                ],
                related_test_cases=["CUS Simulation Tests"],
                dependency_chain=["CUS", "ExtP", "Screen Detection"]
            )
            
            prompt_obj = issue_prompt_generator.generate_issue_prompt(
                test_case_context=test_context,
                error_context={
                    "error_type": "cus_simulation",
                    "error_message": f"Action '{action}' repeated {action_repeat_count} times without expected result",
                    "trigger": trigger,
                    "action": action,
                    "repeat_count": action_repeat_count,
                    "screen_content": screen_content[:1000]
                }
            )
            
            saved_path = issue_prompt_generator.save_issue_prompt(prompt_obj)
            safe_print(f"Generated defect prompt for action failure: {prompt_obj.issue_id}")
            safe_print(f"Defect prompt saved to: {saved_path}")
            
        except Exception as e:
            safe_print(f"Error generating action failure prompt: {e}")
    else:
        safe_print("IssuePromptGenerator not available for action failure detection")

def log_error_event(error, screen_content):
    """Log error events to a file and generate defect prompt"""
    timestamp = int(time.time())
    error_filename = f"CUS_error_event_{timestamp}.txt"
    error_filepath = os.path.join(NEW_ERRORS_PATH, error_filename)
    
    # Ensure directory exists
    os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
    
    with open(error_filepath, "w") as error_file:
        error_file.write(f"Error: {error}\n")
        error_file.write(f"Timestamp: {timestamp}\n")
        error_file.write(f"Screen Content:\n{screen_content}")
    
    # Generate defect prompt if available
    if issue_prompt_generator:
        try:
            # Create test case context for external program error
            from IssuePromptGenerator import TestCaseContext, DocumentationReference
            test_context = TestCaseContext(
                test_case_name="External Program Error Detection",
                test_sequence_id=f"CUS_ERROR_{timestamp}",
                expected_behavior="External program should operate without errors",
                actual_behavior=f"Error detected: {error}",
                failure_step=0,
                reproduction_steps=["Monitor screen content", "Detect error condition"],
                documentation_refs=[],
                related_test_cases=[],
                dependency_chain=[]
            )
            
            # Generate defect prompt
            prompt_obj = issue_prompt_generator.generate_issue_prompt(
                test_case_context=test_context,
                error_context={
                    "error_type": "external_program_error",
                    "error_message": f"Error detected: {error}",
                    "screen_content": screen_content[:1000]
                }
            )
            
            saved_path = issue_prompt_generator.save_issue_prompt(prompt_obj)
            safe_print(f"Generated defect prompt for error: {prompt_obj.issue_id}")
            safe_print(f"Defect prompt saved to: {saved_path}")
            
        except Exception as e:
            safe_print(f"Error generating defect prompt: {e}")

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
    """Perform the specified action with multiple input methods for reliability"""
    safe_print(f"Starting action: {action}")
    
    # Add a small delay before performing action to ensure target window is ready
    time.sleep(0.5)
    
    # Focus on the external program window with multiple attempts
    focus_success = False
    for attempt in range(5):  # Try 5 times
        safe_print(f"Focus attempt {attempt + 1}/5...")
        
        # Choose focus method based on mode
        if use_alt_tab_focus:
            safe_print("Using Alt+Tab to switch to ExtP...")
            focus_result = focus_using_alt_tab()
        elif target_window_hwnd:
            safe_print("Using stored window handle to focus ExtP...")
            focus_result = focus_target_window()
        else:
            safe_print("Using pattern matching to find and focus ExtP...")
            focus_result = focus_external_program_window()
            
        if focus_result:
            focus_success = True
            safe_print(f"Focus successful on attempt {attempt + 1}")
            break
        time.sleep(2)  # Wait longer between retry attempts
    
    if not focus_success:
        safe_print("WARNING: Could not focus external program window!")
        safe_print("Keys will be sent to whatever window is currently active.")
        safe_print("Please manually focus on ExtP window if this continues.")
        
        # Generate a defect prompt for focusing failure
        if ISSUE_PROMPT_AVAILABLE and attempt >= 3:  # Only after multiple failures
            try:
                from IssuePromptGenerator import TestCaseContext, DocumentationReference
                test_context = TestCaseContext(
                    test_case_name="Window Focus Failure",
                    test_sequence_id=f"FOCUS_FAILURE_{int(time.time())}",
                    expected_behavior="CUS should be able to focus on ExtP window before sending keys",
                    actual_behavior="CUS failed to focus on ExtP window after multiple attempts",
                    failure_step=1,
                    reproduction_steps=[
                        "CUS attempts to focus ExtP window",
                        "Window focusing fails multiple times",
                        "Keys may be sent to wrong window"
                    ],
                    documentation_refs=[
                        DocumentationReference(
                            file_path="CUS.py",
                            reference_type="requirement",
                            reference_id="CUS-FOCUS",
                            section_title="Window Focus Management"
                        )
                    ],
                    related_test_cases=["CUS Window Management"],
                    dependency_chain=["CUS", "ExtP", "Windows API"]
                )
                
                # Initialize issue generator if not already done
                if not globals().get('issue_prompt_generator'):
                    external_program_path = r"C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem"
                    initialize_issue_prompt_generator(external_program_path)
                
                prompt_obj = issue_prompt_generator.generate_issue_prompt(
                    test_case_context=test_context,
                    error_context={
                        "error_type": "window_focus_failure",
                        "error_message": "Failed to focus on ExtP window after multiple attempts",
                        "action_attempted": action,
                        "attempts_made": attempt + 1
                    }
                )
                
                saved_path = issue_prompt_generator.save_issue_prompt(prompt_obj)
                safe_print(f"Generated defect prompt for focus failure: {prompt_obj.issue_id}")
                
            except Exception as e:
                safe_print(f"Error generating focus failure prompt: {e}")
    
    # Add extra delay after focusing attempt
    time.sleep(1)
    
    if action == "press_enter":
        # Multi-method approach for Enter key
        send_key_multiple_methods(Key.enter, "Enter")
    elif action == "press_space":
        send_key_multiple_methods(Key.space, "Space")
    elif action == "press_escape":
        send_key_multiple_methods(Key.esc, "Escape")
    elif action.startswith("type_"):
        text = action[5:]  # Extract text after "type_"
        safe_print(f"About to type: '{text}'")
        
        # Multi-method approach for typing
        send_text_multiple_methods(text)
        
        # Press Enter after typing using multiple methods
        time.sleep(0.5)
        send_key_multiple_methods(Key.enter, "Enter")
        safe_print(f"Completed typing: '{text}' and pressed Enter")
    elif action == "wait_random":
        wait_time = random.randint(1, 5)
        time.sleep(wait_time)
        safe_print(f"Waited {wait_time} seconds")
    else:
        safe_print(f"Unknown action: {action}")
        
    # Verify action was effective by checking if we should wait for screen change
    safe_print(f"Action '{action}' completed. Waiting for potential screen update...")
    time.sleep(1)  # Give time for the action to take effect

def send_key_multiple_methods(key, key_name):
    """Send a key using multiple methods for maximum reliability"""
    safe_print(f"Sending {key_name} key using multiple methods...")
    
    # Method 1: pynput keyboard
    try:
        keyboard.press(key)
        keyboard.release(key)
        safe_print(f"Method 1 (pynput): {key_name} sent")
        time.sleep(0.2)
    except Exception as e:
        safe_print(f"Method 1 (pynput) failed: {e}")
    
    # Method 2: pyautogui
    try:
        if key == Key.enter:
            pyautogui.press('enter')
        elif key == Key.space:
            pyautogui.press('space')
        elif key == Key.esc:
            pyautogui.press('esc')
        safe_print(f"Method 2 (pyautogui): {key_name} sent")
        time.sleep(0.2)
    except Exception as e:
        safe_print(f"Method 2 (pyautogui) failed: {e}")
    
    # Method 3: Windows-specific using ctypes (for Windows)
    try:
        import ctypes
        from ctypes import wintypes
        
        # Define Windows key codes
        if key == Key.enter:
            vk_code = 0x0D  # VK_RETURN
        elif key == Key.space:
            vk_code = 0x20  # VK_SPACE
        elif key == Key.esc:
            vk_code = 0x1B  # VK_ESCAPE
        else:
            vk_code = None
            
        if vk_code:
            # Send key down and up
            ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)  # Key down
            time.sleep(0.05)
            ctypes.windll.user32.keybd_event(vk_code, 0, 2, 0)  # Key up
            safe_print(f"Method 3 (Windows API): {key_name} sent")
            time.sleep(0.2)
    except Exception as e:
        safe_print(f"Method 3 (Windows API) failed: {e}")

def send_text_multiple_methods(text):
    """Send text using multiple methods for maximum reliability"""
    safe_print(f"Sending text '{text}' using multiple methods...")
    
    # Method 1: pynput keyboard (character by character)
    try:
        for char in text:
            keyboard.type(char)
            time.sleep(0.1)  # Small delay between characters
        safe_print(f"Method 1 (pynput): Text '{text}' sent")
        time.sleep(0.3)
    except Exception as e:
        safe_print(f"Method 1 (pynput) failed: {e}")
    
    # Method 2: pyautogui typewrite
    try:
        pyautogui.typewrite(text, interval=0.1)
        safe_print(f"Method 2 (pyautogui): Text '{text}' sent")
        time.sleep(0.3)
    except Exception as e:
        safe_print(f"Method 2 (pyautogui) failed: {e}")
    
    # Method 3: Windows clipboard + Ctrl+V
    try:
        import pyperclip
        import ctypes
        
        pyperclip.copy(text)
        time.sleep(0.1)
        
        # Send Ctrl+V
        ctypes.windll.user32.keybd_event(0x11, 0, 0, 0)  # Ctrl down
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(0x56, 0, 0, 0)  # V down
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(0x56, 0, 2, 0)  # V up
        ctypes.windll.user32.keybd_event(0x11, 0, 2, 0)  # Ctrl up
        
        safe_print(f"Method 3 (Clipboard): Text '{text}' sent")
        time.sleep(0.3)
    except Exception as e:
        safe_print(f"Method 3 (Clipboard) failed: {e}")

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
    # Show minimal activity indicator every few calls
    if not hasattr(capture_and_process_screen, 'call_count'):
        capture_and_process_screen.call_count = 0
    
    capture_and_process_screen.call_count += 1
    
    # Show activity indicator every 20 calls (about 1 minute)
    if capture_and_process_screen.call_count % 20 == 0:
        safe_print(f"[{datetime.now().strftime('%H:%M:%S')}] Screen monitoring active...")
    
    screenshot, screenshot_path = capture_screen()
    if not screenshot:
        safe_print("Screen capture failed - continuing...")
        return previous_text
    
    # Extract text from screenshot
    current_text = extract_text_from_image(screenshot)
    
    # If OCR failed, inform user but continue
    if not current_text and screenshot:
        safe_print("OCR text extraction failed - screenshots saved for manual review")
        safe_print(f"Screenshot saved to: {screenshot_path}")
        return previous_text
    
    # Process the extracted text
    if current_text:
        process_screen_content(simulation_dictionary, current_text, previous_text)
    
    return current_text

# Enhanced error folder monitoring logic - SIMPLIFIED
# Now integrated directly into the main loop instead of using a blocking function

# Automatically reload simulation dictionary periodically - REMOVED
# Threading approach removed in favor of simple loop-based reloading

# REMOVED: auto_reload_simulation_dictionary() and start_auto_reload_thread()
# The main loop now handles dictionary reloading directly

# Global IssuePromptGenerator instance
issue_prompt_generator = None

def initialize_issue_prompt_generator(external_program_path=""):
    """Initialize the IssuePromptGenerator"""
    global issue_prompt_generator
    if ISSUE_PROMPT_AVAILABLE:
        try:
            issue_config = {
                "external_program_path": external_program_path,
                "annotate_screenshots": True,
                "capture_before_after": False,
                "capture_sequence": False,
                "severity_mapping": {
                    "external_crash": IssueSeverity.CRITICAL,
                    "external_error": IssueSeverity.ERROR,
                    "cus_failure": IssueSeverity.ERROR,
                    "ocr_mismatch": IssueSeverity.WARNING,
                    "timeout": IssueSeverity.WARNING
                },
                "screenshot_settings": {
                    "save_original": True,
                    "save_annotated": True,
                    "annotation_color": "red",
                    "annotation_width": 3
                }
            }
            issue_prompt_generator = IssuePromptGenerator(issue_config)
            safe_print("IssuePromptGenerator initialized successfully")
        except Exception as e:
            safe_print(f"Error initializing IssuePromptGenerator: {e}")
            issue_prompt_generator = None
    else:
        safe_print("IssuePromptGenerator not available")

def test_defect_prompt_generation():
    """Test defect prompt generation to ensure the system is working"""
    if issue_prompt_generator:
        try:
            from IssuePromptGenerator import TestCaseContext, DocumentationReference
            safe_print("Testing defect prompt generation...")
            
            test_context = TestCaseContext(
                test_case_name="Test Defect Prompt Generation",
                test_sequence_id=f"TEST_DEFECT_{int(time.time())}",
                expected_behavior="System should generate defect prompts when issues occur",
                actual_behavior="Testing defect prompt generation system",
                failure_step=1,
                reproduction_steps=["Run CUS", "Trigger test", "Check DefectPrompts directory"],
                documentation_refs=[
                    DocumentationReference(
                        file_path="CUS Requirements.md",
                        reference_type="requirement",
                        reference_id="CUS-001",
                        section_title="Defect Prompt Generation"
                    )
                ],
                related_test_cases=["CUS Integration Test"],
                dependency_chain=["CUS", "ExtP", "DefectPrompts"]
            )
            
            prompt_obj = issue_prompt_generator.generate_issue_prompt(
                test_case_context=test_context,
                error_context={
                    "error_type": "cus_simulation",
                    "error_message": "Testing defect prompt generation system",
                    "test_type": "defect_prompt_generation",
                    "description": "Testing if defect prompt generation system is working",
                    "timestamp": time.time()
                }
            )
            
            saved_path = issue_prompt_generator.save_issue_prompt(prompt_obj)
            safe_print(f"Test defect prompt generated successfully: {prompt_obj.issue_id}")
            safe_print(f"Defect prompt saved to: {saved_path}")
            safe_print(f"Defect prompts directory: {issue_prompt_generator.defect_prompts_path}")
            
        except Exception as e:
            safe_print(f"Error in test defect prompt generation: {e}")
            import traceback
            safe_print(f"Traceback: {traceback.format_exc()}")
    else:
        safe_print("IssuePromptGenerator not available for testing")

def detect_ocr_mismatch(expected_text, actual_text, context=""):
    """Detect OCR mismatches and generate defect prompts"""
    if not expected_text or not actual_text:
        return
    
    # Simple similarity check (can be enhanced with fuzzy matching)
    if expected_text.lower().strip() != actual_text.lower().strip():
        safe_print(f"OCR mismatch detected - Expected: '{expected_text}', Actual: '{actual_text}'")
        
        # Generate defect prompt if available
        if issue_prompt_generator:
            try:
                from IssuePromptGenerator import TestCaseContext, DocumentationReference
                test_context = TestCaseContext(
                    test_case_name="OCR Content Verification",
                    test_sequence_id=f"OCR_MISMATCH_{int(time.time())}",
                    expected_behavior=f"Screen should display: '{expected_text}'",
                    actual_behavior=f"Screen actually displays: '{actual_text}'",
                    failure_step=0,
                    reproduction_steps=["Capture screen", "Extract text via OCR", "Compare with expected"],
                    documentation_refs=[],
                    related_test_cases=[],
                    dependency_chain=[]
                )
                
                prompt_obj = issue_prompt_generator.generate_issue_prompt(
                    test_case_context=test_context,
                    error_context={
                        "error_type": "ocr_mismatch",
                        "error_message": f"OCR mismatch detected - Expected: '{expected_text}', Actual: '{actual_text}'",
                        "expected_text": expected_text,
                        "actual_text": actual_text,
                        "context": context
                    }
                )
                
                saved_path = issue_prompt_generator.save_issue_prompt(prompt_obj)
                safe_print(f"Generated defect prompt for OCR mismatch: {prompt_obj.issue_id}")
                safe_print(f"Defect prompt saved to: {saved_path}")
                
            except Exception as e:
                safe_print(f"Error generating OCR mismatch prompt: {e}")

def focus_external_program_window():
    """Focus on the external program window before performing actions"""
    try:
        # Try to find window by title patterns (in order of preference)
        window_patterns = [
            "DeFi Huddle Trading System",
            "defi huddle",
            "trading system",
            "python.exe",
            "cmd.exe",
            "Command Prompt", 
            "Windows PowerShell",
            "PowerShell",
            "Terminal"
        ]
        
        safe_print("Attempting to focus external program window...")
        
        # Get all windows and log them for debugging
        all_windows = gw.getAllWindows()
        safe_print(f"Found {len(all_windows)} total windows")
        
        # Log visible windows for debugging
        visible_windows = [w for w in all_windows if w.visible and w.title.strip()]
        safe_print(f"Visible windows with titles ({len(visible_windows)}):")
        for i, window in enumerate(visible_windows[:15]):  # Show first 15
            safe_print(f"  {i+1}. '{window.title}'")
        
        # Try to find matching window using exact and partial matches
        best_match = None
        match_score = 0
        
        for pattern in window_patterns:
            safe_print(f"Searching for pattern: '{pattern}'")
            
            # Try exact match first
            for window in all_windows:
                if window.visible and window.title.strip():
                    title_lower = window.title.lower()
                    pattern_lower = pattern.lower()
                    
                    # Exact match (highest priority)
                    if title_lower == pattern_lower and match_score < 3:
                        best_match = window
                        match_score = 3
                        safe_print(f"Exact match found: '{window.title}'")
                        break
                    
                    # Contains match
                    elif pattern_lower in title_lower and match_score < 2:
                        best_match = window
                        match_score = 2
                        safe_print(f"Contains match found: '{window.title}' contains '{pattern}'")
                    
                    # Partial word match
                    elif any(word in title_lower for word in pattern_lower.split()) and match_score < 1:
                        best_match = window
                        match_score = 1
                        safe_print(f"Partial match found: '{window.title}' matches part of '{pattern}'")
            
            if best_match and match_score >= 2:  # Stop at good matches
                break
        
        # Try to activate the best match
        if best_match:
            try:
                safe_print(f"Attempting to activate best match: '{best_match.title}'")
                
                # Multiple activation attempts
                for attempt in range(3):
                    try:
                        best_match.activate()
                        time.sleep(0.5)
                        
                        # Verify activation by checking if it's the foreground window
                        import ctypes
                        foreground_hwnd = ctypes.windll.user32.GetForegroundWindow()
                        if hasattr(best_match, '_hWnd') and best_match._hWnd == foreground_hwnd:
                            safe_print(f"Successfully activated: '{best_match.title}' (attempt {attempt + 1})")
                            return True
                        else:
                            safe_print(f"Activation attempt {attempt + 1} may have failed, trying again...")
                            
                    except Exception as e:
                        safe_print(f"Activation attempt {attempt + 1} failed: {e}")
                        time.sleep(0.5)
                
                # Alternative activation using Windows API
                safe_print("Trying Windows API activation...")
                try:
                    import ctypes
                    from ctypes import wintypes
                    
                    if hasattr(best_match, '_hWnd'):
                        hwnd = best_match._hWnd
                        # Bring window to front
                        ctypes.windll.user32.SetForegroundWindow(hwnd)
                        ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE
                        ctypes.windll.user32.SetActiveWindow(hwnd)
                        time.sleep(0.5)
                        safe_print(f"Windows API activation attempted for: '{best_match.title}'")
                        return True
                        
                except Exception as e:
                    safe_print(f"Windows API activation failed: {e}")
                
            except Exception as e:
                safe_print(f"Could not activate window '{best_match.title}': {e}")
        
        # If no specific window found, try clicking approach
        safe_print("No suitable window found. Using click-to-focus approach.")
        try:
            # Click on center of screen to ensure some window is focused
            screen_width, screen_height = pyautogui.size()
            center_x, center_y = screen_width // 2, screen_height // 2
            safe_print(f"Clicking at screen center: ({center_x}, {center_y})")
            pyautogui.click(center_x, center_y)
            time.sleep(0.5)
            
            # Try Alt+Tab to cycle through windows
            safe_print("Attempting Alt+Tab to cycle to target window...")
            pyautogui.hotkey('alt', 'tab')
            time.sleep(1)
            
            return True
        except Exception as e:
            safe_print(f"Click-to-focus failed: {e}")
        
        return False
        
    except Exception as e:
        safe_print(f"Error in window focusing: {e}")
        import traceback
        safe_print(f"Focus error traceback: {traceback.format_exc()}")
        return False

def list_available_windows():
    """List all available windows for debugging"""
    try:
        all_windows = gw.getAllWindows()
        safe_print(f"Found {len(all_windows)} windows:")
        for i, window in enumerate(all_windows[:10]):  # Show first 10
            if window.visible and window.title.strip():
                safe_print(f"  {i+1}. '{window.title}' (visible: {window.visible})")
    except Exception as e:
        safe_print(f"Error listing windows: {e}")

def get_foreground_window_info():
    """Get detailed information about the currently focused window."""
    try:
        # Get the foreground window handle
        hwnd = win32gui.GetForegroundWindow()
        if not hwnd:
            return None
        
        # Get window title
        title = win32gui.GetWindowText(hwnd)
        
        # Get process ID
        _, process_id = win32process.GetWindowThreadProcessId(hwnd)
        
        # Get process name
        process_name = ""
        try:
            process = psutil.Process(process_id)
            process_name = process.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        
        # Get window class name
        class_name = win32gui.GetClassName(hwnd)
        
        # Get window rect
        rect = win32gui.GetWindowRect(hwnd)
        
        return {
            'hwnd': hwnd,
            'title': title,
            'process_id': process_id,
            'process_name': process_name,
            'class_name': class_name,
            'rect': rect,
            'x': rect[0],
            'y': rect[1],
            'width': rect[2] - rect[0],
            'height': rect[3] - rect[1]
        }
    except Exception as e:
        safe_print(f"Error getting foreground window info: {str(e)}")
        return None

def prompt_user_for_focus_and_switch():
    """Simple focus workflow: user focuses ExtP, confirms in CUS, then Alt+Tab back"""
    print("\n" + "="*60, flush=True)
    print("SIMPLE WINDOW FOCUS SETUP", flush=True)
    print("="*60, flush=True)
    print("Please follow these steps:", flush=True)
    print("1. Click on the External Program (ExtP) window to bring it into focus", flush=True)
    print("2. Make sure ExtP is visible and active", flush=True)
    print("3. Return to this CUS window and type 'Y' then press Enter", flush=True)
    print("4. CUS will then use Alt+Tab to switch back to ExtP", flush=True)
    print("="*60, flush=True)
    
    while True:
        user_input = input("Type 'Y' when ExtP is focused and ready (or 'q' to quit): ").strip().upper()
        
        if user_input == 'Q':
            print("Setup cancelled.", flush=True)
            return False
        elif user_input == 'Y':
            print("Switching back to ExtP using Alt+Tab...", flush=True)
            
            # Use Alt+Tab to switch to the previous window (ExtP)
            try:
                pyautogui.hotkey('alt', 'tab')
                time.sleep(0.5)  # Give time for the switch to complete
                print("✓ Alt+Tab executed - ExtP should now be in focus", flush=True)
                print("✓ Simple focus setup complete!", flush=True)
                return True
            except Exception as e:
                print(f"✗ Error executing Alt+Tab: {e}", flush=True)
                return False
        else:
            print("Please type 'Y' to confirm or 'q' to quit.", flush=True)

def focus_using_alt_tab():
    """Use Alt+Tab to switch back to the previously focused window (ExtP)"""
    try:
        safe_print("Using Alt+Tab to switch to ExtP window...")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.3)  # Brief pause for window switch
        safe_print("Alt+Tab executed - should be focused on ExtP")
        return True
    except Exception as e:
        safe_print(f"Error executing Alt+Tab: {e}")
        return False

def focus_target_window():
    """Focus the target window using the stored window handle."""
    global target_window_hwnd, target_window_title
    
    if not target_window_hwnd:
        safe_print("No target window handle stored")
        return False
    
    try:
        # Verify the window still exists
        if not win32gui.IsWindow(target_window_hwnd):
            safe_print(f"Target window handle {target_window_hwnd} is no longer valid")
            return False
        
        # Check if window is visible
        if not win32gui.IsWindowVisible(target_window_hwnd):
            safe_print(f"Target window {target_window_title} is not visible")
            # Try to show it
            win32gui.ShowWindow(target_window_hwnd, win32con.SW_SHOW)
        
        # Restore if minimized
        if win32gui.IsIconic(target_window_hwnd):
            win32gui.ShowWindow(target_window_hwnd, win32con.SW_RESTORE)
        
        # Bring to foreground
        win32gui.SetForegroundWindow(target_window_hwnd)
        
        # Give it a moment to process
        time.sleep(0.1)
        
        # Verify it's now the foreground window
        current_foreground = win32gui.GetForegroundWindow()
        if current_foreground == target_window_hwnd:
            safe_print(f"Successfully focused target window: {target_window_title}")
            return True
        else:
            safe_print(f"Focus attempt may have failed. Current foreground: {win32gui.GetWindowText(current_foreground)}")
            return False
            
    except Exception as e:
        safe_print(f"Error focusing target window: {str(e)}")
        return False

def run_manual_trigger_mode(simulation_dictionary):
    """Run manual trigger mode where user can test actions manually"""
    safe_print("Manual trigger mode started")
    
    print("\n" + "="*60)
    print("MANUAL TRIGGER MODE")
    print("="*60)
    print("Available triggers:")
    
    triggers = list(simulation_dictionary.keys())
    for i, trigger in enumerate(triggers[:15], 1):  # Show first 15
        action = simulation_dictionary[trigger]
        print(f"{i:2d}. '{trigger}' -> '{action}'")
    
    print("="*60)
    print("Commands:")
    print("  - Enter trigger number to execute action")
    print("  - Type 'list' to show triggers again")
    print("  - Type 'q' to quit")
    print("="*60)
    
    while True:
        choice = input("\nEnter command: ").strip().lower()
        
        if choice == 'q':
            safe_print("Manual trigger mode ended")
            break
        elif choice == 'list':
            print("\nAvailable triggers:")
            for i, trigger in enumerate(triggers[:15], 1):
                action = simulation_dictionary[trigger]
                print(f"{i:2d}. '{trigger}' -> '{action}'")
            continue
        
        try:
            trigger_idx = int(choice) - 1
            if 0 <= trigger_idx < len(triggers):
                trigger = triggers[trigger_idx]
                action = simulation_dictionary[trigger]
                
                print(f"\nSelected: '{trigger}' -> '{action}'")
                print("Make sure ExtP window is ready to receive the action...")
                confirm = input("Execute this action? (y/n): ").strip().lower()
                
                if confirm == 'y':
                    safe_print(f"Executing action: {action}")
                    perform_action(action)
                    log_simulation_event(trigger, action)
                    print("✓ Action executed!")
            else:
                print("Invalid choice! Enter a number from the list.")
        except ValueError:
            print("Invalid input! Enter a number, 'list', or 'q'.")
        except Exception as e:
            safe_print(f"Error executing action: {e}")

def main():
    """Main function to run the CUS system"""
    try:
        print("=== CUS STARTING UP ===", flush=True)
        safe_print("Starting CLI User Simulator with Screen Capture...")
        
        # Add startup delay as suggested
        safe_print("Initializing... (3 second delay)")
        # TEMPORARILY DISABLED FOR DEBUGGING
        # time.sleep(3)
        safe_print("✓ Sleep completed")
        
        safe_print("Using screen capture + OCR for monitoring")
        if ENABLE_ERROR_DETECTION:
            safe_print("Smart error detection: ENABLED - will detect real errors, ignore menu text")
        else:
            safe_print("Error detection: DISABLED")
        
        # Create required directories
        safe_print("Creating directories...")
        safe_print(f"NEW_ERRORS_PATH: {NEW_ERRORS_PATH}")
        safe_print(f"SIMULATION_EVENTS_PATH: {SIMULATION_EVENTS_PATH}")
        safe_print(f"SCREENSHOTS_PATH: {SCREENSHOTS_PATH}")
        os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
        safe_print("✓ NEW_ERRORS_PATH created")
        os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
        safe_print("✓ SIMULATION_EVENTS_PATH created")
        os.makedirs(SCREENSHOTS_PATH, exist_ok=True)
        safe_print("✓ SCREENSHOTS_PATH created")
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
        
        safe_print("External program launch completed.")
        
        # Initialize IssuePromptGenerator with external program path
        external_program_path = r"C:\Users\gibea\Documents\GitRepos\DeFiHuddleTradingSystem"
        # TEMPORARILY DISABLED FOR DEBUGGING - THESE MIGHT BE CAUSING THE HANG
        # initialize_issue_prompt_generator(external_program_path)
        
        # Test defect prompt generation
        # TEMPORARILY DISABLED FOR DEBUGGING
        # test_defect_prompt_generation()
        
        # List available windows for debugging
        safe_print("Listing available windows...")
        # TEMPORARILY DISABLED FOR DEBUGGING
        # list_available_windows()
        
        # NEW WORKFLOW: Simple Alt+Tab focus approach - STREAMLINED
        print("\n" + "="*60, flush=True)
        print("WINDOW FOCUS SETUP", flush=True)
        print("="*60, flush=True)
        print("CUS will use the Simple Alt+Tab method for reliable focusing.", flush=True)
        print("Please ensure the External Program (ExtP) is running before proceeding.", flush=True)
        print("="*60, flush=True)
        
        # Force simple mode - this was the DECISION made
        safe_print("Using Simple Alt+Tab mode (as decided).")
        setup_success = prompt_user_for_focus_and_switch()
        
        if setup_success:
            # Set a flag to use Alt+Tab for focusing
            global use_alt_tab_focus
            use_alt_tab_focus = True
            safe_print("Simple Alt+Tab focus setup complete.")
            
            # IMPORTANT: Give user a moment to see the confirmation while ExtP is focused
            print("\nCUS will now start monitoring in 3 seconds...", flush=True)
            print("ExtP should remain focused and ready to receive keystrokes.", flush=True)
            print("3...", flush=True)
            time.sleep(1)
            print("2...", flush=True)
            time.sleep(1)
            print("1...", flush=True)
            time.sleep(1)
            print("Starting monitoring now!", flush=True)
            
        else:
            safe_print("Focus setup failed or was cancelled. Exiting.")
            return
        
        # Start monitoring immediately - no additional prompts that break focus
        safe_print("Starting automatic OCR monitoring mode...")
        
        try:
            # Screen capture mode
            safe_print("Running in screen capture mode")
            safe_print("CUS is now actively monitoring the screen for triggers...")
            safe_print("ExtP should be focused and ready to receive simulated keystrokes")
            safe_print("Press Ctrl+C to stop monitoring")
            safe_print("Type 'manual' during monitoring to switch to manual trigger mode")
            safe_print("="*60)
            
            loop_count = 0
            previous_text = ""
            last_dict_reload_time = time.time()
            start_time = time.time()
            
            while True:
                time.sleep(POLL_INTERVAL)
                loop_count += 1
                current_time = time.time()
                elapsed_minutes = (current_time - start_time) / 60
                
                # Show periodic status with timestamp
                if loop_count % 10 == 0:  # Every 30 seconds (3s * 10)
                    safe_print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring active - Loop {loop_count} ({elapsed_minutes:.1f} min elapsed)")
                elif loop_count % 5 == 0:  # Every 15 seconds, show a dot
                    print(".", end="", flush=True)
                
                # Reload simulation dictionary every 5 minutes (300 seconds)
                if current_time - last_dict_reload_time >= 300:
                    safe_print(f"[{datetime.now().strftime('%H:%M:%S')}] Reloading simulation dictionary...")
                    simulation_dictionary = load_simulation_dictionary()
                    last_dict_reload_time = current_time
                    safe_print(f"Dictionary reloaded with {len(simulation_dictionary)} rules")
                
                # Check for error folder - only pause if NEW errors are detected
                # Skip error folder monitoring if error detection is disabled
                if ENABLE_ERROR_DETECTION:
                    error_files = []
                    if os.path.exists(NEW_ERRORS_PATH):
                        error_files = os.listdir(NEW_ERRORS_PATH)
                    
                    # Track error files to avoid repeated pausing
                    if not hasattr(main, 'known_error_files'):
                        main.known_error_files = set()
                    
                    new_error_files = set(error_files) - main.known_error_files
                    
                    if new_error_files:
                        safe_print(f"[{datetime.now().strftime('%H:%M:%S')}] {len(new_error_files)} new error files detected")
                        for error_file in new_error_files:
                            safe_print(f"  - {error_file}")
                        main.known_error_files.update(new_error_files)
                        # Only pause for truly new errors, not old ones
                        safe_print("Pausing for 5 seconds for new errors...")
                        time.sleep(5)
                
                # Capture and process screen
                previous_text = capture_and_process_screen(simulation_dictionary, previous_text)
                        
        except KeyboardInterrupt:
            safe_print("Interrupted by user. Stopping CUS...")
        finally:
            if process and process != "dummy_process":
                safe_print("Terminating external program...")
                process.terminate()
                
    except Exception as e:
        safe_print(f"Critical error in main: {e}")
        import traceback
        safe_print(f"Traceback: {traceback.format_exc()}")
        
        # Generate defect prompt for critical errors
        if ISSUE_PROMPT_AVAILABLE:
            try:
                issue_generator = IssuePromptGenerator(
                    project_root=external_program_path,
                    component_name="CUS_Main",
                    log_file_path=os.path.join(NEW_ERRORS_PATH, "critical_error.log")
                )
                
                with open(os.path.join(NEW_ERRORS_PATH, "critical_error.log"), 'w') as f:
                    f.write(f"Critical error in CUS main function: {str(e)}\n")
                    f.write(f"Traceback: {traceback.format_exc()}\n")
                
                defect_prompt = issue_generator.generate_defect_prompt(
                    error_description=f"Critical error in CUS main function: {str(e)}",
                    failure_type=FailureType.RUNTIME_ERROR,
                    severity=IssueSeverity.CRITICAL,
                    steps_to_reproduce=["1. Start CUS", "2. Error occurs during initialization"],
                    expected_behavior="CUS should start successfully and begin monitoring",
                    actual_behavior=f"CUS crashed with error: {str(e)}"
                )
                
                safe_print(f"Generated defect prompt for critical error: {defect_prompt}")
                
            except Exception as prompt_error:
                safe_print(f"Could not generate defect prompt: {prompt_error}")
        
        raise
        
    except Exception as e:
        safe_print(f"Error in main function: {e}")
        import traceback
        safe_print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    print("=== CUS PYTHON SCRIPT STARTING ===", flush=True)
    print("[CUS] Script is being executed directly", flush=True)
    print("[CUS] *** RUNNING THE CORRECTED CUS.PY WITH ALT+TAB FOCUS ***", flush=True)
    print("[CUS] *** NO AUTO-RELOAD THREAD - FOCUS WORKFLOW ENABLED ***", flush=True)
    
    try:
        print("[CUS] About to call main()", flush=True)
        main()
        print("[CUS] Main function completed", flush=True)
    except Exception as e:
        print(f"[CUS] Fatal error: {e}", flush=True)
        import traceback
        print(f"[CUS] Traceback: {traceback.format_exc()}", flush=True)
        exit(1)
