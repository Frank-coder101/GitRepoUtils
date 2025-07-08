from src.core.config_manager import ConfigManager
from src.core.logger import Logger
from src.core.emergency_stop import EmergencyStop

def run_cli_wizard(config):
    Logger.init()
    Logger.info("Test log message: CLI wizard started.")
    print("Welcome to DeFi Huddle Trading System Setup Wizard!")
    while True:
        print("\nOptions:")
        print("1. Configure trading system")
        print("2. Activate EMERGENCY STOP")
        print("3. Deactivate EMERGENCY STOP")
        print("4. Show EMERGENCY STOP status")
        print("5. Exit wizard")
        choice = input("Select an option: ").strip()
        Logger.info(f"User selected option: {choice}")
        Logger.info(f"Raw user input: {choice}")
        try:
            choice = int(choice)
        except ValueError:
            Logger.error(f"Invalid input: {choice} is not a number.")
            print("Invalid input. Please enter a number between 1 and 5.")
            continue
        if choice < 1 or choice > 5:
            Logger.error(f"Invalid option: {choice} is out of range.")
            print("Invalid option. Please try again.")
            continue
        Logger.info(f"Processed choice: {choice}")
        if choice == 1:
            if not config["funds"]:
                config["funds"] = float(input("Enter total funds available for trading: "))
            if not config["broker"]:
                config["broker"] = {
                    "type": input("Enter broker type (TWS/ClientPortal): "),
                    "username": input("Enter broker username: "),
                    "password": input("Enter broker password: ")
                }
            ConfigManager.save(config)
            Logger.info("CLI wizard completed.")
            print("Trading system is already configured.")
        elif choice == 2:
            EmergencyStop().activate()
            print("EMERGENCY STOP activated.")
        elif choice == 3:
            EmergencyStop().deactivate()
            print("EMERGENCY STOP deactivated.")
        elif choice == 4:
            status = EmergencyStop().is_active()
            print(f"EMERGENCY STOP is {'ACTIVE' if status else 'INACTIVE'}.")
        elif choice == 5:
            break
        else:
            print("Invalid option. Please try again.")
