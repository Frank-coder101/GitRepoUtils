import os, sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from src.core.persistence import Persistence
import os

class TestPersistence(unittest.TestCase):
    def test_init_db_and_connection(self):
        Persistence.init_db()
        conn = Persistence.get_connection()
        self.assertIsNotNone(conn)
        conn.close()
        self.assertTrue(os.path.exists(os.path.expanduser("~/.defihuddle_trading.db")))

if __name__ == "__main__":
    unittest.main()
