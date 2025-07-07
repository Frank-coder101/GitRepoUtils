#!/usr/bin/env python3
"""
Test script to check GitHub Copilot API access capabilities
"""
import requests
import json
import os
import sys
from datetime import datetime

def test_copilot_api_access():
    """Test various methods to access GitHub Copilot programmatically"""
    
    print("=== COPILOT API ACCESS TEST ===")
    print(f"Test started at: {datetime.now()}")
    print()
    
    # Test 1: Check for VS Code Copilot extension API
    print("1. Testing VS Code Extension API...")
    try:
        # This would be the ideal way if available
        import vscode
        print("✓ VS Code Python API available")
        
        # Try to access Copilot extension
        copilot_ext = vscode.extensions.getExtension('GitHub.copilot')
        if copilot_ext:
            print("✓ GitHub Copilot extension found")
            print(f"   Version: {copilot_ext.packageJSON.get('version', 'unknown')}")
            return True
        else:
            print("✗ GitHub Copilot extension not accessible")
    except ImportError:
        print("✗ VS Code Python API not available")
    except Exception as e:
        print(f"✗ VS Code API error: {e}")
    
    # Test 2: Check for GitHub Copilot REST API
    print("\n2. Testing GitHub Copilot REST API...")
    try:
        # Check if we can access GitHub API with Copilot endpoints
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'CUS-Test-Script'
        }
        
        # Try to access GitHub API (this won't work without auth, but tests connectivity)
        response = requests.get('https://api.github.com/user', headers=headers, timeout=5)
        print(f"   GitHub API response: {response.status_code}")
        
        if response.status_code == 401:
            print("✓ GitHub API accessible (authentication required)")
        else:
            print("✗ GitHub API not accessible or unexpected response")
            
    except Exception as e:
        print(f"✗ GitHub API error: {e}")
    
    # Test 3: Check for local Copilot processes
    print("\n3. Testing for local Copilot processes...")
    try:
        import psutil
        copilot_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'copilot' in proc.info['name'].lower():
                    copilot_processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if copilot_processes:
            print(f"✓ Found {len(copilot_processes)} Copilot-related processes")
            for proc in copilot_processes[:3]:  # Show first 3
                print(f"   PID: {proc['pid']}, Name: {proc['name']}")
        else:
            print("✗ No Copilot processes found")
            
    except ImportError:
        print("✗ psutil not available (install with: pip install psutil)")
    except Exception as e:
        print(f"✗ Process check error: {e}")
    
    # Test 4: Check for Copilot configuration files
    print("\n4. Testing for Copilot configuration...")
    config_paths = [
        os.path.expanduser("~/.vscode/extensions"),
        os.path.expanduser("~/.vscode-insiders/extensions"),
        os.path.expanduser("~/AppData/Roaming/Code/User"),
        os.path.expanduser("~/Library/Application Support/Code/User")
    ]
    
    copilot_configs = []
    for path in config_paths:
        if os.path.exists(path):
            try:
                for item in os.listdir(path):
                    if 'copilot' in item.lower():
                        copilot_configs.append(os.path.join(path, item))
            except PermissionError:
                pass
    
    if copilot_configs:
        print(f"✓ Found {len(copilot_configs)} Copilot-related config items")
        for config in copilot_configs[:3]:  # Show first 3
            print(f"   {config}")
    else:
        print("✗ No Copilot configuration found")
    
    print("\n=== CONCLUSION ===")
    print("Direct programmatic API access appears LIMITED.")
    print("Recommendation: Use standardized prompt approach with JSON output.")
    
    return False

def test_large_data_handling():
    """Test how much data we can handle in prompts"""
    
    print("\n=== LARGE DATA HANDLING TEST ===")
    
    # Generate test data of various sizes
    test_sizes = [1000, 5000, 10000, 50000, 100000]  # characters
    
    for size in test_sizes:
        test_data = "x" * size
        print(f"Test data size: {size:,} characters ({size/1024:.1f} KB)")
        
        # This simulates what we'd send to Copilot
        prompt_template = f"""
        Please analyze this ExtP codebase and generate requirements:
        
        ExtP Code Data:
        {test_data}
        
        Generate: requirements.json, validation_rules.json
        """
        
        prompt_size = len(prompt_template)
        print(f"   Total prompt size: {prompt_size:,} characters ({prompt_size/1024:.1f} KB)")
        
        # Practical limits (these are rough estimates)
        if prompt_size < 8000:
            print("   ✓ Size: SAFE - Well within limits")
        elif prompt_size < 32000:
            print("   ⚠ Size: CAUTION - May work but could hit limits")
        elif prompt_size < 128000:
            print("   ⚠ Size: RISKY - Likely to hit context limits")
        else:
            print("   ✗ Size: TOO LARGE - Will definitely hit limits")
    
    print("\nRecommendation: Keep total context under 32KB for reliability")

if __name__ == "__main__":
    print("Testing GitHub Copilot API access and data handling capabilities...")
    print("=" * 60)
    
    # Test API access
    api_available = test_copilot_api_access()
    
    # Test data handling
    test_large_data_handling()
    
    print("\n" + "=" * 60)
    print("Test completed. Check results above.")
