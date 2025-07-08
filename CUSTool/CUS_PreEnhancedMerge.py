#!/usr/bin/env python3
"""
CLI User Simulator (CUS) - Clean Baseline Version
Production-ready version with proven Alt+Tab focusing
"""

print("=== CUS STARTING - IMPORT PHASE ===", flush=True)
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
import ctypes
print("ctypes imported", flush=True)
import traceback
print("traceback imported", flush=True)
import json
print("json imported", flush=True)

# Import required system modules
try:
    import psutil
    import pyautogui
    from PIL import ImageGrab
    import pyperclip
    print("System modules imported successfully", flush=True)
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
    import pytesseract
    from PIL import Image, ImageGrab
    
    # Configure pytesseract path - try common Windows locations
    tesseract_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\gibea\AppData\Local\Microsoft\WinGet\Packages\UB-Mannheim.TesseractOCR_Microsoft.Winget.Source_8wekyb3d8bbwe\tesseract.exe"
    ]
    
    tesseract_found = False
    for path in tesseract_paths:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            tesseract_found = True
            print(f"OCR libraries imported successfully - Tesseract found at: {path}", flush=True)
            break
    
    if not tesseract_found:
        print("OCR libraries imported - Tesseract not found in common locations, OCR may fail", flush=True)
    
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

# Global variables for action tracking
last_action_time = 0
last_action_type = ""
action_repeat_count = 0

# Global IssuePromptGenerator instance
issue_prompt_generator = None

def load_simulation_dictionary():
    """Load simulation dictionary from a configuration file"""
    if not os.path.exists(SIMULATION_DICTIONARY_FILE):
        return {}
    
    with open(SIMULATION_DICTIONARY_FILE, "r") as file:
        try:
            return json.load(file)  # Load dictionary from JSON format
        except json.JSONDecodeError:
            safe_print("Error: Invalid JSON format in simulation dictionary file.")
            return {}

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

def focus_using_alt_tab():
    """Focus on the external program window using Alt+Tab"""
    try:
        # Use Alt+Tab to switch to the next window - correct pynput syntax
        keyboard.press(Key.alt)
        keyboard.press(Key.tab)
        time.sleep(0.1)  # Brief hold
        keyboard.release(Key.tab)
        keyboard.release(Key.alt)
        time.sleep(0.5)  # Brief pause for window switch
        return True
    except Exception as e:
        safe_print(f"[ERROR] Failed to switch windows with Alt+Tab: {e}")
        return False

def prompt_user_for_focus_and_switch():
    """Prompt user to focus on the external program and confirm setup"""
    try:
        print("\n" + "="*60)
        print("IMPORTANT: Please ensure the External Program is focused!")
        print("="*60)
        print("1. Click on the External Program window to focus it")
        print("2. The External Program should be visible and ready to receive input")
        print("3. Press Enter here when ready...")
        print("="*60)
        
        # Wait for user confirmation
        input("Press Enter when the External Program is focused and ready: ")
        
        # Give a moment for the user to see the confirmation
        time.sleep(1)
        
        return True
    except Exception as e:
        safe_print(f"[ERROR] Failed during focus setup: {e}")
        return False

def send_key_multiple_methods(key, key_name):
    """Send a key using fallback methods for maximum reliability"""
    safe_print(f"🔄 ATTEMPTING TO SEND KEY: {key_name} using multiple methods...")
    
    # Method 1: pynput keyboard - PRIMARY
    try:
        safe_print(f"📤 METHOD 1: Sending {key_name} via pynput...")
        keyboard.press(key)
        keyboard.release(key)
        safe_print(f"✅ METHOD 1 SUCCESS: {key_name} sent via pynput")
        return True  # Success - don't try other methods
    except Exception as e:
        safe_print(f"❌ METHOD 1 FAILED: pynput error - {e}")
    
    # Method 2: pyautogui - FALLBACK 1
    try:
        safe_print(f"📤 METHOD 2: Sending {key_name} via pyautogui...")
        if key == Key.enter:
            pyautogui.press('enter')
        elif key == Key.space:
            pyautogui.press('space')
        elif key == Key.esc:
            pyautogui.press('esc')
        safe_print(f"✅ METHOD 2 SUCCESS: {key_name} sent via pyautogui")
        return True  # Success - don't try Windows API method
    except Exception as e:
        safe_print(f"❌ METHOD 2 FAILED: pyautogui error - {e}")
    
    # Method 3: Windows API - FALLBACK 2
    try:
        safe_print(f"📤 METHOD 3: Sending {key_name} via Windows API...")
        
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
            safe_print(f"✅ METHOD 3 SUCCESS: {key_name} sent via Windows API")
            return True
        else:
            safe_print(f"❌ METHOD 3 FAILED: No Windows API mapping for {key_name}")
            return False
    except Exception as e:
        safe_print(f"❌ METHOD 3 FAILED: Windows API error - {e}")
    
    safe_print(f"🚨 ALL METHODS FAILED: Could not send {key_name}")
    return False

