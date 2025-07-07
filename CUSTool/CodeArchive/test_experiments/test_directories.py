#!/usr/bin/env python3
"""
Test directory creation and path handling
"""
import os
import time

print("=== Testing Directory Operations ===")

# Test paths from CUS.py
NEW_ERRORS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSErrors"
SIMULATION_EVENTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSEvents"
SCREENSHOTS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\Screenshots"

print(f"NEW_ERRORS_PATH: {NEW_ERRORS_PATH}")
print(f"SIMULATION_EVENTS_PATH: {SIMULATION_EVENTS_PATH}")
print(f"SCREENSHOTS_PATH: {SCREENSHOTS_PATH}")

print("Testing directory creation...")
try:
    print("Creating NEW_ERRORS_PATH...")
    os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
    print("✓ NEW_ERRORS_PATH created")
    
    print("Creating SIMULATION_EVENTS_PATH...")
    os.makedirs(SIMULATION_EVENTS_PATH, exist_ok=True)
    print("✓ SIMULATION_EVENTS_PATH created")
    
    print("Creating SCREENSHOTS_PATH...")
    os.makedirs(SCREENSHOTS_PATH, exist_ok=True)
    print("✓ SCREENSHOTS_PATH created")
    
    print("✓ All directories created successfully")
except Exception as e:
    print(f"✗ Directory creation failed: {e}")
    exit(1)

print("Testing simulation dictionary loading...")
SIMULATION_DICTIONARY_FILE = "simulation_dictionary.txt"
try:
    import json
    print(f"Checking if {SIMULATION_DICTIONARY_FILE} exists...")
    if not os.path.exists(SIMULATION_DICTIONARY_FILE):
        print("✗ simulation_dictionary.txt not found!")
        exit(1)
    print("✓ File exists")
    
    print("Loading simulation dictionary...")
    with open(SIMULATION_DICTIONARY_FILE, "r") as file:
        simulation_dictionary = json.load(file)
    print(f"✓ Loaded {len(simulation_dictionary)} simulation rules")
    
except Exception as e:
    print(f"✗ Simulation dictionary loading failed: {e}")
    exit(1)

print("=== Directory operations test complete ===")
print("Ready to test main CUS flow...")

print("Testing focus prompt...")
print("\n" + "="*60)
print("WINDOW FOCUS SETUP")
print("="*60)
print("Test focus prompt display")
print("="*60)

print("✓ Focus prompt test complete")
print("=== All tests passed ===")
