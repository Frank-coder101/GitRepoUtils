#!/usr/bin/env python3
"""
Debug version of CUS startup to find the hanging issue
"""
import os
import sys
import time
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def safe_print(message):
    """Safe print function"""
    print(f"[CUS] {message}")

def debug_main():
    """Debug main function"""
    try:
        print("=== CUS STARTING UP ===")
        safe_print("Starting CLI User Simulator with Screen Capture...")
        
        # Add startup delay as suggested
        safe_print("Initializing... (3 second delay)")
        time.sleep(3)
        safe_print("✓ Delay complete")
        
        safe_print("Using screen capture + OCR for monitoring")
        
        # Create required directories
        safe_print("Creating directories...")
        NEW_ERRORS_PATH = "NewErrors"
        SIMULATION_EVENTS_PATH = "Logs"
        SCREENSHOTS_PATH = "Screenshots"
        
        safe_print(f"Creating directory: {NEW_ERRORS_PATH}")
        os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
        safe_print(f"Creating directory: {SIMULATION_EVENTS_PATH}")
        os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
        safe_print(f"Creating directory: {SCREENSHOTS_PATH}")
        os.makedirs(SCREENSHOTS_PATH, exist_ok=True)
        safe_print("✓ Directories created successfully")
        
        # Load simulation dictionary
        safe_print("Loading simulation dictionary...")
        SIMULATION_DICTIONARY_FILE = "simulation_dictionary.txt"
        
        safe_print(f"Checking if file exists: {SIMULATION_DICTIONARY_FILE}")
        if not os.path.exists(SIMULATION_DICTIONARY_FILE):
            safe_print("ERROR: simulation_dictionary.txt not found!")
            return {}
        
        safe_print("Opening simulation dictionary file...")
        with open(SIMULATION_DICTIONARY_FILE, "r") as file:
            safe_print("File opened, attempting to parse JSON...")
            try:
                simulation_dictionary = json.load(file)
                safe_print(f"✓ JSON parsed successfully")
            except json.JSONDecodeError as e:
                safe_print(f"ERROR: Invalid JSON format: {e}")
                return {}
        
        safe_print(f"✓ Loaded {len(simulation_dictionary)} simulation rules")
        
        # Launch external program (disabled for debugging)
        safe_print("External program handling...")
        process = "dummy_process"  # Simplified
        safe_print("✓ External program launch completed.")
        
        # Focus prompt
        print("\n" + "="*60)
        print("WINDOW FOCUS SETUP")
        print("="*60)
        print("CUS can work in three modes:")
        print("1. SIMPLE MODE: Use Alt+Tab to switch to ExtP (recommended)")
        print("2. GUIDED MODE: You help CUS identify the ExtP window")
        print("3. PATTERN MODE: CUS tries to find ExtP using window title patterns")
        print("Please ensure the External Program is running before proceeding.")
        print("="*60)
        
        focus_mode = input("Choose mode - (s)imple, (g)uided, (p)attern [s]: ").strip().lower()
        if not focus_mode:
            focus_mode = 's'  # Default to simple mode
        
        safe_print(f"✓ Focus mode selected: {focus_mode}")
        
        print("✓ Debug test complete - focus prompt is working!")
        
    except Exception as e:
        safe_print(f"ERROR in debug_main: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_main()