def send_text_multiple_methods(text):
    """Send text using fallback methods for maximum reliability"""
    safe_print(f"🔄 ATTEMPTING TO SEND TEXT: '{text}' using multiple methods...")
    
    # Method 1: pynput keyboard (character by character) - PRIMARY
    try:
        safe_print(f"📤 METHOD 1: Sending text '{text}' via pynput...")
        for char in text:
            keyboard.type(char)
            time.sleep(0.05)  # Small delay between characters
        safe_print(f"✅ METHOD 1 SUCCESS: Text '{text}' sent via pynput")
        return True  # Success - don't try other methods
    except Exception as e:
        safe_print(f"❌ METHOD 1 FAILED: pynput error - {e}")
    
    # Method 2: pyautogui typewrite - FALLBACK 1
    try:
        safe_print(f"📤 METHOD 2: Sending text '{text}' via pyautogui...")
        pyautogui.typewrite(text, interval=0.05)
        safe_print(f"✅ METHOD 2 SUCCESS: Text '{text}' sent via pyautogui")
        return True  # Success - don't try clipboard method
    except Exception as e:
        safe_print(f"❌ METHOD 2 FAILED: pyautogui error - {e}")
    
    # Method 3: Windows clipboard + Ctrl+V - FALLBACK 2
    try:
        pyperclip.copy(text)
        time.sleep(0.1)
        
        # Send Ctrl+V
        ctypes.windll.user32.keybd_event(0x11, 0, 0, 0)  # Ctrl down
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(0x56, 0, 0, 0)  # V down
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(0x56, 0, 2, 0)  # V up
        ctypes.windll.user32.keybd_event(0x11, 0, 2, 0)  # Ctrl up
        
        safe_print(f"✅ Method 3 (Clipboard): Text '{text}' sent successfully")
        return True  # Success
    except Exception as e:
        safe_print(f"❌ Method 3 (Clipboard) failed: {e}")
    
    # All methods failed
    safe_print(f"❌ ALL TEXT INPUT METHODS FAILED for '{text}'")
    return False

def perform_action(action):
    """Perform the specified action with multiple input methods for reliability"""
    safe_print(f"🎮 STARTING ACTION: {action}")
    
    # Add a small delay before performing action to ensure target window is ready
    time.sleep(0.5)
    
    # Focus on the external program window using Alt+Tab
    focus_success = False
    for attempt in range(3):  # Reduced attempts since Alt+Tab is simpler
        safe_print(f"🎯 FOCUS ATTEMPT {attempt + 1}/3: Switching to ExtP window...")
        safe_print("⌨️  EXECUTING: Alt+Tab to switch to ExtP...")
        focus_result = focus_using_alt_tab()
            
        if focus_result:
            focus_success = True
            safe_print(f"✅ FOCUS SUCCESS: ExtP window focused on attempt {attempt + 1}")
            break
        time.sleep(1)  # Brief wait between retry attempts
    
    if not focus_success:
        safe_print("🚨 FOCUS FAILURE: Could not focus external program window!")
        safe_print("⚠️  WARNING: Keys will be sent to whatever window is currently active")
        safe_print("📋 RECOMMENDATION: Please manually focus on ExtP window if this continues")
    
    # Add extra delay after focusing attempt
    time.sleep(1)
    
    if action == "press_enter":
        # Multi-method approach for Enter key
        safe_print("⌨️  SENDING INPUT: Enter key")
        send_key_multiple_methods(Key.enter, "Enter")
    elif action == "press_space":
        safe_print("⌨️  SENDING INPUT: Space key")
        send_key_multiple_methods(Key.space, "Space")
    elif action == "press_escape":
        safe_print("⌨️  SENDING INPUT: Escape key")
        send_key_multiple_methods(Key.esc, "Escape")
    elif action.startswith("type_"):
        text = action[5:]  # Extract text after "type_"
        safe_print(f"⌨️  SENDING INPUT: Typing '{text}' followed by Enter")
        safe_print(f"📝 INPUT DETAILS: Text='{text}', Length={len(text)} characters")
        
        # Multi-method approach for typing
        send_text_multiple_methods(text)
        
        # Press Enter after typing using multiple methods
        time.sleep(0.5)
        safe_print("⌨️  SENDING INPUT: Enter key (after typing)")
        send_key_multiple_methods(Key.enter, "Enter")
        safe_print(f"✅ INPUT COMPLETE: Successfully sent '{text}' + Enter")
    elif action == "wait_random":
        wait_time = random.randint(1, 5)
        safe_print(f"⏳ WAITING: {wait_time} seconds (random delay)")
        time.sleep(wait_time)
        safe_print(f"✅ WAIT COMPLETE: Waited {wait_time} seconds")
    else:
        safe_print(f"❌ UNKNOWN ACTION: {action}")
    
    # Verify action was effective by checking if we should wait for screen change
    safe_print(f"✅ ACTION COMPLETED: '{action}' - Waiting for screen response...")
    time.sleep(1)  # Give time for the action to take effect

