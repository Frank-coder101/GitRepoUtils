#!/usr/bin/env python3
"""Simple test to update log file and test CUS response"""

import time

LOG_FILE = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\output.log"

def test_cus_response():
    """Add content to log file that should trigger CUS response"""
    
    # Clear the log file and add fresh content
    with open(LOG_FILE, "w") as f:
        f.write("INFO:root:Python executable: C:\\Program Files\\Python313\\python.exe\n")
        f.write("2025-07-06 20:35:00,000 INFO CLI wizard started.\n")
        f.write("Welcome to DeFi Huddle Trading System Setup Wizard!\n")
        f.write("\n")
        f.write("Options:\n")
        f.write("1. Configure trading system\n")
        f.write("2. Activate EMERGENCY STOP\n")
        f.write("3. Deactivate EMERGENCY STOP\n")
        f.write("4. Show EMERGENCY STOP status\n")
        f.write("5. Exit wizard\n")
        f.write("Select an option:\n")
    
    print("=== Log file updated with menu content ===")
    print("If CUS is running, it should now:")
    print("1. Detect 'Select an option:' trigger")
    print("2. Execute 'type_4' action")
    print("3. Type '4' and press Enter")
    print("4. Create a simulation event log file")
    
    # Wait a moment then check if CUS responded
    time.sleep(3)
    
    # Check if CUS created a simulation event
    import os
    events_dir = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSEvents"
    if os.path.exists(events_dir):
        files = os.listdir(events_dir)
        latest_files = [f for f in files if f.startswith("CUS_simulation_event")]
        if latest_files:
            latest_file = max(latest_files, key=lambda x: os.path.getctime(os.path.join(events_dir, x)))
            print(f"\n✅ CUS responded! Latest event file: {latest_file}")
            
            # Read the event file
            with open(os.path.join(events_dir, latest_file), "r") as f:
                content = f.read()
                print(f"Event content:\n{content}")
        else:
            print("\n❌ No simulation events found - CUS may not be running or not detecting")
    else:
        print("\n❌ Events directory not found")

if __name__ == "__main__":
    test_cus_response()
