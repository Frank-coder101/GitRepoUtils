#!/usr/bin/env python3
"""Test script to run CUS and capture output"""

import subprocess
import sys
import os

def run_cus_with_output():
    """Run CUS and capture its output"""
    print("=== Testing CUS Production Mode ===")
    
    # Change to the CUS directory
    os.chdir(r"c:\Users\gibea\Documents\GitRepoUtils\CUSTool")
    
    # Run CUS with timeout
    try:
        result = subprocess.run(
            [r"c:/Users/gibea/Documents/GitRepoUtils/.venv/Scripts/python.exe", "CUS.py"],
            capture_output=True,
            text=True,
            timeout=10  # 10 second timeout
        )
        
        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        print(f"\nReturn code: {result.returncode}")
        
    except subprocess.TimeoutExpired:
        print("CUS ran for 10 seconds (timeout reached) - this is expected for a monitoring service")
    except Exception as e:
        print(f"Error running CUS: {e}")

if __name__ == "__main__":
    run_cus_with_output()
