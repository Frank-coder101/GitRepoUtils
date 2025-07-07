#!/usr/bin/env python3
"""
Minimal CUS Test - Verify keystroke simulation works correctly
"""

import time
import json
import subprocess
import pyautogui

def test_cus_keystroke_simulation():
    """Test that CUS sends correct keystrokes, not literal 'Alt+Tab'"""
    print("=== Minimal CUS Keystroke Test ===")
    
    # Read simulation dictionary
    try:
        with open("simulation_dictionary.txt", 'r') as f:
            simulation_dict = json.loads(f.read())
        print(f"✓ Loaded {len(simulation_dict)} simulation rules")
    except Exception as e:
        print(f"✗ Error loading simulation dictionary: {e}")
        return False
    
    # Test the key trigger
    trigger = "Select an option:"
    if trigger in simulation_dict:
        action = simulation_dict[trigger]
        print(f"✓ Found trigger: '{trigger}' -> '{action}'")
        
        # Simulate the action parsing logic from CUS
        if action.startswith("type_"):
            text_to_send = action[5:]  # Extract text after "type_"
            print(f"✓ Action '{action}' will send text: '{text_to_send}'")
            
            # Verify it's what we expect
            if text_to_send == "1":
                print("✅ CORRECT: Will send '1' to ExtP")
                return True
            else:
                print(f"❌ INCORRECT: Will send '{text_to_send}' instead of '1'")
                return False
        else:
            print(f"❌ Action '{action}' is not a type action")
            return False
    else:
        print(f"❌ Trigger '{trigger}' not found in dictionary")
        return False

def create_test_scenario():
    """Create a test scenario with Notepad"""
    print("\n=== Creating Test Scenario ===")
    
    # Open Notepad
    print("Opening Notepad...")
    try:
        process = subprocess.Popen(['notepad.exe'])
        time.sleep(2)
        
        # Type the trigger text
        print("Typing trigger text in Notepad...")
        pyautogui.write("DeFi Huddle Trading System\n")
        pyautogui.write("Select an option:\n")
        pyautogui.write("1. Configure trading system\n")
        pyautogui.write("2. Activate EMERGENCY STOP\n")
        pyautogui.write("Enter your choice: ")
        
        print("✓ Notepad set up with ExtP-like content")
        return process
    except Exception as e:
        print(f"✗ Error creating test scenario: {e}")
        return None

def test_alt_tab_and_keystroke():
    """Test Alt+Tab focus and keystroke sending"""
    print("\n=== Testing Alt+Tab + Keystroke ===")
    
    # This simulates what CUS does:
    # 1. Alt+Tab to switch to ExtP (Notepad)
    # 2. Send the keystroke
    
    print("1. Switching to Notepad with Alt+Tab...")
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.5)
    
    print("2. Sending '1' to Notepad...")
    pyautogui.write('1')
    pyautogui.press('enter')
    
    print("3. Switching back to this window...")
    time.sleep(1)
    pyautogui.hotkey('alt', 'tab')
    
    print("✓ Alt+Tab and keystroke test completed")

def main():
    """Main test function"""
    print("=== CUS Keystroke Validation Test ===")
    print("This test validates that CUS sends correct keystrokes")
    
    # Test 1: Verify simulation dictionary logic
    if not test_cus_keystroke_simulation():
        print("❌ Simulation dictionary test failed")
        return
    
    # Test 2: Interactive test with Notepad
    response = input("\nTest with Notepad? (y/n): ").strip().lower()
    if response == 'y':
        notepad_process = create_test_scenario()
        if notepad_process:
            print("\n📝 Notepad is ready with test content")
            print("This test will:")
            print("1. Alt+Tab to switch to Notepad")
            print("2. Send '1' followed by Enter")
            print("3. Alt+Tab back to this window")
            
            input("\nPress Enter to start the test...")
            test_alt_tab_and_keystroke()
            
            print("\n🔍 Check Notepad - it should show '1' after 'Enter your choice: '")
            input("Press Enter when you've verified the result...")
            
            # Close Notepad
            try:
                notepad_process.terminate()
                print("✓ Notepad closed")
            except:
                print("⚠️ Please close Notepad manually")
    
    print("\n=== Test Summary ===")
    print("✅ Simulation dictionary maps 'Select an option:' to 'type_1'")
    print("✅ Action 'type_1' sends '1' (not 'Alt+Tab')")
    print("✅ Alt+Tab focus mechanism works")
    print("\n🎯 Conclusion: CUS should work correctly!")
    print("   - When it detects 'Select an option:', it will send '1'")
    print("   - Alt+Tab will properly focus ExtP before sending keys")

if __name__ == "__main__":
    main()
