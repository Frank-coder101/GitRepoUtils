#!/usr/bin/env python3
"""Test script to verify all CUS dependencies are available"""

print("Testing all CUS dependencies...")
try:
    import pynput
    print("✓ pynput available")
    
    import pyautogui
    print("✓ pyautogui available")
    
    import pygetwindow
    print("✓ pygetwindow available")
    
    import pytesseract
    print("✓ pytesseract available")
    
    import PIL
    print("✓ PIL available")
    
    import psutil
    print("✓ psutil available")
    
    import win32gui
    print("✓ win32gui available")
    
    import win32con
    print("✓ win32con available")
    
    import win32process
    print("✓ win32process available")
    
    print("\n✓ All dependencies are available in system Python!")
    print("✓ CUS is ready to run!")
    
except ImportError as e:
    print(f"✗ Missing dependency: {e}")
    exit(1)
