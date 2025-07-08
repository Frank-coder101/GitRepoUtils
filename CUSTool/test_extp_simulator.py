"""
Test ExtP Simulator - Simulates the DeFi Huddle Trading System for CUS testing
This script simulates the ExtP behavior including the known false negative issue
when pressing key 1 and ENTER (displays "Trading system is already configured")
"""

import time
import sys

def display_menu():
    """Display the main menu"""
    print("\n" + "="*50)
    print("DeFi Huddle Trading System")
    print("="*50)
    print("1. Configure Trading System")
    print("2. Start Trading Bot")
    print("3. View Portfolio")
    print("4. Exit")
    print("="*50)
    print("Select an option: ", end="", flush=True)

def handle_option_1():
    """Handle option 1 - This contains the false negative issue"""
    print("\nProcessing option 1...")
    time.sleep(1)
    
    # This is the false negative issue that CUS should detect
    print("Trading system is already configured")
    print("No further configuration needed.")
    time.sleep(2)
    
    return True

def handle_option_2():
    """Handle option 2"""
    print("\nStarting trading bot...")
    time.sleep(1)
    print("Trading bot started successfully!")
    time.sleep(2)
    return True

def handle_option_3():
    """Handle option 3"""
    print("\nViewing portfolio...")
    time.sleep(1)
    print("Portfolio Balance: $10,000")
    print("Active Positions: 3")
    time.sleep(2)
    return True

def handle_option_4():
    """Handle option 4 - Exit"""
    print("\nExiting trading system...")
    time.sleep(1)
    print("Goodbye!")
    return False

def main():
    """Main application loop"""
    print("Starting DeFi Huddle Trading System Test Simulator...")
    print("This simulator includes the known false negative issue for CUS testing.")
    time.sleep(2)
    
    running = True
    while running:
        display_menu()
        
        try:
            # Get user input
            choice = input().strip()
            
            if choice == "1":
                running = handle_option_1()
            elif choice == "2":
                running = handle_option_2()
            elif choice == "3":
                running = handle_option_3()
            elif choice == "4":
                running = handle_option_4()
            else:
                print(f"\nInvalid option: {choice}")
                print("Please select a valid option (1-4)")
                time.sleep(2)
                
        except KeyboardInterrupt:
            print("\n\nReceived interrupt signal. Exiting...")
            break
        except Exception as e:
            print(f"\nError: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
