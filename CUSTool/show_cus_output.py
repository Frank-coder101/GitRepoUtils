#!/usr/bin/env python3
"""Test script to show CUS startup output"""

import subprocess
import os
import time

def test_cus_startup():
    """Test CUS startup and show output"""
    print("=== Testing CUS Startup ===")
    
    # Change to the CUS directory
    os.chdir(r"c:\Users\gibea\Documents\GitRepoUtils\CUSTool")
    
    # Run CUS with timeout to show startup
    try:
        process = subprocess.Popen(
            [r"c:/Users/gibea/Documents/GitRepoUtils/.venv/Scripts/python.exe", "CUS.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Let it run for a few seconds to show startup
        time.sleep(8)
        
        # Terminate and get output
        process.terminate()
        stdout, stderr = process.communicate()
        
        print("=== CUS STARTUP OUTPUT ===")
        print(stdout)
        
        if stderr:
            print("=== STDERR ===")
            print(stderr)
        
        print(f"=== Process finished with return code: {process.returncode} ===")
        
    except Exception as e:
        print(f"Error running CUS: {e}")

if __name__ == "__main__":
    test_cus_startup()
