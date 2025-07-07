#!/usr/bin/env python3
"""
Demo Script for CUS Intelligent Testing System

This script demonstrates the new TestCaseCreator and SequenceRunner components
by creating sample test cases and executing them in simulation mode.
"""

import os
import json
import time
from datetime import datetime

# Import our new components
from TestCaseCreator import TestCaseCreator
from SequenceRunner import SequenceRunner

def create_sample_source_file():
    """Create a sample source file to analyze"""
    sample_code = '''
def main_menu():
    """Main menu function"""
    print("=== MAIN MENU ===")
    print("1. View Account Balance")
    print("2. Transfer Money")
    print("3. Account Settings")
    print("4. Transaction History")
    print("5. Exit")
    
    choice = input("Select an option (1-5): ")
    
    if choice == "1":
        view_balance()
    elif choice == "2":
        transfer_menu()
    elif choice == "3":
        settings_menu()
    elif choice == "4":
        transaction_history()
    elif choice == "5":
        print("Thank you for using our service!")
        return False
    else:
        print("Invalid option. Please try again.")
    
    return True

def view_balance():
    """View account balance"""
    print("Current Balance: $1,234.56")
    input("Press Enter to continue...")

def transfer_menu():
    """Money transfer menu"""
    print("=== MONEY TRANSFER ===")
    recipient = input("Enter recipient account number: ")
    amount = input("Enter amount to transfer: $")
    
    confirm = input(f"Transfer ${amount} to {recipient}? (y/n): ")
    if confirm.lower() == 'y':
        print("Transfer completed successfully!")
    else:
        print("Transfer cancelled.")
    
    input("Press Enter to continue...")

def settings_menu():
    """Account settings menu"""
    print("=== ACCOUNT SETTINGS ===")
    print("1. Change Password")
    print("2. Update Profile")
    print("3. Security Settings")
    print("4. Back to Main Menu")
    
    choice = input("Select an option (1-4): ")
    
    if choice == "1":
        change_password()
    elif choice == "2":
        update_profile()
    elif choice == "3":
        security_settings()
    elif choice == "4":
        return
    else:
        print("Invalid option.")

def change_password():
    """Change password"""
    old_password = input("Enter current password: ")
    new_password = input("Enter new password: ")
    confirm_password = input("Confirm new password: ")
    
    if new_password == confirm_password:
        print("Password changed successfully!")
    else:
        print("Passwords do not match!")
    
    input("Press Enter to continue...")

def update_profile():
    """Update user profile"""
    print("=== UPDATE PROFILE ===")
    name = input("Enter your name: ")
    email = input("Enter your email: ")
    phone = input("Enter your phone: ")
    
    print("Profile updated successfully!")
    input("Press Enter to continue...")

def security_settings():
    """Security settings"""
    print("=== SECURITY SETTINGS ===")
    print("1. Enable Two-Factor Authentication")
    print("2. View Login History")
    print("3. Lock Account")
    print("4. Back")
    
    choice = input("Select an option (1-4): ")
    # Implementation would continue here...
    
def transaction_history():
    """View transaction history"""
    print("=== TRANSACTION HISTORY ===")
    print("Loading transactions...")
    time.sleep(1)  # Simulate loading
    
    print("Recent Transactions:")
    print("1. 2024-01-15: Transfer to Account 123 - $50.00")
    print("2. 2024-01-14: ATM Withdrawal - $100.00")
    print("3. 2024-01-13: Direct Deposit - $2,500.00")
    
    input("Press Enter to continue...")

if __name__ == "__main__":
    print("Banking System Demo")
    while main_menu():
        pass
'''
    
    # Create sample source directory
    sample_dir = "sample_source"
    os.makedirs(sample_dir, exist_ok=True)
    
    # Write sample file
    with open(os.path.join(sample_dir, "banking_app.py"), "w") as f:
        f.write(sample_code)
    
    return sample_dir

def demo_test_case_creator():
    """Demo the TestCaseCreator component"""
    print("=== DEMO: TestCaseCreator ===")
    
    # Create sample source file
    sample_dir = create_sample_source_file()
    print(f"Created sample source code in: {sample_dir}")
    
    # Initialize TestCaseCreator
    creator = TestCaseCreator()
    
    # Run analysis
    print("Running source code analysis...")
    results = creator.run_full_analysis([sample_dir])
    
    print(f"\nAnalysis Results:")
    print(f"- Menu options found: {len(results['menu_options'])}")
    print(f"- Simulation rules generated: {len(results['simulation_dict'])}")
    print(f"- Test sequences created: {len(results['test_sequences'])}")
    
    # Display some extracted menu options
    print(f"\nExtracted Menu Options:")
    for i, (trigger, option) in enumerate(results['menu_options'].items()):
        if i < 5:  # Show first 5
            print(f"  {i+1}. '{trigger}' -> Expected inputs: {option.expected_inputs}")
    
    if len(results['menu_options']) > 5:
        print(f"  ... and {len(results['menu_options']) - 5} more")
    
    # Display test sequences
    print(f"\nGenerated Test Sequences:")
    for i, seq in enumerate(results['test_sequences']):
        if i < 3:  # Show first 3
            print(f"  {i+1}. {seq.name} - Priority: {seq.priority}")
            print(f"     Description: {seq.description}")
            print(f"     Steps: {len(seq.steps)}")
    
    if len(results['test_sequences']) > 3:
        print(f"  ... and {len(results['test_sequences']) - 3} more")
    
    # Show coverage report
    coverage = results['coverage_report']
    print(f"\nCoverage Report:")
    print(f"- Total sequences: {coverage['total_test_sequences']}")
    print(f"- Priority 1 sequences: {coverage['priority_distribution'].get(1, 0)}")
    print(f"- Priority 2 sequences: {coverage['priority_distribution'].get(2, 0)}")
    print(f"- Priority 3 sequences: {coverage['priority_distribution'].get(3, 0)}")
    
    return True

