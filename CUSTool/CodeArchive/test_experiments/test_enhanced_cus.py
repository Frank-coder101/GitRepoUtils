"""
Test script for Enhanced CUS components
This script tests all components without requiring ExtP to be running
"""

import os
import json
import time
from pathlib import Path

def test_auto_generation():
    """Test auto-generation components"""
    print("=== Testing Auto-Generation Components ===")
    
    try:
        from auto_generate_dictionary import SourceCodeAnalyzer, SimulationDictionaryGenerator, SmartExplorer
        
        # Test with a dummy source directory
        test_source = Path("test_source")
        test_source.mkdir(exist_ok=True)
        
        # Create a dummy source file
        dummy_code = '''
        print("Select an option:")
        print("1. Option One")
        print("2. Option Two")
        print("3. Exit")
        choice = input("Enter your choice (1-3): ")
        
        if choice == "1":
            password = input("Enter password: ")
            print("Continue? (y/n)")
        '''
        
        with open(test_source / "dummy_app.py", "w") as f:
            f.write(dummy_code)
        
        # Test analyzer
        analyzer = SourceCodeAnalyzer(str(test_source))
        menu_options = analyzer.analyze_directory()
        
        print(f"✓ Found {len(menu_options)} menu options")
        
        # Test generator
        generator = SimulationDictionaryGenerator(menu_options)
        rules_dict = generator.generate_rules()
        
        print(f"✓ Generated {len(rules_dict)} simulation rules")
        
        # Test explorer
        explorer = SmartExplorer(generator.simulation_rules)
        exploration_plan = explorer.generate_exploration_plan()
        
        print(f"✓ Generated {len(exploration_plan)} exploration scenarios")
        
        # Clean up
        os.remove(test_source / "dummy_app.py")
        test_source.rmdir()
        
        return True
        
    except Exception as e:
        print(f"✗ Auto-generation test failed: {e}")
        return False

def test_enhanced_cus():
    """Test Enhanced CUS components"""
    print("\n=== Testing Enhanced CUS Components ===")
    
    try:
        # Test configuration loading
        from enhanced_cus import EnhancedCUS
        
        # Create test config
        test_config = {
            "safe_mode": True,
            "poll_interval": 1,
            "simulation_dictionary_path": "test_dict.json",
            "exploration_plan_path": "test_plan.json"
        }
        
        with open("test_config.json", "w") as f:
            json.dump(test_config, f)
        
        # Test CUS initialization
        cus = EnhancedCUS("test_config.json")
        print("✓ Enhanced CUS initialized successfully")
        
        # Test simulation dictionary creation
        test_dict = {
            "Select an option": "type_1",
            "Enter password": "type_test123",
            "Continue? (y/n)": "type_y"
        }
        
        with open("test_dict.json", "w") as f:
            json.dump(test_dict, f)
        
        # Test exploration plan creation
        test_plan = [
            {
                "name": "Test Scenario",
                "actions": ["type_1"],
                "priority": 10,
                "expected_prompts": ["Select an option"],
                "strategy": "systematic"
            }
        ]
        
        with open("test_plan.json", "w") as f:
            json.dump(test_plan, f)
        
        # Test loading
        cus.load_simulation_dictionary()
        cus.load_exploration_plan()
        
        print("✓ Dictionary and plan loaded successfully")
        
        # Test action execution (safe mode)
        success = cus.execute_action("type_test")
        print(f"✓ Action execution test: {'passed' if success else 'failed'}")
        
        # Test coverage tracker
        cus.coverage_tracker.track_interaction("test_prompt", "test_action")
        report = cus.coverage_tracker.get_coverage_report()
        
        print(f"✓ Coverage tracking: {report['total_interactions']} interactions logged")
        
        # Clean up
        os.remove("test_config.json")
        os.remove("test_dict.json")
        os.remove("test_plan.json")
        
        return True
        
    except Exception as e:
        print(f"✗ Enhanced CUS test failed: {e}")
        return False

def test_ocr_availability():
    """Test OCR components availability"""
    print("\n=== Testing OCR Components ===")
    
    try:
        import pytesseract
        from PIL import Image, ImageGrab
        import pynput
        import pyautogui
        
        print("✓ All OCR and automation libraries available")
        
        # Test Tesseract
        try:
            version = pytesseract.get_tesseract_version()
            print(f"✓ Tesseract version: {version}")
        except:
            print("⚠ Tesseract OCR not found in PATH")
        
        return True
        
    except ImportError as e:
        print(f"✗ Missing required library: {e}")
        return False

def test_directory_structure():
    """Test directory structure creation"""
    print("\n=== Testing Directory Structure ===")
    
    try:
        # Test directory creation
        test_dirs = [
            "Logs/Screenshots",
            "Logs/CUSEvents", 
            "Logs/Reports",
            "Logs/CUSErrors"
        ]
        
        for dir_path in test_dirs:
            os.makedirs(dir_path, exist_ok=True)
            if os.path.exists(dir_path):
                print(f"✓ {dir_path}")
            else:
                print(f"✗ {dir_path}")
        
        return True
        
    except Exception as e:
        print(f"✗ Directory structure test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Enhanced CUS Test Suite ===")
    print("This script tests all components without requiring ExtP\n")
    
    tests = [
        ("Directory Structure", test_directory_structure),
        ("OCR Availability", test_ocr_availability),
        ("Auto-Generation", test_auto_generation),
        ("Enhanced CUS", test_enhanced_cus)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        if test_func():
            passed += 1
        print()
    
    print("=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("\n🎉 All tests passed! Enhanced CUS is ready to use.")
    else:
        print(f"\n⚠ {total-passed} test(s) failed. Please check the output above.")
    
    print("\nNext steps:")
    print("1. Run 'run_enhanced_cus.bat' to use the enhanced system")
    print("2. Use option 1 to auto-generate dictionary from ExtP source")
    print("3. Use option 2 or 3 to run CUS with the generated dictionary")

if __name__ == "__main__":
    main()
