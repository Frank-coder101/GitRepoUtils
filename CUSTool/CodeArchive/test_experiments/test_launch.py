import os
import time
import subprocess

# Test script to safely test CUS launch functionality
def test_external_program_launch():
    """Test the external program launch functionality safely"""
    
    # Check if the external program exists
    external_program = "C:\\Users\\gibea\\Documents\\GitRepos\\DeFiHuddleTradingSystem\\main.py"
    output_log = "C:\\Users\\gibea\\Documents\\GitRepoUtils\\CUSTool\\Logs\\output.log"
    
    print("=== CUS External Program Launch Test ===")
    print(f"Testing external program: {external_program}")
    print(f"Output log file: {output_log}")
    
    # Check if external program exists
    if os.path.exists(external_program):
        print("✅ External program file exists")
    else:
        print("❌ External program file NOT FOUND")
        print("This will cause CUS to fail when launching")
        return False
    
    # Check if output directory exists
    output_dir = os.path.dirname(output_log)
    if os.path.exists(output_dir):
        print("✅ Output directory exists")
    else:
        print("❌ Output directory NOT FOUND")
        os.makedirs(output_dir, exist_ok=True)
        print("✅ Created output directory")
    
    # Test launching with a safer command (just python version check)
    try:
        print("\n=== Testing Python execution ===")
        result = subprocess.run(["python", "--version"], capture_output=True, text=True, timeout=5)
        print(f"Python version: {result.stdout.strip()}")
        print("✅ Python execution works")
    except Exception as e:
        print(f"❌ Python execution failed: {e}")
        return False
    
    # Test if we can read the simulation dictionary
    try:
        print("\n=== Testing Simulation Dictionary ===")
        sim_dict_file = "simulation_dictionary.txt"
        if os.path.exists(sim_dict_file):
            with open(sim_dict_file, "r") as f:
                content = f.read()
                print(f"✅ Simulation dictionary exists: {len(content)} characters")
        else:
            print("❌ Simulation dictionary NOT FOUND")
            return False
    except Exception as e:
        print(f"❌ Error reading simulation dictionary: {e}")
        return False
    
    print("\n=== Test Summary ===")
    print("✅ All preliminary checks passed")
    print("⚠️  WARNING: CUS will try to launch the external program")
    print("⚠️  This may cause VS Code to close if the external program has issues")
    
    return True

if __name__ == "__main__":
    success = test_external_program_launch()
    if not success:
        print("\n❌ Pre-launch tests FAILED - Do not run CUS yet!")
        input("Press Enter to continue...")
    else:
        print("\n✅ Pre-launch tests PASSED")
        response = input("Do you want to test CUS launch? (y/N): ")
        if response.lower() == 'y':
            print("Launching CUS in 3 seconds...")
            time.sleep(3)
            # Import and test CUS launch
            try:
                import CUS
                print("Testing external program launch...")
                CUS.launch_external_program()
                print("✅ External program launch completed")
                time.sleep(2)
                print("✅ Test completed successfully")
            except Exception as e:
                print(f"❌ CUS launch failed: {e}")
        else:
            print("Test cancelled by user")
