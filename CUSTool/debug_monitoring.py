#!/usr/bin/env python3

import os
import time
import threading
from datetime import datetime

def debug_monitoring_loop():
    """Debug version of the monitoring loop to understand what's happening"""
    
    print("=== DEBUG MONITORING LOOP ===", flush=True)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
    
    # Simulate the monitoring loop with detailed logging
    loop_count = 0
    start_time = time.time()
    
    try:
        while True:
            loop_count += 1
            current_time = time.time()
            elapsed = current_time - start_time
            
            print(f"Loop {loop_count}: Running at {datetime.now().strftime('%H:%M:%S')} (elapsed: {elapsed:.1f}s)", flush=True)
            
            # Simulate screen capture
            print("  - Simulating screen capture...", flush=True)
            time.sleep(0.1)  # Simulate capture time
            
            # Simulate OCR processing
            print("  - Simulating OCR processing...", flush=True)
            time.sleep(0.1)  # Simulate OCR time
            
            # Simulate dictionary reload check
            print("  - Checking dictionary reload...", flush=True)
            
            # Simulate error folder monitoring
            print("  - Checking error folder...", flush=True)
            
            print(f"  - Loop {loop_count} completed, sleeping for 2 seconds", flush=True)
            print("", flush=True)  # Empty line for readability
            
            # Sleep for 2 seconds (same as CUS)
            time.sleep(2)
            
            # Stop after 5 loops for testing
            if loop_count >= 5:
                print("=== DEBUG COMPLETE (5 loops) ===", flush=True)
                break
                
    except KeyboardInterrupt:
        print(f"\n=== DEBUG INTERRUPTED (after {loop_count} loops) ===", flush=True)
    except Exception as e:
        print(f"\n=== DEBUG ERROR: {e} ===", flush=True)

if __name__ == "__main__":
    debug_monitoring_loop()
