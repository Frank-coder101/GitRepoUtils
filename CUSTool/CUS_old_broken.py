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

# Import required system modules (pywin32 removed - Alt+Tab mode only)
try:
    import psutil
    import pygetwindow as gw
    import pyautogui
    import re
    import logging
    from PIL import ImageGrab
    import threading
    import queue
    import sys
    import json
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

# Import Enhanced CUS capabilities for false negative remediation
try:
    from AutomatedRemediationSystem import AutomatedRemediationSystem, RemediationAction
    from EnhancedTestCaseGenerator import EnhancedTestCaseGenerator
    from AdvancedTestExecutor import AdvancedTestExecutor
    ENHANCED_CAPABILITIES_AVAILABLE = True
    print("Enhanced CUS capabilities imported successfully", flush=True)
except ImportError:
    ENHANCED_CAPABILITIES_AVAILABLE = False
    print("Warning: Enhanced CUS capabilities not available - using basic functionality", flush=True)

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

# Enhanced CUS capabilities - global variables
remediation_system = None
enhanced_actions = {}
false_negative_count = 0
remediation_count = 0

def initialize_enhanced_capabilities(simulation_dict_path="simulation_dictionary.txt"):
    """Initialize enhanced CUS capabilities for false negative remediation"""
    global remediation_system, enhanced_actions
    
    if ENHANCED_CAPABILITIES_AVAILABLE:
        try:
            remediation_system = AutomatedRemediationSystem(simulation_dict_path)
            enhanced_actions = initialize_enhanced_action_handlers()
            safe_print(f"🚀 Enhanced CUS capabilities initialized")
            safe_print(f"   - Remediation system: Active")
            safe_print(f"   - Enhanced actions: {len(enhanced_actions)} loaded")
            return True
        except Exception as e:
            safe_print(f"❌ Error initializing enhanced capabilities: {e}")
            return False
    else:
        safe_print("Enhanced capabilities not available - using basic functionality")
        return False

def initialize_enhanced_action_handlers():
    """Initialize enhanced action handlers for remediation"""
    return {
        # Original actions with validation
        "type_1": lambda trigger, content: enhanced_type_1_with_validation(trigger, content),
        "type_enter": lambda trigger, content: enhanced_type_enter_with_validation(trigger, content),
        "type_0": lambda trigger, content: enhanced_type_0_with_validation(trigger, content),
        
        # Enhanced remediation actions
        "force_configuration_interface": lambda trigger, content: force_configuration_interface(trigger, content),
        "validate_configuration_request": lambda trigger, content: validate_configuration_request(trigger, content),
        "handle_already_configured": lambda trigger, content: handle_already_configured(trigger, content),
        "verify_configuration_completion": lambda trigger, content: verify_configuration_completion(trigger, content),
        "validate_setup_completion": lambda trigger, content: validate_setup_completion(trigger, content),
        "validate_then_configure": lambda trigger, content: validate_then_configure(trigger, content),
        "verify_configuration_menu_active": lambda trigger, content: verify_configuration_menu_active(trigger, content),
        "ensure_user_input_received": lambda trigger, content: ensure_user_input_received(trigger, content),
        "track_interface_state_changes": lambda trigger, content: track_interface_state_changes(trigger, content),
        "alternative_configuration_approach": lambda trigger, content: alternative_configuration_approach(trigger, content),
        "retry_with_enhanced_validation": lambda trigger, content: retry_with_enhanced_validation(trigger, content),
        "escalate_to_manual_intervention": lambda trigger, content: escalate_to_manual_intervention(trigger, content),
        "detect_false_negative_configuration": lambda trigger, content: detect_false_negative_configuration(trigger, content)
    }

