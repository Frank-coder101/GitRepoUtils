print("=== CUS MINIMAL TEST ===")

# Copy the exact imports from CUS.py
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
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    print("watchdog imported successfully")
except Exception as e:
    print(f"watchdog import failed: {e}")
    exit(1)

print("=== ALL IMPORTS SUCCESSFUL ===")
print("=== INITIALIZING CONFIGURATION ===")

# Production Configuration
SAFE_MODE = False  # Production mode - real keyboard simulation
print("SAFE_MODE set")

# Configuration
OUTPUT_LOG_FILE = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\output.log"
print("OUTPUT_LOG_FILE set")

# Initialize keyboard controller for production
print("=== INITIALIZING KEYBOARD CONTROLLER ===")
try:
    keyboard = Controller()
    print("Keyboard controller initialized successfully")
except Exception as e:
    print(f"Keyboard controller initialization failed: {e}")
    exit(1)

print("=== KEYBOARD CONTROLLER READY ===")
print("=== MINIMAL TEST COMPLETE ===")
print("If you see this message, the basic setup is working!")

# Test the if __name__ == "__main__" block
if __name__ == "__main__":
    print("=== MAIN BLOCK EXECUTED ===")
    print("Script is being run directly")
    print("=== ALL TESTS PASSED ===")
