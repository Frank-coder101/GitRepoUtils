#!/usr/bin/env python3
"""
Test script to simulate log file updates while CUS is running.
Uses Windows-compatible shared file access to avoid locking issues.
"""

import os
import time
import msvcrt
import sys

# Configuration
OUTPUT_LOG_FILE = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\output.log"

def write_to_log_shared(message):
    """Write to log file using shared access mode"""
    try:
        # Open file in append mode with shared access
        with open(OUTPUT_LOG_FILE, "a", encoding='utf-8') as log_file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"[{timestamp}] {message}\n")
            log_file.flush()  # Ensure data is written immediately
        print(f"Successfully wrote to log: {message}")
        return True
    except Exception as e:
        print(f"Failed to write to log: {e}")
        return False

def simulate_menu_interaction():
    """Simulate a menu interaction sequence"""
    print("=== Starting Menu Interaction Simulation ===")
    
    # Simulate program startup
    if write_to_log_shared("Starting DeFi Huddle Trading System..."):
        time.sleep(2)
        
        # Simulate menu display
        if write_to_log_shared("Select an option:"):
            time.sleep(1)
            write_to_log_shared("1. View Portfolio")
            time.sleep(0.5)
            write_to_log_shared("2. Execute Trade")
            time.sleep(0.5)
            write_to_log_shared("3. View Market Data")
            time.sleep(0.5)
            write_to_log_shared("4. Settings")
            time.sleep(0.5)
            write_to_log_shared("5. Exit")
            time.sleep(1)
            write_to_log_shared("Enter your choice: ")
            
            print("Menu simulation complete. CUS should have detected 'Select an option:' trigger.")
            return True
    
    return False

def interactive_mode():
    """Interactive mode for manual testing"""
    print("=== Interactive Log Update Mode ===")
    print("Type messages to add to the log file. Press 'q' to quit.")
    print("Try typing: 'Select an option:' to trigger CUS")
    print()
    
    while True:
        try:
            message = input("Enter message (or 'q' to quit): ")
            if message.lower() == 'q':
                break
            
            if write_to_log_shared(message):
                print("Message added to log successfully!")
            else:
                print("Failed to add message to log.")
                
        except KeyboardInterrupt:
            print("\nInterrupted by user.")
            break

def main():
    """Main function"""
    print("=== Log File Shared Access Test ===")
    print(f"Log file: {OUTPUT_LOG_FILE}")
    
    # Check if log file exists
    if not os.path.exists(OUTPUT_LOG_FILE):
        print("Log file doesn't exist. Creating it...")
        os.makedirs(os.path.dirname(OUTPUT_LOG_FILE), exist_ok=True)
        with open(OUTPUT_LOG_FILE, "w") as f:
            f.write("# Log file created by test script\n")
    
    # Test basic write
    print("Testing basic log write...")
    if write_to_log_shared("TEST: Log file shared access test"):
        print("✓ Basic write test passed")
    else:
        print("✗ Basic write test failed")
        return
    
    # Ask user what to do
    print("\nOptions:")
    print("1. Run menu simulation")
    print("2. Interactive mode")
    print("3. Exit")
    
    choice = input("Enter your choice (1-3): ")
    
    if choice == "1":
        simulate_menu_interaction()
    elif choice == "2":
        interactive_mode()
    elif choice == "3":
        print("Exiting...")
    else:
        print("Invalid choice. Running menu simulation as default.")
        simulate_menu_interaction()

if __name__ == "__main__":
    main()
