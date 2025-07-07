#!/usr/bin/env python3
"""
Test CUS imports to find the hanging issue
"""
print("=== Testing CUS imports ===")

print("Testing basic imports...")
import os
import time
import subprocess
import random
print("✓ Basic imports OK")

print("Testing system imports...")
try:
    import psutil
    print("✓ psutil OK")
    import pygetwindow as gw
    print("✓ pygetwindow OK")
    import pyautogui
    print("✓ pyautogui OK")
    import win32gui
    print("✓ win32gui OK")
    import win32con
    print("✓ win32con OK")
    import win32process
    print("✓ win32process OK")
    import win32api
    print("✓ win32api OK")
    import win32clipboard
    print("✓ win32clipboard OK")
    import re
    print("✓ re OK")
    import logging
    print("✓ logging OK")
    from PIL import ImageGrab
    print("✓ PIL.ImageGrab OK")
    import threading
    print("✓ threading OK")
    import queue
    print("✓ queue OK")
    import sys
    print("✓ sys OK")
    import json
    print("✓ json OK")
    from datetime import datetime
    print("✓ datetime OK")
    import ctypes
    print("✓ ctypes OK")
    from ctypes import wintypes
    print("✓ wintypes OK")
    print("✓ All system imports successful")
except Exception as e:
    print(f"✗ System imports failed: {e}")
    exit(1)

print("Testing pynput import...")
try:
    from pynput.keyboard import Controller, Key
    print("✓ pynput import successful")
except Exception as e:
    print(f"✗ pynput import failed: {e}")
    exit(1)

print("Testing OCR imports...")
try:
    import pytesseract
    print("✓ pytesseract OK")
    from PIL import Image, ImageGrab
    print("✓ PIL imports OK")
    print("✓ OCR imports successful")
except Exception as e:
    print(f"✗ OCR imports failed: {e}")
    exit(1)

print("Testing IssuePromptGenerator import...")
try:
    from IssuePromptGenerator import IssuePromptGenerator, IssueSeverity, FailureType
    print("✓ IssuePromptGenerator imported successfully")
except ImportError:
    print("⚠ IssuePromptGenerator not available")

print("=== All imports successful ===")
print("Testing keyboard controller...")
try:
    keyboard = Controller()
    print("✓ Keyboard controller initialized")
except Exception as e:
    print(f"✗ Keyboard controller failed: {e}")
    exit(1)

print("=== Import test complete ===")
