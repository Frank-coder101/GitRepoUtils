#!/usr/bin/env python3
"""
Standalone test for window focus workflow
This script contains the window focus functions and tests them directly
"""

import os
import sys
import time
import traceback
import win32gui
import win32con
import win32process
import psutil

# Global variables for target window tracking
target_window = None
target_window_title = ""
target_window_hwnd = None
target_window_process_id = None

def safe_print(message):
    """Safe printing that won't cause issues"""
    print(f"[TEST] {message}")

def prompt_user_to_focus_external_program():
    """Prompt user to focus the external program and confirm."""
    global target_window, target_window_title, target_window_hwnd, target_window_process_id
    
    print("\n" + "="*60)
    print("WINDOW FOCUS SETUP")
    print("="*60)
    print("Please follow these steps:")
    print("1. Click on the External Program (ExtP) window to bring it into focus")
    print("2. Make sure ExtP is visible and active")
    print("3. Then return to this terminal and press Enter to confirm")
    print("   (This will shift focus to CUS, allowing us to record ExtP's window)")
    print("4. CUS will then bring ExtP back into focus for monitoring")
    print("="*60)
    
    # Wait for user confirmation
    input("Press Enter after focusing ExtP...")
    
    # At this point, the user has pressed Enter, so focus is back on CUS
    # We need to get the window that was previously focused (ExtP)
    
    # Try to find the external program window using various methods
    print("\nSearching for External Program window...")
    
    # Method 1: Look for windows that were recently active
    all_windows = []
    try:
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
                windows.append(hwnd)
            return True
        
        win32gui.EnumWindows(enum_windows_callback, all_windows)
        
        # Get info for all visible windows
        window_candidates = []
        for hwnd in all_windows:
            try:
                title = win32gui.GetWindowText(hwnd)
                _, process_id = win32process.GetWindowThreadProcessId(hwnd)
                
                # Skip our own window and common system windows
                if (title and 
                    'CUS' not in title and 
                    'Command Prompt' not in title and
                    'PowerShell' not in title and
                    'Windows Terminal' not in title and
                    'Terminal' not in title and
                    'Explorer' not in title and
                    'Desktop' not in title):
                    
                    try:
                        process = psutil.Process(process_id)
                        process_name = process.name()
                        
                        window_candidates.append({
                            'hwnd': hwnd,
                            'title': title,
                            'process_id': process_id,
                            'process_name': process_name
                        })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except Exception:
                pass
        
        if window_candidates:
            print("\nFound potential External Program windows:")
            for i, window in enumerate(window_candidates):
                print(f"{i+1}. {window['title']} (Process: {window['process_name']})")
            
            # Ask user to select the correct window
            while True:
                try:
                    choice = input(f"\nSelect the External Program window (1-{len(window_candidates)}) or 'q' to quit: ").strip()
                    if choice.lower() == 'q':
                        print("Setup cancelled.")
                        return False
                    
                    choice_idx = int(choice) - 1
                    if 0 <= choice_idx < len(window_candidates):
                        selected_window = window_candidates[choice_idx]
                        break
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a number or 'q' to quit.")
            
            # Store the selected window information
            target_window_hwnd = selected_window['hwnd']
            target_window_title = selected_window['title']
            target_window_process_id = selected_window['process_id']
            
            print(f"\nSelected: {target_window_title}")
            print(f"Process: {selected_window['process_name']}")
            print(f"Window Handle: {target_window_hwnd}")
            
            # Test focusing the window
            print("\nTesting window focus...")
            success = focus_target_window()
            if success:
                print("✓ Successfully focused External Program window")
                print("✓ Window focus setup complete!")
                return True
            else:
                print("✗ Failed to focus External Program window")
                print("Please try the setup again.")
                return False
        else:
            print("No suitable External Program windows found.")
            print("Please make sure ExtP is running and try again.")
            return False
            
    except Exception as e:
        safe_print(f"Error during window focus setup: {str(e)}")
        print(f"Error during setup: {str(e)}")
        return False

def focus_target_window():
    """Focus the target window using the stored window handle."""
    global target_window_hwnd, target_window_title
    
    if not target_window_hwnd:
        safe_print("No target window handle stored")
        return False
    
    try:
        # Verify the window still exists
        if not win32gui.IsWindow(target_window_hwnd):
            safe_print(f"Target window handle {target_window_hwnd} is no longer valid")
            return False
        
        # Check if window is visible
        if not win32gui.IsWindowVisible(target_window_hwnd):
            safe_print(f"Target window {target_window_title} is not visible")
            # Try to show it
            win32gui.ShowWindow(target_window_hwnd, win32con.SW_SHOW)
        
        # Restore if minimized
        if win32gui.IsIconic(target_window_hwnd):
            win32gui.ShowWindow(target_window_hwnd, win32con.SW_RESTORE)
        
        # Bring to foreground
        win32gui.SetForegroundWindow(target_window_hwnd)
        
        # Give it a moment to process
        time.sleep(0.1)
        
        # Verify it's now the foreground window
        current_foreground = win32gui.GetForegroundWindow()
        if current_foreground == target_window_hwnd:
            safe_print(f"Successfully focused target window: {target_window_title}")
            return True
        else:
            safe_print(f"Focus attempt may have failed. Current foreground: {win32gui.GetWindowText(current_foreground)}")
            return False
            
    except Exception as e:
        safe_print(f"Error focusing target window: {str(e)}")
        return False

def main():
    """Test the new window focus workflow"""
    try:
        print("=== TESTING NEW WINDOW FOCUS WORKFLOW ===")
        print("This script will test the new user-guided window focus setup.")
        print("Please have an external program running (like Notepad) to test with.")
        
        print("\n1. Testing window focus setup...")
        success = prompt_user_to_focus_external_program()
        
        if success:
            print("\n✓ Window focus setup successful!")
            
            # Test multiple focus attempts
            print("\n2. Testing multiple focus attempts...")
            for i in range(3):
                print(f"\nFocus test {i+1}/3...")
                time.sleep(1)
                if focus_target_window():
                    print(f"✓ Focus test {i+1} successful")
                else:
                    print(f"✗ Focus test {i+1} failed")
                time.sleep(2)
            
            print("\n=== TEST COMPLETE ===")
            print("If all focus tests succeeded, the new workflow is working correctly!")
            
        else:
            print("\n✗ Window focus setup failed")
            print("Please check that an external program is running and try again.")
            
    except Exception as e:
        print(f"\nError during test: {e}")
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    main()
