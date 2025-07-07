#!/usr/bin/env python3
"""
Alternative test approach: Create content in a separate file and append to main log
This avoids file locking issues entirely.
"""

import os
import time
import shutil
import tempfile

# Configuration
OUTPUT_LOG_FILE = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\output.log"

def append_to_log_safe(message):
    """Safely append to log file using temporary file approach"""
    try:
        # Create temporary file with the message
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tmp') as temp_file:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            temp_file.write(f"[{timestamp}] {message}\n")
            temp_file.flush()
            temp_name = temp_file.name
        
        # Append temp file content to main log
        with open(OUTPUT_LOG_FILE, "a", encoding='utf-8') as log_file:
            with open(temp_name, "r", encoding='utf-8') as temp_read:
                log_file.write(temp_read.read())
            log_file.flush()
        
        # Clean up temp file
        os.unlink(temp_name)
        
        print(f"Successfully appended to log: {message}")
        return True
        
    except Exception as e:
        print(f"Failed to append to log: {e}")
        try:
            os.unlink(temp_name)
        except:
            pass
        return False

def run_cus_trigger_test():
    """Run a test that should trigger CUS simulation"""
    print("=== CUS Trigger Test ===")
    print("This will add a trigger phrase to the log that should make CUS respond.")
    print()
    
    # Add some normal log content first
    append_to_log_safe("Starting test sequence...")
    time.sleep(1)
    
    append_to_log_safe("Initializing trading system...")
    time.sleep(1)
    
    append_to_log_safe("Loading configuration...")
    time.sleep(1)
    
    # Add the trigger phrase
    print("Adding trigger phrase: 'Select an option:'")
    append_to_log_safe("Select an option:")
    time.sleep(0.5)
    
    # Add menu options
    append_to_log_safe("1. View Portfolio")
    append_to_log_safe("2. Execute Trade")
    append_to_log_safe("3. View Market Data")
    append_to_log_safe("4. Settings")
    append_to_log_safe("5. Exit")
    
    append_to_log_safe("Enter your choice: ")
    
    print("Trigger test complete!")
    print("Check CUS output - it should have detected the trigger and simulated typing '4'")
    print("Also check the CUSEvents folder for simulation event files.")

def main():
    """Main function"""
    print("=== Safe Log Update Test ===")
    print(f"Target log file: {OUTPUT_LOG_FILE}")
    
    # Ensure log file exists
    if not os.path.exists(OUTPUT_LOG_FILE):
        print("Creating log file...")
        os.makedirs(os.path.dirname(OUTPUT_LOG_FILE), exist_ok=True)
        with open(OUTPUT_LOG_FILE, "w") as f:
            f.write("# Log file created\n")
    
    # Test basic append
    print("Testing basic append operation...")
    if append_to_log_safe("TEST: Safe log append test"):
        print("✓ Basic append test passed")
    else:
        print("✗ Basic append test failed")
        return
    
    print("\nReady to run CUS trigger test.")
    input("Make sure CUS is running, then press Enter to continue...")
    
    run_cus_trigger_test()
    
    print("\nTest complete!")

if __name__ == "__main__":
    main()
