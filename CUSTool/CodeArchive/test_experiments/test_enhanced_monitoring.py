#!/usr/bin/env python3

import sys
import os
import time

# Add the CUSTool directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the enhanced CUS
from CUS import (
    load_simulation_dictionary,
    prompt_user_for_focus_and_switch,
    capture_and_process_screen,
    safe_print,
    datetime,
    POLL_INTERVAL,
    NEW_ERRORS_PATH
)

def test_enhanced_monitoring():
    """Test the enhanced monitoring feedback"""
    print("=== TESTING ENHANCED MONITORING FEEDBACK ===", flush=True)
    
    # Load simulation dictionary
    simulation_dictionary = load_simulation_dictionary()
    print(f"Loaded {len(simulation_dictionary)} simulation rules", flush=True)
    
    # Test the focus prompt
    print("\n--- Testing Focus Prompt ---", flush=True)
    focus_success = prompt_user_for_focus_and_switch()
    
    if not focus_success:
        print("Focus setup failed or cancelled", flush=True)
        return
    
    print("\n--- Starting Enhanced Monitoring Test ---", flush=True)
    print("This will run for 30 seconds to demonstrate the enhanced feedback", flush=True)
    print("Press Ctrl+C to stop early", flush=True)
    
    try:
        loop_count = 0
        previous_text = ""
        start_time = time.time()
        
        while True:
            # Check if we've run for 30 seconds
            if time.time() - start_time > 30:
                print("\n30-second test completed!", flush=True)
                break
                
            time.sleep(POLL_INTERVAL)
            loop_count += 1
            current_time = time.time()
            elapsed_minutes = (current_time - start_time) / 60
            
            # Show periodic status with timestamp - same as enhanced CUS
            if loop_count % 10 == 0:  # Every 30 seconds (3s * 10)
                safe_print(f"[{datetime.now().strftime('%H:%M:%S')}] Monitoring active - Loop {loop_count} ({elapsed_minutes:.1f} min elapsed)")
            elif loop_count % 5 == 0:  # Every 15 seconds, show a dot
                print(".", end="", flush=True)
            
            # Simulate screen capture and processing
            previous_text = capture_and_process_screen(simulation_dictionary, previous_text)
                
    except KeyboardInterrupt:
        print("\nTest interrupted by user", flush=True)
    
    print("=== ENHANCED MONITORING TEST COMPLETE ===", flush=True)

if __name__ == "__main__":
    test_enhanced_monitoring()
