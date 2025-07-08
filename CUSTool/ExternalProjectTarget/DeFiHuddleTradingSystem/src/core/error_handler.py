from src.core.logger import Logger

class ErrorHandler:
    @staticmethod
    def handle_error(error, context=""):
        Logger.error(f"Error in {context}: {error}")
        print(f"An error occurred: {error}\nContext: {context}\nPlease check the logs for more details.")
