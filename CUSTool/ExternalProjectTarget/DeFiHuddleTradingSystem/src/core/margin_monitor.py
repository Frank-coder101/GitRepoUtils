import time
from src.integration.broker_manager import BrokerManager
from src.core.logger import Logger

class MarginMonitor:
    def __init__(self, broker_manager, config, logger=None):
        self.broker_manager = broker_manager
        self.config = config
        self.poll_interval = config.get('margin_poll_interval', 60)
        self.usage_threshold = config.get('margin_usage_threshold', 80)
        self.consecutive_error_limit = config.get('margin_error_limit', 3)
        self.error_count = 0
        self.logger = logger or Logger

    def poll(self):
        try:
            info = self.broker_manager.get_account_info()
            margin_usage = info['margin_usage_pct']
            self.logger.info(f"[MarginMonitor] Margin usage: {margin_usage:.2f}% (Threshold: {self.usage_threshold}%)")
            if margin_usage > self.usage_threshold:
                self.logger.error(f"E17001: Margin usage {margin_usage:.2f}% exceeds threshold {self.usage_threshold}%!")
                # TODO: Display persistent warning and halt new position entries
            self.error_count = 0
        except Exception as e:
            self.error_count += 1
            self.logger.error(f"E17002: Error polling margin info: {e} (Consecutive errors: {self.error_count})")
            if self.error_count >= self.consecutive_error_limit:
                self.logger.error("E17003: Broker API error/stale data for 3+ consecutive attempts. Notifying user and skipping cycle.")
                # TODO: Notify user and skip impacted cycle

    def run(self):
        while True:
            self.poll()
            time.sleep(self.poll_interval)
