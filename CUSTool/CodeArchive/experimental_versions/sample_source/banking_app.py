
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
