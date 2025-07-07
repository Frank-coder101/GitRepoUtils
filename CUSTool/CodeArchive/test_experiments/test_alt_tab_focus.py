#!/usr/bin/env python3
"""
Test the simple Alt+Tab focus workflow
"""

import time
import pyautogui

def test_alt_tab_focus():
    """Test the simple Alt+Tab focus workflow"""
    print("=== TESTING SIMPLE ALT+TAB FOCUS WORKFLOW ===")
    print("This will test the simple approach using Alt+Tab.")
    print("Please have your External Program (ExtP) running before starting.")
    
    print("\n" + "="*60)
    print("SIMPLE WINDOW FOCUS TEST")
    print("="*60)
    print("Please follow these steps:")
    print("1. Click on the External Program (ExtP) window to bring it into focus")
    print("2. Make sure ExtP is visible and active")
    print("3. Return to this test window and type 'Y' then press Enter")
    print("4. The test will use Alt+Tab to switch back to ExtP")
    print("="*60)
    
    while True:
        user_input = input("Type 'Y' when ExtP is focused and ready (or 'q' to quit): ").strip().upper()
        
        if user_input == 'Q':
            print("Test cancelled.")
            return
        elif user_input == 'Y':
            print("Testing Alt+Tab switch back to ExtP...")
            
            # Use Alt+Tab to switch to the previous window (ExtP)
            try:
                pyautogui.hotkey('alt', 'tab')
                time.sleep(1)  # Give time for the switch to complete
                print("✓ Alt+Tab executed!")
                
                # Now test sending some keys to see if ExtP receives them
                print("Sending test keys to ExtP in 3 seconds...")
                time.sleep(3)
                
                # Send a test sequence
                pyautogui.typewrite("Test from CUS Alt+Tab", interval=0.1)
                pyautogui.press('enter')
                
                print("✓ Test sequence sent to ExtP")
                print("Check ExtP window to see if it received: 'Test from CUS Alt+Tab'")
                
                # Switch back to this window
                print("\nSwitching back to test window...")
                time.sleep(2)
                pyautogui.hotkey('alt', 'tab')
                time.sleep(1)
                
                print("✓ Test complete!")
                print("If ExtP received the test text, the Alt+Tab approach is working!")
                return
                
            except Exception as e:
                print(f"✗ Error during test: {e}")
                return
        else:
            print("Please type 'Y' to confirm or 'q' to quit.")

if __name__ == "__main__":
    test_alt_tab_focus()
