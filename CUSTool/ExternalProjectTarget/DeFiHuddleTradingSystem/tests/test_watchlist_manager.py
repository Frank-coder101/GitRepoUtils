import os
import sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from src.data.watchlist_manager import WatchlistManager
import json
import pytest
from src.data.watchlist_manager import WatchlistManager, WATCHLIST_PATH

@pytest.fixture(autouse=True)
def cleanup():
    if os.path.exists(WATCHLIST_PATH):
        os.remove(WATCHLIST_PATH)
    yield
    if os.path.exists(WATCHLIST_PATH):
        os.remove(WATCHLIST_PATH)

class TestWatchlistManager(unittest.TestCase):
    def test_load_and_save(self):
        test_watchlist = ['AAPL', 'GOOG']
        WatchlistManager.save(test_watchlist)
        loaded = WatchlistManager.load()
        self.assertEqual(loaded, test_watchlist)
        os.remove(os.path.expanduser("~/.defihuddle_watchlist.json"))

    def test_review_and_flag_symbols_low_volume(self):
        watchlist = [
            {'symbol': 'AAA', 'avg_volume': 9000, 'price_history': [1,2,3,4,5], 'status': 'active'},
            {'symbol': 'BBB', 'avg_volume': 20000, 'price_history': [1,1,1,1,1], 'status': 'active'},
            {'symbol': 'CCC', 'avg_volume': 15000, 'price_history': [1,2,3,4,5], 'status': 'active'},
        ]
        with open(WATCHLIST_PATH, 'w') as f:
            json.dump(watchlist, f)
        flagged = WatchlistManager.review_and_flag_symbols(volume_threshold=10000)
        assert 'AAA' in flagged
        loaded = WatchlistManager.load()
        assert any(s['symbol'] == 'AAA' and s['status'] == 'disabled' for s in loaded)

    def test_review_and_flag_symbols_zero_movement(self):
        watchlist = [
            {'symbol': 'ZZZ', 'avg_volume': 20000, 'price_history': [2,2,2,2,2], 'status': 'active'},
        ]
        with open(WATCHLIST_PATH, 'w') as f:
            json.dump(watchlist, f)
        flagged = WatchlistManager.review_and_flag_symbols(price_days=5)
        assert 'ZZZ' in flagged
        loaded = WatchlistManager.load()
        assert any(s['symbol'] == 'ZZZ' and s['status'] == 'disabled' for s in loaded)

    def test_review_and_flag_symbols_broker_error(self):
        watchlist = [
            {'symbol': 'ERR', 'avg_volume': 20000, 'price_history': [1,2,3,4,5], 'status': 'active'},
        ]
        with open(WATCHLIST_PATH, 'w') as f:
            json.dump(watchlist, f)
        flagged = WatchlistManager.review_and_flag_symbols(broker_error_symbols=['ERR'])
        assert 'ERR' in flagged
        loaded = WatchlistManager.load()
        assert any(s['symbol'] == 'ERR' and s['status'] == 'disabled' for s in loaded)

    def test_reactivate_symbol(self):
        watchlist = [
            {'symbol': 'AAA', 'avg_volume': 9000, 'price_history': [1,2,3,4,5], 'status': 'disabled', 'flag_reason': 'low_volume'},
        ]
        with open(WATCHLIST_PATH, 'w') as f:
            json.dump(watchlist, f)
        WatchlistManager.reactivate_symbol('AAA')
        loaded = WatchlistManager.load()
        assert any(s['symbol'] == 'AAA' and s['status'] == 'active' for s in loaded)

if __name__ == "__main__":
    unittest.main()
