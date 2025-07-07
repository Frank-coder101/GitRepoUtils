#!/usr/bin/env python3
"""Very simple test to debug CUS execution"""

print("=== SIMPLE TEST SCRIPT ===")
print("Python is working!")

# Try importing the modules
try:
    from pynput.keyboard import Controller, Key
    print("pynput imported successfully")
except ImportError as e:
    print(f"pynput import failed: {e}")

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    print("watchdog imported successfully")
except ImportError as e:
    print(f"watchdog import failed: {e}")

print("=== TEST COMPLETE ===")
