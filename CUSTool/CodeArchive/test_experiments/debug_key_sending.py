#!/usr/bin/env python3
"""
Debug script to test key sending directly to ExtP
"""

import time
import pyautogui
import pygetwindow as gw
from pynput.keyboard import Controller, Key

def list_windows():
    """List all available windows"""
    print("Available windows:")
    windows = gw.getAllWindows()
    for i, window in enumerate(windows):
        if window.visible and window.title.strip():
            print(f"  {i+1}. '{window.title}' (visible: {window.visible})")

def focus_target_window():
    """Focus on the target window"""
    patterns = [
        "DeFi Huddle Trading System",
        "Python",
        "Command Prompt", 
        "Windows PowerShell",
        "PowerShell"
    ]
    
    windows = gw.getAllWindows()
    for pattern in patterns:
        for window in windows:
            if pattern.lower() in window.title.lower() and window.visible:
                try:
                    print(f"Focusing on: {window.title}")
                    window.activate()
                    time.sleep(1)
                    return True
                except Exception as e:
                    print(f"Could not focus on {window.title}: {e}")
    return False

def test_key_methods():
    """Test different key sending methods"""
    keyboard = Controller()
    
    print("Testing key sending methods...")
    print("Make sure the target window is ready and focused!")
    
    for i in range(5, 0, -1):
        print(f"Starting in {i} seconds...")
        time.sleep(1)
    
    # Test 1: pynput
    print("Test 1: Sending '1' via pynput...")
    try:
        keyboard.type("1")
        time.sleep(0.2)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        print("✓ pynput method completed")
    except Exception as e:
        print(f"✗ pynput failed: {e}")
    
    time.sleep(2)
    
    # Test 2: pyautogui
    print("Test 2: Sending '2' via pyautogui...")
    try:
        pyautogui.typewrite("2")
        time.sleep(0.2)
        pyautogui.press('enter')
        print("✓ pyautogui method completed")
    except Exception as e:
        print(f"✗ pyautogui failed: {e}")
    
    time.sleep(2)
    
    # Test 3: Windows API
    print("Test 3: Sending '3' via Windows API...")
    try:
        import ctypes
        
        # Send '3'
        ctypes.windll.user32.keybd_event(0x33, 0, 0, 0)  # '3' key down
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(0x33, 0, 2, 0)  # '3' key up
        time.sleep(0.2)
        
        # Send Enter
        ctypes.windll.user32.keybd_event(0x0D, 0, 0, 0)  # Enter down
        time.sleep(0.05)
        ctypes.windll.user32.keybd_event(0x0D, 0, 2, 0)  # Enter up
        print("✓ Windows API method completed")
    except Exception as e:
        print(f"✗ Windows API failed: {e}")
    
    print("All tests completed. Check if any inputs were received by the target program.")

if __name__ == "__main__":
    print("=== Key Sending Debug Tool ===")
    
    print("\nStep 1: Listing available windows...")
    list_windows()
    
    print("\nStep 2: Attempting to focus target window...")
    focus_success = focus_target_window()
    if not focus_success:
        print("Warning: Could not automatically focus target window")
        print("Please manually focus on your ExtP window now!")
        input("Press Enter when ExtP window is focused and ready...")
    
    print("\nStep 3: Testing key sending methods...")
    test_key_methods()