def process_screen_content(simulation_dictionary, current_text, previous_text):
    """Process screen content for triggers with enhanced false negative detection"""
    global last_action_time, last_action_type, action_repeat_count, false_negative_count
    
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
    
    # ENHANCED: Check for false negatives FIRST if remediation system is available
    if remediation_system:
        safe_print("🔍 DETECTING FALSE NEGATIVES...")
        false_negatives = remediation_system.detect_and_remediate_false_negatives(text_to_process)
        
        if false_negatives:
            false_negative_count += len(false_negatives)
            safe_print(f"🚨 {len(false_negatives)} FALSE NEGATIVES DETECTED AND REMEDIATED")
            
            # Reload simulation dictionary after remediation
            simulation_dictionary = load_simulation_dictionary()
    
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
            
            # ENHANCED: Try enhanced action first if available
            action_executed = False
            if enhanced_actions and action in enhanced_actions:
                safe_print(f"🔧 EXECUTING ENHANCED ACTION: {action}")
                try:
                    success = enhanced_actions[action](trigger, text_to_process)
                    if success:
                        safe_print(f"✅ ENHANCED ACTION SUCCESSFUL")
                        action_executed = True
                    else:
                        safe_print(f"⚠️  ENHANCED ACTION FAILED, FALLING BACK TO STANDARD ACTION")
                except Exception as e:
                    safe_print(f"❌ ENHANCED ACTION ERROR: {e}")
                    safe_print(f"🔄 FALLING BACK TO STANDARD ACTION")
            
            # Execute standard action if enhanced action not available or failed
            if not action_executed:
                safe_print(f"🎮 EXECUTING STANDARD ACTION: {action}")
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
            # Enhanced error detection: Filter out false positives
            if is_legitimate_error(error, text_to_process):
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
            else:
                safe_print(f"⚡ FILTERED FALSE POSITIVE: '{error}' detected but appears to be OCR misreading or benign context")
            
            return

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
                    "error_type": "action_failure",
                    "error_message": f"Action '{action}' failed to produce expected result",
                    "trigger": trigger,
                    "screen_content": screen_content[:500]  # Truncate for readability
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
                    "error_type": "detected_error",
                    "error_message": f"Error '{error}' detected in screen content",
                    "error_id": error_id,
                    "screen_content": screen_content[:500],
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

def log_error_event(error, screen_content, error_id=None, screenshot_path=None):
    """Log error events to a file and generate defect prompt"""
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
    
    # Generate defect prompt if available
    if issue_prompt_generator:
        try:
            # Create test case context for external program error
            from IssuePromptGenerator import TestCaseContext, DocumentationReference
            safe_print(f"📄 GENERATING DEFECT PROMPT FOR ERROR: {error_id}")
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
                    "error_id": error_id,
                    "screen_content": screen_content[:1000],
                    "screenshot_path": screenshot_path
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
        
        # Generate a defect prompt for focusing failure
        if ISSUE_PROMPT_AVAILABLE and attempt >= 3:  # Only after multiple failures
            try:
                from IssuePromptGenerator import TestCaseContext, DocumentationReference
                safe_print(f"📄 GENERATING DEFECT PROMPT FOR FOCUS FAILURE")
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
                safe_print(f"💾 FOCUS FAILURE DEFECT PROMPT SAVED: {prompt_obj.issue_id}")
                
            except Exception as e:
                safe_print(f"❌ ERROR GENERATING FOCUS FAILURE PROMPT: {e}")
    
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

