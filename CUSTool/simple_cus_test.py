#!/usr/bin/env python3
"""
Simplified CUS startup test
"""
import os
import time
import json

def safe_print(message):
    """Safe printing that won't cause issues"""
    print(f"[CUS] {message}")

def test_cus_startup():
    """Test CUS startup sequence step by step"""
    try:
        print("=== CUS STARTING UP ===")
        safe_print("Starting CLI User Simulator with Screen Capture...")
        
        # Add startup delay
        safe_print("Initializing... (3 second delay)")
        time.sleep(3)
        safe_print("✓ Sleep completed")
        
        safe_print("Using screen capture + OCR for monitoring")
        
        # Configuration paths
        NEW_ERRORS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\NewErrors"
        SIMULATION_EVENTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSEvents"
        SCREENSHOTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\Screenshots"
        
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
        SIMULATION_DICTIONARY_FILE = "simulation_dictionary.txt"
        
        if not os.path.exists(SIMULATION_DICTIONARY_FILE):
            safe_print("ERROR: simulation_dictionary.txt not found!")
            return {}
        
        with open(SIMULATION_DICTIONARY_FILE, "r") as file:
            try:
                simulation_dictionary = json.load(file)
                safe_print(f"✓ Loaded {len(simulation_dictionary)} simulation rules")
            except json.JSONDecodeError:
                safe_print("ERROR: Invalid JSON format in simulation dictionary file.")
                return {}
        
        # Launch external program (disabled for debugging)
        safe_print("External program handling...")
        safe_print("External program launch is disabled.")
        safe_print("Please start your external program manually before running CUS.")
        process = "dummy_process"
        safe_print("External program launch completed.")
        
        # Focus prompt
        safe_print("About to display focus prompt...")
        
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
            focus_mode = 's'
        
        safe_print(f"✓ Focus mode selected: {focus_mode}")
        
        print("✓ Test complete - focus prompt is working!")
        
    except Exception as e:
        safe_print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cus_startup()
