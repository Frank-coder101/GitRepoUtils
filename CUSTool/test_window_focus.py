#!/usr/bin/env python3
"""
Window focus test script for ExtP integration
"""

import time
import pygetwindow as gw
import pyautogui

def test_window_detection():
    """Test window detection and focusing capabilities"""
    print("=== Window Focus Test ===")
    
    # Get all windows
    all_windows = gw.getAllWindows()
    print(f"Total windows found: {len(all_windows)}")
    
    # Show visible windows
    visible_windows = [w for w in all_windows if w.visible and w.title.strip()]
    print(f"\nVisible windows with titles ({len(visible_windows)}):")
    
    for i, window in enumerate(visible_windows):
        print(f"  {i+1:2d}. '{window.title}'")
        if hasattr(window, '_hWnd'):
            print(f"      HWND: {window._hWnd}")
        print(f"      Visible: {window.visible}")
    
    # Look for ExtP specifically
    print(f"\n=== Searching for ExtP patterns ===")
    extp_patterns = [
        "DeFi Huddle Trading System",
        "defi huddle",
        "trading system",
        "python"
    ]
    
    found_matches = []
    for pattern in extp_patterns:
        print(f"\nSearching for pattern: '{pattern}'")
        matches = []
        
        for window in visible_windows:
            title_lower = window.title.lower()
            pattern_lower = pattern.lower()
            
            if pattern_lower in title_lower:
                matches.append(window)
                print(f"  MATCH: '{window.title}'")
        
        if matches:
            found_matches.extend(matches)
    
    # Remove duplicates
    unique_matches = list(set(found_matches))
    
    if unique_matches:
        print(f"\n=== Found {len(unique_matches)} potential ExtP windows ===")
        for i, window in enumerate(unique_matches):
            print(f"{i+1}. '{window.title}'")
        
        # Test focusing on the first match
        test_window = unique_matches[0]
        print(f"\n=== Testing focus on: '{test_window.title}' ===")
        
        try:
            print("Attempting activation...")
            test_window.activate()
            time.sleep(1)
            print("✓ Activation command sent")
            
            # Check if it worked using Windows API
            try:
                import ctypes
                foreground_hwnd = ctypes.windll.user32.GetForegroundWindow()
                if hasattr(test_window, '_hWnd'):
                    if test_window._hWnd == foreground_hwnd:
                        print("✓ Window is now in foreground")
                        return True
                    else:
                        print("✗ Window may not be in foreground")
                        print(f"  Expected HWND: {test_window._hWnd}")
                        print(f"  Foreground HWND: {foreground_hwnd}")
                else:
                    print("? Cannot verify focus (no HWND available)")
            except Exception as e:
                print(f"? Focus verification failed: {e}")
                
        except Exception as e:
            print(f"✗ Activation failed: {e}")
            
    else:
        print("\n✗ No ExtP windows found!")
        print("\nPlease ensure ExtP is running and try again.")
        print("Expected window title contains: 'DeFi Huddle Trading System'")
    
    return False

def test_manual_focus():
    """Test manual window focusing"""
    print("\n=== Manual Focus Test ===")
    print("This will give you 5 seconds to manually focus on ExtP window...")
    
    for i in range(5, 0, -1):
        print(f"Focus ExtP window now... {i}")
        time.sleep(1)
    
    # Now test if we can detect the focused window
    try:
        import ctypes
        foreground_hwnd = ctypes.windll.user32.GetForegroundWindow()
        
        # Find which window is focused
        all_windows = gw.getAllWindows()
        focused_window = None
        
        for window in all_windows:
            if hasattr(window, '_hWnd') and window._hWnd == foreground_hwnd:
                focused_window = window
                break
        
        if focused_window:
            print(f"✓ Currently focused window: '{focused_window.title}'")
            
            # Test sending keys to this window
            print("Sending test key 'x' to focused window...")
            pyautogui.press('x')
            print("✓ Test key sent")
            
        else:
            print("✗ Could not identify focused window")
            
    except Exception as e:
        print(f"✗ Manual focus test failed: {e}")

if __name__ == "__main__":
    test_window_detection()
    test_manual_focus()