def process_screen_content(simulation_dictionary, current_text, previous_text):
    """Process screen content for triggers"""
    global last_action_time, last_action_type, action_repeat_count
    
    if not current_text:
        return
    
    # Check if content has changed
    if current_text == previous_text:
        return  # No change, skip processing
    
    safe_print(f"📊 SCREEN CONTENT CHANGED: New text length: {len(current_text)}")
    
    # Extract last MAX_LOG_SIZE characters for processing
    if len(current_text) > MAX_LOG_SIZE:
        text_to_process = current_text[-MAX_LOG_SIZE:]
    else:
        text_to_process = current_text
    
    # PRIORITY 1: Check for simulation triggers (ExtP waiting for input) FIRST
    for trigger, action in simulation_dictionary.items():
        if trigger.lower() in text_to_process.lower():
            safe_print(f"🎯 TRIGGER DETECTED: '{trigger}'")
            safe_print(f"🎮 PREPARING TO EXECUTE ACTION: '{action}'")
            
            # Check for repetitive actions (indicating action failure)
            current_time = time.time()
            if action == last_action_type and (current_time - last_action_time) < 30:  # Same action within 30 seconds
                action_repeat_count += 1
                if action_repeat_count >= 3:  # 3 repetitions indicate failure
                    safe_print(f"🚨 ACTION FAILURE DETECTED: '{action}' repeated {action_repeat_count} times")
                    safe_print(f"🔥 GENERATING DEFECT PROMPT FOR ACTION FAILURE")
                    generate_action_failure_prompt(trigger, action, text_to_process)
                    action_repeat_count = 0  # Reset counter
                    return
            else:
                action_repeat_count = 0  # Reset if different action or too much time passed
            
            last_action_time = current_time
            last_action_type = action
            
            # Store screen content before action for comparison
            screen_before_action = text_to_process
            
            # Execute action
            safe_print(f"🎮 EXECUTING ACTION: {action}")
            perform_action(action)
            
            log_simulation_event(trigger, action)
            
            # Wait and capture screen after action to detect if it was effective
            time.sleep(2)  # Wait longer to see if action took effect
            screenshot_after, screenshot_path_after = capture_screen()
            if screenshot_after:
                screen_after_action = extract_text_from_image(screenshot_after)
                if screen_after_action:
                    # Check if the action was effective
                    if trigger.lower() in screen_after_action.lower():
                        safe_print(f"⚠️  ACTION EFFECTIVENESS WARNING: Same trigger '{trigger}' still present after action")
                        safe_print(f"📸 CAPTURING SCREENSHOT FOR ANALYSIS: {screenshot_path_after}")
                        generate_ineffective_action_prompt(trigger, action, screen_before_action, screen_after_action, screenshot_path_after)
                    else:
                        safe_print(f"✅ ACTION APPEARS EFFECTIVE: Trigger '{trigger}' no longer present")
                else:
                    safe_print(f"❌ OCR FAILED ON POST-ACTION SCREENSHOT: {screenshot_path_after}")
            
            return  # Only process first matching trigger
    
    # PRIORITY 2: Only check for errors if NO triggers found (ExtP not waiting for input)
    errors = ["error", "exception", "failed", "timeout", "critical"]
    for error in errors:
        if error.lower() in text_to_process.lower():
            safe_print(f"🚨 ERROR DETECTED: '{error}' found in screen content")
            
            # Capture screenshot for error documentation
            screenshot, screenshot_path = capture_screen()
            if screenshot_path:
                safe_print(f"📸 ERROR SCREENSHOT CAPTURED: {screenshot_path}")
                
                # Generate error ID
                error_id = f"ERROR_{int(time.time())}"
                safe_print(f"🆔 ERROR ID GENERATED: {error_id}")
                
                # Log error event with ID
                log_error_event(error, text_to_process, error_id, screenshot_path)
                
                # Generate defect prompt for error
                generate_error_defect_prompt(error, text_to_process, error_id, screenshot_path)
            else:
                safe_print(f"❌ FAILED TO CAPTURE ERROR SCREENSHOT")
            
            return

