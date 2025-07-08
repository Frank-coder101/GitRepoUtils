import os
import json
from src.core.logger import Logger

CONFIG_PATH = os.path.expanduser("~/.defihuddle_config.json")

class ConfigManager:
    @staticmethod
    def load_or_create():
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config = json.load(f)
            Logger.info("Loaded configuration.")
            return config
        else:
            config = ConfigManager.default_config()
            ConfigManager.save(config)
            Logger.info("Created default configuration.")
            return config

    @staticmethod
    def save(config):
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=4)
        Logger.info("Configuration saved.")

    @staticmethod
    def default_config():
        return {
            "funds": 0.0,
            "broker": {},
            "mode": "BackTesting",
            "watchlist": [],
            "risk": {},
            "ai_optimizer": {},
            "logging": {}
        }
