#!/usr/bin/env python3
"""
Quick test to see what windows are available and test focusing
"""

import pygetwindow as gw
import time

def list_windows():
    """List all available windows"""
    try:
        all_windows = gw.getAllWindows()
        print(f"Found {len(all_windows)} total windows")
        
        visible_windows = [w for w in all_windows if w.visible and w.title.strip()]
        print(f"\nVisible windows with titles ({len(visible_windows)}):")
        
        for i, window in enumerate(visible_windows):
            print(f"{i+1:2d}. '{window.title}' (size: {window.width}x{window.height})")
            
        return visible_windows
    except Exception as e:
        print(f"Error listing windows: {e}")
        return []

def test_window_focus():
    """Test focusing on a specific window"""
    windows = list_windows()
    
    if not windows:
        print("No windows found to test")
        return
    
    print(f"\nSelect a window to test focusing (1-{len(windows)}) or 0 to quit:")
    try:
        choice = int(input("Enter choice: "))
        if choice == 0:
            return
        if 1 <= choice <= len(windows):
            selected_window = windows[choice - 1]
            print(f"\nTesting focus on: '{selected_window.title}'")
            
            # Try to activate the window
            try:
                selected_window.activate()
                time.sleep(0.5)
                print("✓ Focus attempt completed")
                
                # Check if it worked by seeing if it's still visible and active
                if selected_window.isActive:
                    print("✓ Window appears to be active")
                else:
                    print("✗ Window may not be active")
                    
            except Exception as e:
                print(f"✗ Focus failed: {e}")
        else:
            print("Invalid choice")
    except ValueError:
        print("Please enter a number")

if __name__ == "__main__":
    print("=== WINDOW FOCUS TEST ===")
    test_window_focus()