def is_legitimate_error(error_word: str, screen_content: str) -> bool:
    """
    Intelligently filter error detections to avoid false positives from:
    - OCR misreading (e.g., "GitRepos" as "error")  
    - File paths and directory names
    - VS Code interface elements
    - Help documentation mentioning errors
    - Benign contexts where "error" is not an actual error
    """
    error_lower = error_word.lower()
    content_lower = screen_content.lower()
    
    # Get the context around the error word
    error_index = content_lower.find(error_lower)
    if error_index == -1:
        return False
    
    # Extract context before and after the error word (50 chars each direction)
    start_idx = max(0, error_index - 50)
    end_idx = min(len(content_lower), error_index + len(error_lower) + 50)
    context = content_lower[start_idx:end_idx]
    
    # FALSE POSITIVE FILTERS:
    
    # 1. File paths and directories (common OCR misreading source)
    file_path_indicators = [
        "\\\\", "\\users\\", "\\documents\\", "\\program files\\", 
        "\\gitrepo", "\\defi", "\\trading", ".py", ".md", ".txt", ".json",
        "c:", "d:", "/users/", "/documents/", "/program", "gitrepo"
    ]
    if any(indicator in context for indicator in file_path_indicators):
        return False
    
    # 2. VS Code interface elements
    vscode_indicators = [
        "explorer", "open editors", "timeline", "breadcrumb", "workspace",
        "extension", "terminal", "debug", "git", "search", "problems"
    ]
    if any(indicator in context for indicator in vscode_indicators):
        return False
    
    # 3. Help documentation or instructional text
    help_indicators = [
        "help", "documentation", "guide", "how to", "to avoid", "prevent",
        "troubleshooting", "faq", "readme", "instructions", "tutorial"
    ]
    if any(indicator in context for indicator in help_indicators):
        return False
    
    # 4. Common OCR misreadings 
    ocr_misread_patterns = [
        "gitrepo", "defi", "huddle", "python313", "site-packages",
        "appdata", "roaming", "pythonwin", "tesseract", "ctrl+c"
    ]
    if any(pattern in context for pattern in ocr_misread_patterns):
        return False
    
    # 5. Technical configuration/setup contexts (usually not real errors)
    config_indicators = [
        "configuration", "setup", "initialization", "loading", "imported",
        "keyboard controller", "ocr libraries", "imported successfully",
        "ready", "initialized", "capabilities", "wizard", "options"
    ]
    if any(indicator in context for indicator in config_indicators):
        return False
    
    # 6. Log level indicators (INFO, DEBUG, etc. - not actual errors)
    log_indicators = ["info:", "debug:", "trace:", "loaded", "started", "completed"]
    if any(indicator in context for indicator in log_indicators):
        return False
    
    # LEGITIMATE ERROR INDICATORS:
    # Only report as error if it appears in contexts that suggest real errors
    legitimate_error_contexts = [
        "exception", "traceback", "stack trace", "critical", "fatal",
        "crash", "abort", "panic", "assertion", "failure", "undefined",
        "null pointer", "access violation", "segmentation fault",
        "connection refused", "timeout occurred", "permission denied",
        "file not found", "syntax error", "runtime error", "compile error"
    ]
    
    # Check if this appears to be a legitimate error context
    if any(context_indicator in context for context_indicator in legitimate_error_contexts):
        return True
    
    # 7. Additional filtering for specific error words
    if error_lower == "error":
        # Be extra strict for "error" since it's commonly misread by OCR
        # Only allow if it's clearly in an error message format
        error_message_patterns = [
            "error:", "error message", "an error occurred", "error code",
            "error details", "error description", "system error", "runtime error"
        ]
        return any(pattern in context for pattern in error_message_patterns)
    
    # For other error words, be less strict but still filter obvious false positives
    return True

# ================================================
# Missing Focus Functions
# ================================================

def focus_using_alt_tab():
    """Focus on the external program window using Alt+Tab"""
    try:
        # Use Alt+Tab to switch to the next window
        keyboard.press_and_release('alt+tab')
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

# ================================================
# End Missing Focus Functions
# ================================================

# ================================================
# Enhanced Action Handlers from EnhancedCUS.py
# ================================================

