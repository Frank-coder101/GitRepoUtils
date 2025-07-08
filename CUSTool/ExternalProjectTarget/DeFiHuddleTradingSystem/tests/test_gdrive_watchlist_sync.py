import os
os.environ['TEST_MODE'] = 'integration'
import sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from src.integration.gdrive_watchlist_sync import GDriveWatchlistSync

class TestGDriveWatchlistSync(unittest.TestCase):
    def test_sync_integration(self):
        config = {}  # No credentials
        sync = GDriveWatchlistSync(config)
        with self.assertRaises(RuntimeError):
            sync.sync(['AAPL', 'GOOG'])

if __name__ == "__main__":
    unittest.main()
