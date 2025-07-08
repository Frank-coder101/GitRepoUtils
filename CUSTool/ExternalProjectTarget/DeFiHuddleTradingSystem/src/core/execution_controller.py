from src.core.logger import Logger
from src.core.error_handler import ErrorHandler
from src.integration.broker_manager import BrokerManager
from src.core.order_manager import OrderManager
from src.core.backtest_engine import BacktestEngine
from src.ai.optimizer import AIOptimizer
from src.core.persistence import Persistence
from src.core.emergency_stop import EmergencyStop
import backtrader as bt
import os

EXECUTION_MODE = os.environ.get('EXECUTION_MODE', 'backtest').lower()

class ExecutionController:
    def __init__(self, config, broker):
        self.config = config
        self.broker = broker
        self.order_manager = OrderManager(broker)
        self.ai_optimizer = AIOptimizer(config)
        Persistence.init_db()

    def run(self):
        if not self.broker.check_capabilities():
            Logger.error("[CAPABILITY] Required broker capabilities missing. Execution aborted.")
            return
        if EmergencyStop().is_active():
            Logger.error('[EMERGENCY STOP] All execution cycles halted. Trading is disabled.')
            return
        mode = self.config.get("mode", EXECUTION_MODE)
        Logger.info(f"Starting execution in mode: {mode}")
        try:
            if mode == "backtest":
                self.run_backtest()
            elif mode == "live":
                self.run_live()
            else:
                Logger.error(f"Unknown mode: {mode}")
        except Exception as e:
            ErrorHandler.handle_error(e, context=f"ExecutionController.run (mode={mode})")

    def run_backtest(self):
        Logger.info("Running backtest with Backtrader")
        try:
            data = bt.feeds.YahooFinanceData(dataname='AAPL', fromdate=None, todate=None)
            engine = BacktestEngine(self.config)
            params = {"param1": 1}
            optimized_params = self.ai_optimizer.optimize(params)
            result = engine.run(data)
            Persistence.save_backtest_result(self.config.get('strategy', 'sample_strategy'), result)
        except Exception as e:
            ErrorHandler.handle_error(e, context="ExecutionController.run_backtest")

    def run_live(self):
        if not self.broker.is_connected():
            Logger.error("Broker not connected!")
            return
        Logger.info("Running live trading")
        try:
            order = {"symbol": "AAPL", "qty": 1, "side": "buy"}
            self.order_manager.place_order(order)
        except Exception as e:
            ErrorHandler.handle_error(e, context="ExecutionController.run_live")
