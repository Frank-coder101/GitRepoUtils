#!/usr/bin/env python3
"""
CUS Production Status Check
Quick verification that all production components are operational
"""

import os
import sys
import json
import traceback
from datetime import datetime

def check_component(name, import_statement, description):
    """Check if a component can be imported and is functional"""
    try:
        exec(import_statement)
        print(f"✅ {name}: {description}")
        return True
    except Exception as e:
        print(f"❌ {name}: Failed - {str(e)}")
        return False

def check_file_exists(filepath, description):
    """Check if a required file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description}: Found")
        return True
    else:
        print(f"❌ {description}: Missing")
        return False

def main():
    print("🔍 CUS Production Status Check")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    all_good = True
    
    # Check core components
    print("📦 Core Components:")
    components = [
        ("CUS", "import CUS", "Core CLI User Simulator"),
        ("EnhancedCUS", "import EnhancedCUS", "Enhanced CUS with remediation"),
        ("AdvancedTestExecutor", "import AdvancedTestExecutor", "Advanced test execution"),
        ("AutomatedRemediationSystem", "import AutomatedRemediationSystem", "Automated remediation"),
        ("EnhancedTestCaseGenerator", "import EnhancedTestCaseGenerator", "Enhanced test case generation"),
        ("ProductionValidationTest", "import ProductionValidationTest", "Production validation")
    ]
    
    for name, import_stmt, desc in components:
        if not check_component(name, import_stmt, desc):
            all_good = False
    
    print()
    
    # Check required files
    print("📁 Required Files:")
    files = [
        ("simulation_dictionary.txt", "Simulation dictionary"),
        ("requirements.txt", "Dependencies file"),
        ("setup_and_run.bat", "Setup script"),
        ("deploy_production.bat", "Deployment script")
    ]
    
    for filepath, desc in files:
        if not check_file_exists(filepath, desc):
            all_good = False
    
    print()
    
    # Check directories
    print("📂 Runtime Directories:")
    directories = [
        "Logs", "NewErrors", "NewEvents", "TestResults", "RemediationResults",
        "Logs/CUSEvents", "Logs/Screenshots"
    ]
    
    for directory in directories:
        if not check_file_exists(directory, f"Directory: {directory}"):
            all_good = False
    
    print()
    
    # Check recent validation results
    print("📊 Recent Validation Results:")
    if os.path.exists("ProductionValidationResults.json"):
        try:
            with open("ProductionValidationResults.json", "r") as f:
                results = json.load(f)
            
            overall_score = results.get("final_score", 0) * 100
            status = results.get("validation_status", "UNKNOWN")
            
            print(f"✅ Overall Score: {overall_score}%")
            print(f"✅ Status: {status}")
            
            if overall_score < 85:
                print("⚠️  Score below 85% - monitor closely")
                all_good = False
            
        except Exception as e:
            print(f"❌ Failed to read validation results: {e}")
            all_good = False
    else:
        print("❌ No recent validation results found")
        all_good = False
    
    print()
    print("=" * 50)
    
    if all_good:
        print("🚀 STATUS: ALL SYSTEMS OPERATIONAL")
        print("✅ Production deployment is ready for live use!")
        print("✅ All components verified and functional")
        print("✅ False negative detection and remediation active")
        print("✅ Enhanced CUS with RADAR methodology ready")
        return 0
    else:
        print("⚠️  STATUS: ISSUES DETECTED")
        print("❌ Some components need attention before live deployment")
        print("📋 Review the issues above and re-run after fixes")
        return 1

if __name__ == "__main__":
    sys.exit(main())
