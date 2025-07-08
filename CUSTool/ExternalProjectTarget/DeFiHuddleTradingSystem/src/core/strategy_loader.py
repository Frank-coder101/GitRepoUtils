import importlib
from src.core.logger import Logger

class StrategyLoader:
    @staticmethod
    def load_strategy(strategy_name):
        try:
            module = importlib.import_module(f"src.strategies.{strategy_name}")
            strategy_class = getattr(module, "Strategy")
            Logger.info(f"Loaded strategy: {strategy_name}")
            return strategy_class
        except Exception as e:
            Logger.error(f"Failed to load strategy {strategy_name}: {e}")
            return None
