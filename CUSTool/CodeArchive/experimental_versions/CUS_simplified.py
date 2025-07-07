#!/usr/bin/env python3
"""
CUS Simplified - Direct keyboard simulation without OCR dependency
For immediate testing with ExtP
"""

import time
import json
import pyautogui
import os

# Configuration
SIMULATION_DICTIONARY_FILE = "simulation_dictionary.txt"
POLL_INTERVAL = 5  # Check every 5 seconds instead of 3

# Global flag for Alt+Tab focus mode
use_alt_tab_focus = False

def safe_print(message):
    """Safe printing that won't cause issues"""
    print(f"[CUS-SIMPLE] {message}")

def load_simulation_dictionary():
    """Load the simulation dictionary"""
    try:
        if not os.path.exists(SIMULATION_DICTIONARY_FILE):
            safe_print(f"Dictionary file {SIMULATION_DICTIONARY_FILE} not found")
            return {}
        
        with open(SIMULATION_DICTIONARY_FILE, "r") as file:
            simulation_dict = json.load(file)
            safe_print(f"Loaded {len(simulation_dict)} simulation rules")
            return simulation_dict
    except Exception as e:
        safe_print(f"Error loading simulation dictionary: {e}")
        return {}

def focus_using_alt_tab():
    """Use Alt+Tab to switch back to the previously focused window (ExtP)"""
    try:
        safe_print("Using Alt+Tab to switch to ExtP window...")
        pyautogui.hotkey('alt', 'tab')
        time.sleep(0.3)
        safe_print("Alt+Tab executed - should be focused on ExtP")
        return True
    except Exception as e:
        safe_print(f"Error executing Alt+Tab: {e}")
        return False

def send_keystroke(text):
    """Send keystroke to the focused window"""
    try:
        safe_print(f"Sending keystroke: '{text}'")
        pyautogui.typewrite(text, interval=0.1)
        time.sleep(0.2)
        pyautogui.press('enter')
        safe_print(f"Keystroke '{text}' sent successfully")
        return True
    except Exception as e:
        safe_print(f"Error sending keystroke: {e}")
        return False

def perform_action(action):
    """Perform the specified action"""
    safe_print(f"Performing action: {action}")
    
    # Focus ExtP using Alt+Tab
    if use_alt_tab_focus:
        focus_success = focus_using_alt_tab()
        if not focus_success:
            safe_print("WARNING: Alt+Tab focus failed!")
    
    # Process the action
    if action.startswith("type_"):
        text = action[5:]  # Extract text after "type_"
        send_keystroke(text)
    elif action == "press_enter":
        pyautogui.press('enter')
        safe_print("Enter key sent")
    elif action == "press_space":
        pyautogui.press('space')
        safe_print("Space key sent")
    else:
        safe_print(f"Unknown action: {action}")
    
    time.sleep(1)  # Give time for action to take effect

def prompt_user_for_focus_and_switch():
    """Simple focus workflow: user focuses ExtP, confirms in CUS, then Alt+Tab back"""
    print("\n" + "="*60)
    print("SIMPLE WINDOW FOCUS SETUP")
    print("="*60)
    print("Please follow these steps:")
    print("1. Click on the External Program (ExtP) window to bring it into focus")
    print("2. Make sure ExtP is visible and active")
    print("3. Return to this CUS window and type 'Y' then press Enter")
    print("4. CUS will then use Alt+Tab to switch back to ExtP")
    print("="*60)
    
    while True:
        user_input = input("Type 'Y' when ExtP is focused and ready (or 'q' to quit): ").strip().upper()
        
        if user_input == 'Q':
            print("Setup cancelled.")
            return False
        elif user_input == 'Y':
            print("Switching back to ExtP using Alt+Tab...")
            
            # Use Alt+Tab to switch to the previous window (ExtP)
            try:
                pyautogui.hotkey('alt', 'tab')
                time.sleep(0.5)
                print("✓ Alt+Tab executed - ExtP should now be in focus")
                print("✓ Simple focus setup complete!")
                return True
            except Exception as e:
                print(f"✗ Error executing Alt+Tab: {e}")
                return False
        else:
            print("Please type 'Y' to confirm or 'q' to quit.")

