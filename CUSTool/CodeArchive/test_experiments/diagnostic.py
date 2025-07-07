#!/usr/bin/env python3
"""
Simple diagnostic script to check if the CUS system is working properly.
This script performs basic checks without running intensive operations.
"""

import sys
import os
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    print(f"Python version: {sys.version}")
    if sys.version_info < (3, 8):
        print("⚠️  Warning: Python 3.8+ recommended")
    else:
        print("✓ Python version is compatible")

def check_required_modules():
    """Check if required modules are available."""
    required_modules = ['watchdog', 'pynput', 'psutil', 'json', 'logging', 'threading']
    
    for module in required_modules:
        try:
            if importlib.util.find_spec(module) is not None:
                print(f"✓ {module} module available")
            else:
                print(f"❌ {module} module NOT available")
        except ImportError:
            print(f"❌ {module} module NOT available")

def check_file_structure():
    """Check if required files exist."""
    required_files = [
        'CUS.py',
        'CUS_safe.py', 
        'test_CUS_safe.py',
        'simulation_dictionary.txt',
        'requirements.txt'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"❌ {file} missing")

def check_directories():
    """Check if required directories exist."""
    required_dirs = ['Logs', 'NewErrors', 'NewEvents']
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")

def main():
    print("CUS System Diagnostic")
    print("=" * 50)
    
    print("\n1. Python Environment Check:")
    check_python_version()
    
    print("\n2. Required Modules Check:")
    check_required_modules()
    
    print("\n3. File Structure Check:")
    check_file_structure()
    
    print("\n4. Directory Structure Check:")
    check_directories()
    
    print("\n5. CUS Module Import Test:")
    try:
        import CUS_safe
        print("✓ CUS_safe module imported successfully")
    except Exception as e:
        print(f"❌ Failed to import CUS_safe: {e}")
    
    print("\n" + "=" * 50)
    print("Diagnostic completed!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