def log_error_event(error, screen_content, error_id=None, screenshot_path=None):
    """Log error events to a file"""
    timestamp = int(time.time())
    error_id = error_id or f"ERROR_{timestamp}"
    error_filename = f"CUS_error_event_{timestamp}.txt"
    error_filepath = os.path.join(NEW_ERRORS_PATH, error_filename)
    
    # Enhanced logging with ID and screenshot
    safe_print(f"📝 LOGGING ERROR EVENT: {error_id}")
    safe_print(f"🔍 ERROR TYPE: {error}")
    safe_print(f"📊 SCREEN CONTENT LENGTH: {len(screen_content)} characters")
    if screenshot_path:
        safe_print(f"📸 SCREENSHOT: {screenshot_path}")
    
    # Ensure directory exists
    os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
    
    with open(error_filepath, "w") as error_file:
        error_file.write(f"Error ID: {error_id}\n")
        error_file.write(f"Error: {error}\n")
        error_file.write(f"Timestamp: {timestamp}\n")
        if screenshot_path:
            error_file.write(f"Screenshot: {screenshot_path}\n")
        error_file.write(f"Screen Content:\n{screen_content}")
    
    safe_print(f"💾 ERROR LOGGED TO: {error_filepath}")

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

def launch_external_program():
    """Launch the external program - COMMENTED OUT FOR DEBUGGING"""
    safe_print("External program launch is disabled.")
    safe_print("Please start your external program manually before running CUS.")
    return "dummy_process"  # Return something so we don't exit

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

def generate_action_failure_prompt(trigger, action, screen_content):
    """Generate defect prompt for action failures"""
    if issue_prompt_generator:
        try:
            from IssuePromptGenerator import TestCaseContext, DocumentationReference
            safe_print(f"📄 GENERATING DEFECT PROMPT FOR ACTION FAILURE: {action}")
            
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
            safe_print(f"💾 DEFECT PROMPT SAVED: {prompt_obj.issue_id} at {saved_path}")
            
        except Exception as e:
            safe_print(f"❌ ERROR GENERATING ACTION FAILURE PROMPT: {e}")

def generate_error_defect_prompt(error, screen_content, error_id, screenshot_path):
    """Generate defect prompt for detected errors"""
    if issue_prompt_generator:
        try:
            from IssuePromptGenerator import TestCaseContext, DocumentationReference
            safe_print(f"📄 GENERATING DEFECT PROMPT FOR ERROR: {error}")
            
            test_context = TestCaseContext(
                test_case_name="Error Detection",
                test_sequence_id=f"ERROR_DETECTION_{error_id}",
                expected_behavior="ExtP should operate without errors",
                actual_behavior=f"Error detected: {error}",
                failure_step=1,
                reproduction_steps=[
                    "Run CUS monitoring",
                    "Wait for ExtP operation",
                    f"Error '{error}' appears on screen",
                    "Error captured and logged"
                ],
                documentation_refs=[
                    DocumentationReference(
                        file_path="ExtP_ErrorHandling.md",
                        reference_type="requirement",
                        reference_id="EXTP-ERR",
                        section_title="Error Handling Requirements"
                    )
                ],
                related_test_cases=["ExtP Error Handling Tests"],
                dependency_chain=["CUS", "ExtP", "Error Detection"]
            )
            
            prompt_obj = issue_prompt_generator.generate_issue_prompt(
                test_case_context=test_context,
                error_context={
                    "error_type": "external_program_error",
                    "error_message": f"Error '{error}' detected in screen content",
                    "error_id": error_id,
                    "screen_content": screen_content[:1000],
                    "screenshot_path": screenshot_path
                }
            )
            
            saved_path = issue_prompt_generator.save_issue_prompt(prompt_obj)
            safe_print(f"💾 ERROR DEFECT PROMPT SAVED: {prompt_obj.issue_id} at {saved_path}")
            
        except Exception as e:
            safe_print(f"❌ ERROR GENERATING ERROR DEFECT PROMPT: {e}")

