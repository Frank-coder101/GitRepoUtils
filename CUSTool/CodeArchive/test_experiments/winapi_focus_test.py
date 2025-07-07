#!/usr/bin/env python3
"""
Test focusing using Windows API directly
"""

import win32gui
import win32con
import win32process
import psutil
import time

def list_windows_with_winapi():
    """List windows using Windows API"""
    windows = []
    
    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title.strip():
                try:
                    _, process_id = win32process.GetWindowThreadProcessId(hwnd)
                    try:
                        process = psutil.Process(process_id)
                        process_name = process.name()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        process_name = "Unknown"
                    
                    windows.append({
                        'hwnd': hwnd,
                        'title': title,
                        'process_id': process_id,
                        'process_name': process_name
                    })
                except Exception:
                    pass
        return True
    
    win32gui.EnumWindows(enum_windows_callback, windows)
    return windows

def test_focus_with_winapi():
    """Test focusing using Windows API"""
    windows = list_windows_with_winapi()
    
    print(f"Found {len(windows)} visible windows with titles:")
    for i, window in enumerate(windows):
        print(f"{i+1:2d}. '{window['title']}' (Process: {window['process_name']}, PID: {window['process_id']})")
    
    print(f"\nSelect a window to test focusing (1-{len(windows)}) or 0 to quit:")
    try:
        choice = int(input("Enter choice: "))
        if choice == 0:
            return
        if 1 <= choice <= len(windows):
            selected_window = windows[choice - 1]
            print(f"\nTesting focus on: '{selected_window['title']}'")
            
            hwnd = selected_window['hwnd']
            
            # Test if window is valid
            if not win32gui.IsWindow(hwnd):
                print("✗ Window handle is invalid")
                return
                
            print("✓ Window handle is valid")
            
            # Check if window is visible
            if not win32gui.IsWindowVisible(hwnd):
                print("✗ Window is not visible")
                return
                
            print("✓ Window is visible")
            
            # Try to restore if minimized
            if win32gui.IsIconic(hwnd):
                print("Window is minimized, restoring...")
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                time.sleep(0.5)
            
            # Try to bring to foreground
            try:
                print("Attempting to bring window to foreground...")
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.5)
                
                # Check if it's now the foreground window
                current_foreground = win32gui.GetForegroundWindow()
                if current_foreground == hwnd:
                    print("✓ Successfully focused window!")
                else:
                    current_title = win32gui.GetWindowText(current_foreground)
                    print(f"✗ Focus may have failed. Current foreground: '{current_title}'")
                    
            except Exception as e:
                print(f"✗ Focus failed: {e}")
                
        else:
            print("Invalid choice")
    except ValueError:
        print("Please enter a number")

if __name__ == "__main__":
    print("=== WINDOWS API FOCUS TEST ===")
    test_focus_with_winapi()
