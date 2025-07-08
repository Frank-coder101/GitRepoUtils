import os, sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from src.core.order_manager import OrderManager

class DummyBroker:
    def is_connected(self):
        return False

class TestOrderManager(unittest.TestCase):
    def test_place_and_cancel_order(self):
        broker = DummyBroker()
        manager = OrderManager(broker)
        if os.environ.get('TEST_MODE', 'unit').lower() == 'integration':
            with self.assertRaises(RuntimeError):
                manager.place_order({'symbol': 'AAPL', 'qty': 10})
            with self.assertRaises(RuntimeError):
                manager.cancel_order('order123')
        else:
            self.assertFalse(manager.place_order({'symbol': 'AAPL', 'qty': 10}))
            self.assertTrue(manager.cancel_order('order123'))

if __name__ == "__main__":
    unittest.main()