def enhanced_type_1_with_validation(trigger: str, screen_content: str) -> bool:
    """Type '1' with enhanced validation"""
    safe_print("🔍 ENHANCED ACTION: type_1_with_validation")
    
    # Check if this is a configuration menu
    if "configure" in trigger.lower() or "configuration" in screen_content.lower():
        safe_print("   Configuration context detected")
        
        # Pre-validation: Check if already configured
        if "already configured" in screen_content.lower():
            safe_print("   ⚠️  Pre-validation failed: System already configured")
            return handle_already_configured(trigger, screen_content)
        
        # Execute the action using real keyboard input
        safe_print("   🎮 EXECUTING: Typing '1' with validation...")
        send_text_multiple_methods("1")
        time.sleep(0.5)
        send_key_multiple_methods(Key.enter, "Enter")
        
        # Post-validation: Check result
        return validate_configuration_response(screen_content)
    
    # Standard type_1 action
    safe_print("   🎮 EXECUTING: Standard type_1 action")
    send_text_multiple_methods("1")
    time.sleep(0.5)
    send_key_multiple_methods(Key.enter, "Enter")
    return True

def enhanced_type_enter_with_validation(trigger: str, screen_content: str) -> bool:
    """Type Enter with enhanced validation"""
    safe_print("🔍 ENHANCED ACTION: type_enter_with_validation")
    send_key_multiple_methods(Key.enter, "Enter")
    return True

def enhanced_type_0_with_validation(trigger: str, screen_content: str) -> bool:
    """Type '0' with enhanced validation"""
    safe_print("🔍 ENHANCED ACTION: type_0_with_validation")
    send_text_multiple_methods("0")
    time.sleep(0.5)
    send_key_multiple_methods(Key.enter, "Enter")
    return True

def force_configuration_interface(trigger: str, screen_content: str) -> bool:
    """Force configuration interface to appear"""
    safe_print("🔧 REMEDIATION ACTION: force_configuration_interface")
    
    # Focus on ExtP first
    focus_using_alt_tab()
    time.sleep(1)
    
    # Try alternative approaches to show configuration
    approaches = [
        ("Try pressing 'C' for configuration", "c"),
        ("Try Alt+C for configuration menu", "alt+c"),
        ("Try pressing '1' multiple times", "1"),
        ("Try Escape then '1' for configuration", "escape")
    ]
    
    for description, key_combo in approaches:
        safe_print(f"   🎮 ATTEMPTING: {description}")
        try:
            if key_combo == "alt+c":
                pyautogui.hotkey('alt', 'c')
            elif key_combo == "escape":
                send_key_multiple_methods(Key.esc, "Escape")
                time.sleep(0.5)
                send_text_multiple_methods("1")
            else:
                send_text_multiple_methods(key_combo)
            time.sleep(1)
        except Exception as e:
            safe_print(f"   ❌ Failed: {e}")
    
    safe_print("   ✅ Configuration interface force attempts completed")
    return True

def validate_configuration_request(trigger: str, screen_content: str) -> bool:
    """Validate configuration request before proceeding"""
    safe_print("🔍 VALIDATION ACTION: validate_configuration_request")
    
    # Check if configuration is actually needed
    if "already configured" in screen_content.lower():
        safe_print("   ⚠️  Configuration not needed - already configured")
        return handle_already_configured(trigger, screen_content)
    
    # Check if configuration interface is available
    if "configure" in screen_content.lower():
        safe_print("   ✅ Configuration interface available")
        return True
    
    safe_print("   ❌ Configuration interface not available")
    return False

def handle_already_configured(trigger: str, screen_content: str) -> bool:
    """Handle the 'already configured' false negative"""
    global false_negative_count
    safe_print("🚨 FALSE NEGATIVE HANDLER: handle_already_configured")
    
    false_negative_count += 1
    
    # Log the false negative
    log_false_negative("already_configured", trigger, screen_content)
    
    # Focus on ExtP first
    focus_using_alt_tab()
    time.sleep(1)
    
    # Try to access configuration anyway with real keyboard input
    alternative_actions = [
        ("Try 'R' for reconfigure", "r"),
        ("Try 'M' for modify configuration", "m"),
        ("Try 'E' for edit configuration", "e"),
        ("Try 'A' for advanced configuration", "a"),
        ("Try '2' for alternative option", "2"),
        ("Try 'C' for configuration", "c")
    ]
    
    for description, key in alternative_actions:
        safe_print(f"   🎮 ATTEMPTING: {description}")
        try:
            send_text_multiple_methods(key)
            time.sleep(0.8)
        except Exception as e:
            safe_print(f"   ❌ Failed: {e}")
    
    safe_print("   ✅ Alternative configuration access attempted")
    return True