def demo_sequence_runner():
    """Demo the SequenceRunner component"""
    print("\n=== DEMO: SequenceRunner ===")
    
    # Initialize SequenceRunner
    runner = SequenceRunner()
    
    # Load test sequences (created by TestCaseCreator)
    if os.path.exists("test_sequences.json"):
        success = runner.load_test_sequences()
        if success:
            print(f"Loaded {len(runner.sequences)} test sequences")
        else:
            print("Failed to load test sequences")
            return False
    else:
        print("No test sequences found. Run TestCaseCreator first.")
        return False
    
    # Show execution plan
    plan = runner.create_execution_plan()
    print(f"\nExecution Plan ({len(plan)} sequences):")
    for i, seq in enumerate(plan):
        if i < 5:  # Show first 5
            print(f"  {i+1}. {seq.name} - Priority: {seq.priority}")
    
    if len(plan) > 5:
        print(f"  ... and {len(plan) - 5} more")
    
    # Execute sequences in simulation mode
    print(f"\nExecuting sequences in simulation mode...")
    start_time = time.time()
    
    success = runner.run_all_sequences()
    
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"\nExecution completed in {execution_time:.2f} seconds")
    
    # Show execution summary
    status = runner.get_execution_status()
    print(f"\nExecution Summary:")
    print(f"- Total sequences: {status['total_sequences']}")
    print(f"- Completed: {status['completed_sequences']}")
    print(f"- Failed: {status['failed_sequences']}")
    print(f"- Skipped: {status['skipped_sequences']}")
    print(f"- Coverage: {status['coverage_percentage']:.1f}%")
    
    # Generate reports
    print(f"\nGenerating reports...")
    runner.generate_html_report("demo_report.html")
    runner.save_execution_log("demo_log.json")
    
    print(f"Reports generated:")
    print(f"- HTML report: demo_report.html")
    print(f"- JSON log: demo_log.json")
    
    return True

def demo_integration():
    """Demo the integration between components"""
    print("\n=== DEMO: Component Integration ===")
    
    # This would demonstrate how MasterController coordinates everything
    # For now, we'll show the workflow
    
    workflow_steps = [
        "1. MasterController initializes components",
        "2. TestCaseCreator analyzes source code",
        "3. TestCaseCreator generates simulation dictionary",
        "4. TestCaseCreator creates test sequences",
        "5. SequenceRunner loads test sequences",
        "6. SequenceRunner executes sequences",
        "7. MasterController generates final report",
        "8. Results saved to session directory"
    ]
    
    print("Integration Workflow:")
    for step in workflow_steps:
        print(f"  {step}")
    
    print(f"\nKey Integration Points:")
    print(f"- TestCaseCreator -> simulation_dictionary.txt -> CUS.py")
    print(f"- TestCaseCreator -> test_sequences.json -> SequenceRunner")
    print(f"- SequenceRunner -> CUS.py (for actual simulation)")
    print(f"- MasterController -> orchestrates all components")
    
    return True

def main():
    """Main demo function"""
    print("=== CUS INTELLIGENT TESTING SYSTEM DEMO ===")
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Demo TestCaseCreator
        if demo_test_case_creator():
            print("✓ TestCaseCreator demo completed successfully")
        else:
            print("✗ TestCaseCreator demo failed")
            return
        
        # Demo SequenceRunner
        if demo_sequence_runner():
            print("✓ SequenceRunner demo completed successfully")
        else:
            print("✗ SequenceRunner demo failed")
            return
        
        # Demo Integration
        if demo_integration():
            print("✓ Integration demo completed successfully")
        else:
            print("✗ Integration demo failed")
            return
        
        print()
        print("=== DEMO COMPLETED SUCCESSFULLY ===")
        print("Files created:")
        print("- sample_source/banking_app.py (sample source code)")
        print("- simulation_dictionary.txt (generated simulation rules)")
        print("- test_sequences.json (generated test sequences)")
        print("- demo_report.html (execution report)")
        print("- demo_log.json (execution log)")
        print()
        print("Next steps:")
        print("1. Review the generated files to understand the system")
        print("2. Try running MasterController.py for full automation")
        print("3. Configure your own external program for testing")
        print("4. Analyze your program's source code for comprehensive testing")
        
    except Exception as e:
        print(f"Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
