#!/usr/bin/env python3
"""
CUS Diagnostic Script - Check what CUS is seeing and configure for ExtP

This script will help diagnose why CUS isn't detecting ExtP menu interactions.
Run this when you're ready (after letting CUS run for a bit).
"""

import os
import time
from datetime import datetime

def check_cus_logs():
    """Check what CUS has been logging"""
    print("=== CUS LOG ANALYSIS ===")
    
    # Check CUS error logs
    error_log_path = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSErrors"
    if os.path.exists(error_log_path):
        try:
            error_files = os.listdir(error_log_path)
            if error_files:
                print(f"✓ Found {len(error_files)} error log files")
                # Show most recent error
                error_files.sort(key=lambda x: os.path.getmtime(os.path.join(error_log_path, x)), reverse=True)
                recent_error = error_files[0]
                print(f"Most recent error: {recent_error}")
                
                # Read the error
                with open(os.path.join(error_log_path, recent_error), 'r') as f:
                    content = f.read()
                    print(f"Error content preview:\n{content[:200]}...")
            else:
                print("✓ No error files found (good!)")
        except Exception as e:
            print(f"✗ Error reading error logs: {e}")
    else:
        print("✗ CUS error log directory not found")
    
    # Check CUS events
    events_path = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\CUSEvents"
    if os.path.exists(events_path):
        try:
            event_files = os.listdir(events_path)
            if event_files:
                print(f"✓ Found {len(event_files)} event log files")
                # Show most recent events
                event_files.sort(key=lambda x: os.path.getmtime(os.path.join(events_path, x)), reverse=True)
                for i, event_file in enumerate(event_files[:3]):
                    print(f"Recent event {i+1}: {event_file}")
                    
                    # Read the event
                    with open(os.path.join(events_path, event_file), 'r') as f:
                        content = f.read()
                        print(f"  Content: {content[:100]}...")
            else:
                print("✓ No event files found - CUS may not be triggering actions")
        except Exception as e:
            print(f"✗ Error reading event logs: {e}")
    else:
        print("✗ CUS events directory not found")

def check_simulation_dictionary():
    """Check what's in the simulation dictionary"""
    print("\n=== SIMULATION DICTIONARY ANALYSIS ===")
    
    dict_path = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\simulation_dictionary.txt"
    if os.path.exists(dict_path):
        try:
            with open(dict_path, 'r') as f:
                content = f.read()
                lines = content.strip().split('\n')
                
            print(f"✓ Simulation dictionary has {len(lines)} entries")
            
            # Show first few entries
            print("Sample triggers:")
            for i, line in enumerate(lines[:10]):
                if ':' in line:
                    trigger, action = line.split(':', 1)
                    print(f"  {i+1}. '{trigger.strip()}' -> '{action.strip()}'")
            
            # Look for DeFi/Trading related triggers
            defi_triggers = [line for line in lines if any(keyword in line.lower() for keyword in ['defi', 'trading', 'portfolio', 'menu', 'option'])]
            if defi_triggers:
                print(f"\n✓ Found {len(defi_triggers)} DeFi/Trading related triggers:")
                for trigger in defi_triggers[:5]:
                    print(f"  - {trigger}")
            else:
                print("✗ No DeFi/Trading specific triggers found")
                
        except Exception as e:
            print(f"✗ Error reading simulation dictionary: {e}")
    else:
        print("✗ Simulation dictionary file not found")

def check_screenshots():
    """Check if CUS has captured any screenshots"""
    print("\n=== SCREENSHOT ANALYSIS ===")
    
    screenshot_path = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\Screenshots"
    if os.path.exists(screenshot_path):
        try:
            screenshots = os.listdir(screenshot_path)
            if screenshots:
                print(f"✓ Found {len(screenshots)} screenshots")
                # Show most recent
                screenshots.sort(key=lambda x: os.path.getmtime(os.path.join(screenshot_path, x)), reverse=True)
                for i, screenshot in enumerate(screenshots[:3]):
                    file_path = os.path.join(screenshot_path, screenshot)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    print(f"  {i+1}. {screenshot} (taken: {mod_time})")
            else:
                print("✗ No screenshots found - CUS may not be capturing screen")
        except Exception as e:
            print(f"✗ Error reading screenshots: {e}")
    else:
        print("✗ Screenshot directory not found")

def check_defect_prompts():
    """Check if any defect prompts were generated"""
    print("\n=== DEFECT PROMPT ANALYSIS ===")
    
    defect_path = "C:\\Users\\gibea\\Documents\\GitRepos\\DeFiHuddleTradingSystem\\UserSimulator\\DefectPrompts"
    if os.path.exists(defect_path):
        try:
            # Check main directory
            items = os.listdir(defect_path)
            prompt_files = [f for f in items if f.endswith('.md')]
            
            if prompt_files:
                print(f"✓ Found {len(prompt_files)} defect prompt files")
                for i, prompt_file in enumerate(prompt_files):
                    file_path = os.path.join(defect_path, prompt_file)
                    mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    size = os.path.getsize(file_path)
                    print(f"  {i+1}. {prompt_file} (created: {mod_time}, size: {size} bytes)")
            else:
                print("✓ No defect prompts generated yet (system is working normally)")
            
            # Check subdirectories
            for subdir in ['screenshots', 'metadata']:
                subdir_path = os.path.join(defect_path, subdir)
                if os.path.exists(subdir_path):
                    subdir_items = os.listdir(subdir_path)
                    print(f"  {subdir}: {len(subdir_items)} items")
                    
        except Exception as e:
            print(f"✗ Error reading defect prompts: {e}")
    else:
        print("✗ Defect prompts directory not found")

def suggest_fixes():
    """Suggest potential fixes for CUS not detecting ExtP"""
    print("\n=== SUGGESTED FIXES ===")
    
    print("1. **Check Simulation Dictionary**:")
    print("   - Make sure ExtP's menu options are in simulation_dictionary.txt")
    print("   - Add entries like: 'Main Menu:press_enter', 'Portfolio:press_1', etc.")
    
    print("\n2. **OCR Detection Issues**:")
    print("   - ExtP's font/text might not be OCR-readable")
    print("   - Check if CUS is capturing screenshots correctly")
    print("   - Verify screen capture timing matches ExtP's refresh rate")
    
    print("\n3. **Focus/Timing Issues**:")
    print("   - CUS might be checking at wrong intervals")
    print("   - ExtP window might be losing focus")
    print("   - Check if ExtP is displaying text that CUS can read")
    
    print("\n4. **Integration Issues**:")
    print("   - Verify CUS is actually running the main detection loop")
    print("   - Check if there are any Python errors in CUS window")
    print("   - Ensure OCR libraries (pytesseract) are working properly")

def main():
    print("=== CUS DIAGNOSTIC REPORT ===")
    print(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all checks
    check_cus_logs()
    check_simulation_dictionary()
    check_screenshots()
    check_defect_prompts()
    suggest_fixes()
    
    print("\n=== NEXT STEPS ===")
    print("1. Review the analysis above")
    print("2. Check CUS window for any error messages")
    print("3. Verify ExtP is showing text that CUS can detect")
    print("4. Consider updating simulation_dictionary.txt with ExtP-specific triggers")

if __name__ == "__main__":
    main()
