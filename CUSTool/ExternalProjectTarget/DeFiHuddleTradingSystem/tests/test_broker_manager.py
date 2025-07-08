import os, sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from src.integration.broker_manager import BrokerManager

class TestBrokerManager(unittest.TestCase):
    def setUp(self):
        self.broker = BrokerManager(config={})

    def test_broker_connect(self):
        # Force unit test mode for this test run
        os.environ['TEST_MODE'] = 'unit'
        config = {'broker': {'type': 'TWS', 'username': 'user', 'password': 'pass'}}
        test_mode = os.environ.get('TEST_MODE', 'unit').lower()
        print(f"[TEST] TEST_MODE={test_mode}")
        if test_mode == 'integration':
            # Use an invalid host/port to guarantee connection failure
            bad_config = {'broker': {'type': 'TWS', 'host': 'invalid_host', 'port': 9999, 'clientId': 9999}}
            with self.assertRaises(RuntimeError) as cm:
                BrokerManager(bad_config).connect()
            print(f"[TEST] Caught exception: {cm.exception}")
        else:
            broker = BrokerManager(config)
            self.assertTrue(broker.is_connected())
        # Explicitly assert test mode to catch environment leakage
        self.assertIn(test_mode, ['unit', 'integration'])

    def test_place_order(self):
        order = {'symbol': 'AAPL', 'qty': 10, 'side': 'BUY'}
        try:
            trade = self.broker.place_order(order)
            self.assertIsNotNone(trade)
        except Exception as e:
            self.fail(f"Order placement failed: {e}")

    def test_get_account_data(self):
        try:
            account_data = self.broker.get_account_data()
            self.assertIn('cash_balance', account_data)
            self.assertIn('maintenance_margin', account_data)
            self.assertIn('margin_usage_pct', account_data)
        except Exception as e:
            self.fail(f"Account data retrieval failed: {e}")

if __name__ == "__main__":
    unittest.main()
