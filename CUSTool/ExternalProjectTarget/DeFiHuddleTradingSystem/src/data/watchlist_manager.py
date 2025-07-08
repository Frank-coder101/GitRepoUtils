import os
import json
from src.core.logger import Logger
from src.integration.gdrive_watchlist_sync import GDriveWatchlistSync

WATCHLIST_PATH = os.path.expanduser("~/.defihuddle_watchlist.json")

class WatchlistManager:
    @staticmethod
    def load():
        if os.path.exists(WATCHLIST_PATH):
            with open(WATCHLIST_PATH, 'r') as f:
                return json.load(f)
        return []

    @staticmethod
    def save(watchlist):
        with open(WATCHLIST_PATH, 'w') as f:
            json.dump(watchlist, f, indent=4)
        Logger.info("Watchlist saved.")
        # Sync with Google Drive (stub)
        config = {}
        GDriveWatchlistSync(config).sync(watchlist)

    @staticmethod
    def review_and_flag_symbols(volume_threshold=10000, price_days=5, broker_error_symbols=None):
        """
        Review symbols for low volume, zero price movement, or broker errors. Flag and disable as needed.
        """
        watchlist = WatchlistManager.load()
        flagged = []
        for symbol in watchlist:
            # Assume symbol is a dict with keys: symbol, avg_volume, price_history, status
            if symbol.get('status') == 'disabled':
                continue
            if symbol.get('avg_volume', 0) < volume_threshold:
                symbol['status'] = 'disabled'
                symbol['flag_reason'] = 'low_volume'
                flagged.append(symbol['symbol'])
            elif all(p == symbol['price_history'][-1] for p in symbol.get('price_history', [])[-price_days:]):
                symbol['status'] = 'disabled'
                symbol['flag_reason'] = 'zero_movement'
                flagged.append(symbol['symbol'])
            elif broker_error_symbols and symbol['symbol'] in broker_error_symbols:
                symbol['status'] = 'disabled'
                symbol['flag_reason'] = 'broker_error'
                flagged.append(symbol['symbol'])
        WatchlistManager.save(watchlist)
        Logger.info(f"Flagged symbols: {flagged}")
        return flagged

    @staticmethod
    def reactivate_symbol(symbol_name):
        watchlist = WatchlistManager.load()
        for symbol in watchlist:
            if symbol['symbol'] == symbol_name and symbol.get('status') == 'disabled':
                symbol['status'] = 'active'
                symbol.pop('flag_reason', None)
                Logger.info(f"Symbol {symbol_name} reactivated.")
        WatchlistManager.save(watchlist)
