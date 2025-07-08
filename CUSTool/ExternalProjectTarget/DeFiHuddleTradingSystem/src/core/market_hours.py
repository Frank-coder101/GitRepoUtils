import datetime
import pytz
import holidays
from src.core.logger import Logger

class MarketHours:
    def __init__(self, exchange_tz='America/New_York', premarket_enabled=False, afterhours_enabled=False):
        self.exchange_tz = pytz.timezone(exchange_tz)
        self.premarket_enabled = premarket_enabled
        self.afterhours_enabled = afterhours_enabled
        self.holidays = holidays.US()

    def is_market_open(self, dt=None):
        dt = dt or datetime.datetime.now(self.exchange_tz)
        if dt.date() in self.holidays:
            Logger.info(f"Market closed for holiday: {dt.date()}")
            return False
        # NYSE regular hours: 9:30am to 4:00pm
        open_time = dt.replace(hour=9, minute=30, second=0, microsecond=0)
        close_time = dt.replace(hour=16, minute=0, second=0, microsecond=0)
        if self.premarket_enabled and dt < open_time:
            return True
        if self.afterhours_enabled and dt > close_time:
            return True
        return open_time <= dt <= close_time

    def adjust_for_early_close(self, dt=None):
        # Example: Early close at 1:00pm on certain holidays
        dt = dt or datetime.datetime.now(self.exchange_tz)
        early_close_days = {datetime.date(2025, 7, 3)}  # Example: July 3, 2025
        if dt.date() in early_close_days:
            return dt.replace(hour=13, minute=0, second=0, microsecond=0)
        return dt.replace(hour=16, minute=0, second=0, microsecond=0)
