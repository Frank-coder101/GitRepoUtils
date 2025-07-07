#!/usr/bin/env python3
"""
Very simple test to isolate the hanging issue
"""
import sys
import os
import time

print("=== SIMPLE TEST START ===", flush=True)
print("Step 1: Basic imports", flush=True)

print("Step 2: Testing time.sleep", flush=True)
time.sleep(1)
print("Step 3: Sleep completed", flush=True)

print("Step 4: Testing configuration", flush=True)
NEW_ERRORS_PATH = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\NewErrors"
print(f"NEW_ERRORS_PATH: {NEW_ERRORS_PATH}", flush=True)

print("Step 5: Testing directory operations", flush=True)
try:
    os.makedirs(NEW_ERRORS_PATH, exist_ok=True)
    print("✓ Directory created", flush=True)
except Exception as e:
    print(f"✗ Directory creation failed: {e}", flush=True)

print("Step 6: Testing file check", flush=True)
if os.path.exists(NEW_ERRORS_PATH) and os.listdir(NEW_ERRORS_PATH):
    print("✓ NewErrors directory has files", flush=True)
else:
    print("✓ NewErrors directory is empty", flush=True)

print("=== SIMPLE TEST COMPLETE ===", flush=True)