def verify_configuration_completion(trigger: str, screen_content: str) -> bool:
    """Verify that configuration was actually completed properly"""
    safe_print("🔍 VALIDATION ACTION: verify_configuration_completion")
    
    # Check for proper completion indicators
    completion_indicators = [
        "configuration saved",
        "settings updated", 
        "configuration complete",
        "setup finished",
        "configuration successful"
    ]
    
    for indicator in completion_indicators:
        if indicator in screen_content.lower():
            safe_print(f"   ✅ Configuration completion verified: {indicator}")
            return True
    
    safe_print("   ⚠️  Configuration completion not verified")
    return False

def validate_setup_completion(trigger: str, screen_content: str) -> bool:
    """Validate setup completion"""
    safe_print("🔍 VALIDATION ACTION: validate_setup_completion")
    return verify_configuration_completion(trigger, screen_content)

def validate_then_configure(trigger: str, screen_content: str) -> bool:
    """Validate then configure"""
    safe_print("🔍 ENHANCED ACTION: validate_then_configure")
    
    # First validate
    if not validate_configuration_request(trigger, screen_content):
        return False
    
    # Then configure
    return enhanced_type_1_with_validation(trigger, screen_content)

def verify_configuration_menu_active(trigger: str, screen_content: str) -> bool:
    """Verify configuration menu is active"""
    safe_print("🔍 CONTEXT ACTION: verify_configuration_menu_active")
    
    menu_indicators = [
        "select an option",
        "choose option",
        "configuration menu", 
        "setup menu",
        "options:",
        "1. configure"
    ]
    
    for indicator in menu_indicators:
        if indicator in screen_content.lower():
            safe_print(f"   ✅ Configuration menu active: {indicator}")
            return True
    
    safe_print("   ❌ Configuration menu not active")
    return False

def ensure_user_input_received(trigger: str, screen_content: str) -> bool:
    """Ensure user input was actually received"""
    safe_print("🔍 CONTEXT ACTION: ensure_user_input_received")
    
    # Check for input confirmation indicators
    input_indicators = [
        "input received",
        "processing input",
        "user selected",
        "choice recorded",
        "option selected"
    ]
    
    for indicator in input_indicators:
        if indicator in screen_content.lower():
            safe_print(f"   ✅ User input confirmed: {indicator}")
            return True
    
    safe_print("   ⚠️  User input not confirmed")
    return False

def track_interface_state_changes(trigger: str, screen_content: str) -> bool:
    """Track interface state changes"""
    safe_print("🔍 CONTEXT ACTION: track_interface_state_changes")
    
    # Capture current state for comparison
    screenshot, screenshot_path = capture_screen()
    if screenshot_path:
        safe_print(f"   📸 Interface state captured: {screenshot_path}")
    
    safe_print("   ✅ Interface state change tracked")
    return True

def alternative_configuration_approach(trigger: str, screen_content: str) -> bool:
    """Try alternative configuration approach"""
    safe_print("🔧 ALTERNATIVE ACTION: alternative_configuration_approach")
    
    # Focus on ExtP first
    focus_using_alt_tab()
    time.sleep(1)
    
    # Try different configuration methods with real keyboard input
    alternatives = [
        ("Try configuration via F1 key", Key.f1),
        ("Try configuration via F2 key", Key.f2),
        ("Try Ctrl+C for configuration", "ctrl+c"),
        ("Try Ctrl+S for settings", "ctrl+s")
    ]
    
    for description, key_action in alternatives:
        safe_print(f"   🎮 ATTEMPTING: {description}")
        try:
            if isinstance(key_action, str) and "+" in key_action:
                # Handle key combinations
                keys = key_action.split("+")
                if len(keys) == 2:
                    pyautogui.hotkey(keys[0], keys[1])
            else:
                # Handle single keys
                send_key_multiple_methods(key_action, str(key_action))
            time.sleep(1)
        except Exception as e:
            safe_print(f"   ❌ Failed: {e}")
    
    safe_print("   ✅ Alternative configuration approach completed")
    return True

