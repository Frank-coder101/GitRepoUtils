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

# Global flag for Alt+Tab focus mode
use_alt_tab_focus = False

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
                import pyautogui
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
        import pyautogui
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.3)  # Brief pause for window switch
        safe_print("Alt+Tab executed - should be focused on ExtP")
        return True
    except Exception as e:
        safe_print(f"Error executing Alt+Tab: {e}")
        return False

def perform_action(action):
    """Perform the specified action with Alt+Tab focus"""
    global use_alt_tab_focus
    
    safe_print(f"Starting action: {action}")
    
    # Focus on ExtP using Alt+Tab
    if use_alt_tab_focus:
        safe_print("Using Alt+Tab to switch to ExtP...")
        focus_using_alt_tab()
    
    # Simple action execution
    if action == "press_enter":
        safe_print("Pressing Enter")
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    elif action == "press_space":
        safe_print("Pressing Space")
        keyboard.press(Key.space)
        keyboard.release(Key.space)
    elif action.startswith("type_"):
        text = action[5:]
        safe_print(f"Typing: {text}")
        keyboard.type(text)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
    
    safe_print(f"Action '{action}' completed")

def main():
    """Main function to run the CUS system"""
    try:
        print("=== CUS STARTING UP ===", flush=True)
        safe_print("Starting CLI User Simulator with Alt+Tab Focus...")
        
        # Load simulation dictionary
        safe_print("Loading simulation dictionary...")
        simulation_dictionary = load_simulation_dictionary()
        safe_print(f"Loaded {len(simulation_dictionary)} simulation rules")
        
        # NEW WORKFLOW: Simple Alt+Tab focus approach
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
        
        # Simple monitoring loop for testing
        safe_print("CUS monitoring started - Alt+Tab focus enabled!")
        safe_print("Press Ctrl+C to stop monitoring")
        
        loop_count = 0
        while True:
            time.sleep(5)  # Check every 5 seconds
            loop_count += 1
            if loop_count % 10 == 0:  # Show status every 50 seconds
                safe_print(f"Monitoring active - Loop {loop_count}")
            
            # Simple test: if dictionary has triggers, simulate one
            if simulation_dictionary and loop_count == 5:  # Test after 25 seconds
                test_trigger = list(simulation_dictionary.keys())[0]
                test_action = simulation_dictionary[test_trigger]
                safe_print(f"TESTING: Simulating trigger '{test_trigger}' -> action '{test_action}'")
                perform_action(test_action)
                        
    except KeyboardInterrupt:
        safe_print("Interrupted by user. Stopping CUS...")
    except Exception as e:
        safe_print(f"Critical error in main: {e}")
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