def test_trigger_manually():
    """Test triggers manually without OCR"""
    simulation_dict = load_simulation_dictionary()
    
    print("\n" + "="*60)
    print("MANUAL TRIGGER TESTING")
    print("="*60)
    print("Available triggers:")
    
    triggers = list(simulation_dict.keys())
    for i, trigger in enumerate(triggers[:10], 1):  # Show first 10
        action = simulation_dict[trigger]
        print(f"{i}. '{trigger}' -> '{action}'")
    
    print("="*60)
    
    while True:
        choice = input("\nEnter trigger number to test (or 'q' to quit, 'a' for auto mode): ").strip().lower()
        
        if choice == 'q':
            break
        elif choice == 'a':
            return 'auto'  # Signal to start auto mode
        
        try:
            trigger_idx = int(choice) - 1
            if 0 <= trigger_idx < len(triggers):
                trigger = triggers[trigger_idx]
                action = simulation_dict[trigger]
                
                print(f"\nSelected: '{trigger}' -> '{action}'")
                confirm = input("Execute this action? (y/n): ").strip().lower()
                
                if confirm == 'y':
                    perform_action(action)
                    print("✓ Action executed!")
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a number!")

def auto_monitor_mode():
    """Simple auto monitoring mode - prompts user when to check"""
    simulation_dict = load_simulation_dictionary()
    
    print("\n" + "="*60)
    print("AUTO MONITORING MODE")
    print("="*60)
    print("CUS will ask you to check ExtP for triggers every few seconds.")
    print("Look at your ExtP window and tell CUS what you see.")
    print("="*60)
    
    loop_count = 0
    
    while True:
        time.sleep(POLL_INTERVAL)
        loop_count += 1
        
        print(f"\n[Loop {loop_count}] Checking ExtP...")
        user_input = input("What text do you see in ExtP? (or 'q' to quit): ").strip()
        
        if user_input.lower() == 'q':
            break
        
        if not user_input:
            continue
        
        # Check for triggers in user input
        found_trigger = False
        for trigger, action in simulation_dict.items():
            if trigger.lower() in user_input.lower():
                print(f"🎯 TRIGGER FOUND: '{trigger}' -> '{action}'")
                confirm = input("Execute this action? (y/n): ").strip().lower()
                
                if confirm == 'y':
                    perform_action(action)
                    found_trigger = True
                    break
        
        if not found_trigger:
            print("No triggers found in that text.")

def main():
    """Main function"""
    global use_alt_tab_focus
    
    print("=== CUS SIMPLIFIED - DIRECT KEYBOARD SIMULATION ===")
    safe_print("Starting simplified CUS for immediate ExtP testing...")
    
    # Load simulation dictionary
    simulation_dict = load_simulation_dictionary()
    if not simulation_dict:
        safe_print("No simulation dictionary available. Exiting.")
        return
    
    # Focus setup
    print("\n" + "="*60)
    print("WINDOW FOCUS SETUP")
    print("="*60)
    print("Please ensure the External Program (ExtP) is running before proceeding.")
    print("="*60)
    
    setup_success = prompt_user_for_focus_and_switch()
    if setup_success:
        use_alt_tab_focus = True
        safe_print("Focus setup complete. Alt+Tab mode enabled.")
    else:
        safe_print("Focus setup failed or cancelled.")
        return
    
    # Choose mode
    print("\n" + "="*60)
    print("OPERATION MODE")
    print("="*60)
    print("1. MANUAL MODE: Test triggers manually")
    print("2. AUTO MODE: Monitor ExtP automatically (user assisted)")
    print("="*60)
    
    mode = input("Choose mode (1/2): ").strip()
    
    if mode == "1":
        result = test_trigger_manually()
        if result == 'auto':
            auto_monitor_mode()
    elif mode == "2":
        auto_monitor_mode()
    else:
        safe_print("Invalid choice. Starting manual mode...")
        test_trigger_manually()
    
    safe_print("CUS Simplified session complete.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[CUS-SIMPLE] Interrupted by user. Stopping...")
    except Exception as e:
        print(f"\n[CUS-SIMPLE] Error: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