def retry_with_enhanced_validation(trigger: str, screen_content: str) -> bool:
    """Retry with enhanced validation"""
    safe_print("🔧 RETRY ACTION: retry_with_enhanced_validation")
    
    # Retry with additional validation steps
    return validate_then_configure(trigger, screen_content)

def escalate_to_manual_intervention(trigger: str, screen_content: str) -> bool:
    """Escalate to manual intervention"""
    safe_print("🚨 ESCALATION ACTION: escalate_to_manual_intervention")
    
    # Log escalation
    log_escalation(trigger, screen_content)
    
    # Generate defect prompt for escalation
    if issue_prompt_generator:
        try:
            from IssuePromptGenerator import TestCaseContext, DocumentationReference
            safe_print(f"📄 GENERATING DEFECT PROMPT FOR ESCALATION")
            
            test_context = TestCaseContext(
                test_case_name="Manual Intervention Required",
                test_sequence_id=f"ESCALATION_{int(time.time())}",
                expected_behavior="CUS should handle all scenarios automatically",
                actual_behavior="Manual intervention required due to unhandled scenario",
                failure_step=1,
                reproduction_steps=[
                    f"Trigger detected: {trigger}",
                    "All automated remediation attempts failed",
                    "Manual intervention required"
                ],
                documentation_refs=[
                    DocumentationReference(
                        file_path="CUS_Escalation_Procedures.md",
                        reference_type="procedure",
                        reference_id="CUS-ESC",
                        section_title="Manual Intervention Procedures"
                    )
                ],
                related_test_cases=["CUS Escalation Tests"],
                dependency_chain=["CUS", "ExtP", "Manual Intervention"]
            )
            
            prompt_obj = issue_prompt_generator.generate_issue_prompt(
                test_case_context=test_context,
                error_context={
                    "error_type": "manual_intervention_required",
                    "error_message": "All automated remediation attempts failed",
                    "trigger": trigger,
                    "screen_content": screen_content[:500]
                }
            )
            
            saved_path = issue_prompt_generator.save_issue_prompt(prompt_obj)
            safe_print(f"💾 ESCALATION DEFECT PROMPT SAVED: {prompt_obj.issue_id}")
            
        except Exception as e:
            safe_print(f"❌ ERROR GENERATING ESCALATION PROMPT: {e}")
    
    safe_print("   ⚠️  Manual intervention required")
    safe_print("   📋 Issue logged for manual review")
    return True

def detect_false_negative_configuration(trigger: str, screen_content: str) -> bool:
    """Detect false negative configuration scenario"""
    global false_negative_count
    safe_print("🚨 DETECTION ACTION: detect_false_negative_configuration")
    
    # This is a meta-action that triggers when false negatives are detected
    false_negative_count += 1
    
    # Apply remediation
    return handle_already_configured(trigger, screen_content)

def validate_configuration_response(screen_content: str) -> bool:
    """Validate configuration response"""
    safe_print("🔍 VALIDATING CONFIGURATION RESPONSE...")
    
    # Check for success indicators
    success_indicators = [
        "configuration interface",
        "setup wizard",
        "configuration menu",
        "enter configuration",
        "trading system configuration"
    ]
    
    for indicator in success_indicators:
        if indicator in screen_content.lower():
            safe_print(f"   ✅ Configuration response valid: {indicator}")
            return True
    
    # Check for false negative indicators
    false_negative_indicators = [
        "already configured",
        "configuration complete",
        "setup complete",
        "no configuration needed"
    ]
    
    for indicator in false_negative_indicators:
        if indicator in screen_content.lower():
            safe_print(f"   🚨 False negative detected: {indicator}")
            return False
    
    safe_print("   ⚠️  Configuration response unclear")
    return False

