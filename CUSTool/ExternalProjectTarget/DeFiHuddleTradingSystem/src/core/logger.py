import logging
import os
from logging.handlers import RotatingFileHandler

LOG_PATH = os.path.join(os.getcwd(), "defihuddle_test.log")
LOG_MAX_BYTES = 5 * 1024 * 1024  # 5 MB
LOG_BACKUP_COUNT = 3

class Logger:
    @staticmethod
    def init():
        # Remove all handlers associated with the root logger object.
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        try:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            handler.setFormatter(formatter)
            logging.basicConfig(
                level=logging.INFO,
                handlers=[handler]
            )
        except Exception as e:
            print(f"Logger initialization failed: {e}")

    @staticmethod
    def info(msg):
        logging.info(msg)
        logging.getLogger().handlers[0].flush()

    @staticmethod
    def error(msg):
        logging.error(msg)
        logging.getLogger().handlers[0].flush()

    @staticmethod
    def warning(msg):
        logging.warning(msg)
        logging.getLogger().handlers[0].flush()