def generate_ineffective_action_prompt(trigger, action, screen_before, screen_after, screenshot_path):
    """Generate defect prompt when action appears ineffective"""
    if issue_prompt_generator:
        try:
            from IssuePromptGenerator import TestCaseContext, DocumentationReference
            safe_print(f"📄 GENERATING DEFECT PROMPT FOR INEFFECTIVE ACTION: {action}")
            
            test_context = TestCaseContext(
                test_case_name="Action Ineffectiveness",
                test_sequence_id=f"INEFFECTIVE_ACTION_{int(time.time())}",
                expected_behavior=f"Action '{action}' should remove trigger '{trigger}' from screen",
                actual_behavior=f"Trigger '{trigger}' still present after action '{action}' was performed",
                failure_step=1,
                reproduction_steps=[
                    f"Wait for trigger: {trigger}",
                    f"Perform action: {action}",
                    "Check screen content",
                    "Trigger still present - action was ineffective"
                ],
                documentation_refs=[
                    DocumentationReference(
                        file_path="simulation_dictionary.txt",
                        reference_type="requirement",
                        reference_id="CUS-DICT",
                        section_title="CUS Action Dictionary"
                    )
                ],
                related_test_cases=["CUS Action Effectiveness Tests"],
                dependency_chain=["CUS", "ExtP", "Screen Detection"]
            )
            
            prompt_obj = issue_prompt_generator.generate_issue_prompt(
                test_case_context=test_context,
                error_context={
                    "error_type": "ineffective_action",
                    "error_message": f"Action '{action}' did not remove trigger '{trigger}' from screen",
                    "trigger": trigger,
                    "screen_before": screen_before[:300],
                    "screen_after": screen_after[:300],
                    "screenshot_path": screenshot_path
                }
            )
            
            saved_path = issue_prompt_generator.save_issue_prompt(prompt_obj)
            safe_print(f"💾 DEFECT PROMPT SAVED: {prompt_obj.issue_id} at {saved_path}")
            
        except Exception as e:
            safe_print(f"❌ ERROR GENERATING INEFFECTIVE ACTION PROMPT: {e}")

def main():
    """Main function to run the CUS system"""
    try:
        print("=== CUS STARTING UP ===", flush=True)
        safe_print("Starting CLI User Simulator with Screen Capture...")
        
        # Add startup delay as suggested
        safe_print("Initializing... (3 second delay)")
        time.sleep(3)
        safe_print("✓ Sleep completed")
        
        safe_print("Using screen capture + OCR for monitoring")
        
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
        safe_print("🔧 INITIALIZING ISSUE PROMPT GENERATOR...")
        initialize_issue_prompt_generator(external_program_path)
        safe_print("✅ ISSUE PROMPT GENERATOR READY FOR DEFECT PROMPT GENERATION")
        
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
                
                # Check for error folder - if errors exist, pause briefly and continue
                if os.path.exists(NEW_ERRORS_PATH) and os.listdir(NEW_ERRORS_PATH):
                    safe_print(f"[{datetime.now().strftime('%H:%M:%S')}] NewErrorsPath contains errors. Pausing for 10 seconds...")
                    time.sleep(10)
                    # Check again after pause
                    if os.path.exists(NEW_ERRORS_PATH) and os.listdir(NEW_ERRORS_PATH):
                        safe_print("NewErrorsPath still contains errors after pause - continuing monitoring")
                    else:
                        safe_print("NewErrorsPath cleared - resuming normal monitoring")
                
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
        safe_print(f"Traceback: {traceback.format_exc()}")
        raise

if __name__ == "__main__":
    print("=== CUS PYTHON SCRIPT STARTING ===", flush=True)
    print("[CUS] Script is being executed directly", flush=True)
    
    try:
        print("[CUS] About to call main()", flush=True)
        main()
        print("[CUS] Main function completed", flush=True)
    except Exception as e:
        print(f"[CUS] Fatal error: {e}", flush=True)
        print(f"[CUS] Traceback: {traceback.format_exc()}", flush=True)
        exit(1)