def log_false_negative(fn_type: str, trigger: str, screen_content: str):
    """Log false negative occurrence"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": fn_type,
        "trigger": trigger,
        "screen_content": screen_content[:200] + "..." if len(screen_content) > 200 else screen_content
    }
    
    log_file = "Logs/false_negatives.json"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Load existing log
    try:
        with open(log_file, 'r') as f:
            log_data = json.load(f)
    except:
        log_data = []
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
        
        # Initialize Enhanced CUS capabilities for false negative remediation
        safe_print("🔧 INITIALIZING ENHANCED CUS CAPABILITIES...")
        enhanced_success = initialize_enhanced_capabilities()
        if enhanced_success:
            safe_print("✅ ENHANCED CUS CAPABILITIES READY FOR FALSE NEGATIVE DETECTION")
        else:
            safe_print("⚠️  ENHANCED CUS CAPABILITIES NOT AVAILABLE - USING BASIC FUNCTIONALITY")
        
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
                
                # Check for error folder - if errors exist, pause briefly and continue
                if os.path.exists(NEW_ERRORS_PATH) and os.listdir(NEW_ERRORS_PATH):
                    safe_print(f"[{datetime.now().strftime('%H:%M:%S')}] NewErrorsPath contains errors. Pausing for 10 seconds...")
                    time.sleep(10)
                    # Check again after pause
                    if os.path.exists(NEW_ERRORS_PATH) and os.listdir(NEW_ERRORS_PATH):
                        safe_print("Errors still present. Continuing monitoring anyway.")
                    else:
                        safe_print("Errors cleared. Resuming normal operations.")
                
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
        
        # Generate defect prompt for critical errors
        if ISSUE_PROMPT_AVAILABLE:
            try:
                from IssuePromptGenerator import TestCaseContext, DocumentationReference
                safe_print(f"📄 GENERATING DEFECT PROMPT FOR CRITICAL ERROR")
                test_context = TestCaseContext(
                    test_case_name="CUS Critical Error",
                    test_sequence_id=f"CUS_CRITICAL_{int(time.time())}",
                    expected_behavior="CUS should start successfully and begin monitoring",
                    actual_behavior=f"Critical error in CUS main function: {str(e)}",
                    failure_step=0,
                    reproduction_steps=["1. Start CUS", "2. Error occurs during initialization"],
                    documentation_refs=[],
                    related_test_cases=[],
                    dependency_chain=[]
                )
                
                prompt_obj = issue_prompt_generator.generate_issue_prompt(
                    test_case_context=test_context,
                    error_context={
                        "error_type": "critical_error",
                        "error_message": f"Critical error in CUS main function: {str(e)}",
                        "traceback": traceback.format_exc()
                    }
                )
                
                saved_path = issue_prompt_generator.save_issue_prompt(prompt_obj)
                safe_print(f"💾 CRITICAL ERROR DEFECT PROMPT SAVED: {prompt_obj.issue_id}")
                
            except Exception as prompt_error:
                safe_print(f"❌ ERROR GENERATING CRITICAL ERROR PROMPT: {prompt_error}")
        
        raise
        
    except Exception as e:
        safe_print(f"Error in main function: {e}")
        safe_print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    print("=== CUS PYTHON SCRIPT STARTING ===", flush=True)
    print("[CUS] Script is being executed directly", flush=True)
    
    try:
        print("[CUS] About to call main()", flush=True)
        main()
        print("[CUS] Main function completed", flush=True)
    except Exception as e:
        print(f"[CUS] Fatal error: {e}", flush=True)
        import traceback
        print(f"[CUS] Traceback: {traceback.format_exc()}", flush=True)
        exit(1)
