#!/usr/bin/env python3
"""
Minimal dependency check - only includes what's actually needed for Alt+Tab mode
"""

print("Testing ESSENTIAL CUS dependencies (Alt+Tab mode)...")
try:
    # Core automation libraries
    import pynput
    print("✓ pynput available")
    
    import pyautogui
    print("✓ pyautogui available")
    
    # OCR libraries  
    import pytesseract
    print("✓ pytesseract available")
    
    import PIL
    print("✓ PIL available")
    
    # System monitoring
    import psutil
    print("✓ psutil available")
    
    # Window management (minimal)
    import pygetwindow
    print("✓ pygetwindow available")
    
    print("\n✅ All ESSENTIAL dependencies available!")
    print("✅ CUS Alt+Tab mode is ready!")
    
except ImportError as e:
    print(f"❌ Missing essential dependency: {e}")
    exit(1)

print("\nChecking OPTIONAL dependencies (legacy window management)...")
try:
    import win32gui
    import win32con
    import win32process
    print("✓ win32 modules available (but not required for Alt+Tab mode)")
except ImportError:
    print("⚠️  win32 modules not available (OK - not needed for Alt+Tab mode)")

print("\n" + "="*60)
print("DEPENDENCY ANALYSIS COMPLETE")
print("="*60)
