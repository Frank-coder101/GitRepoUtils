import os, sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from src.core.risk_engine import RiskEngine

class TestRiskEngine(unittest.TestCase):
    def test_check_risk(self):
        config = {}
        engine = RiskEngine(config)
        if os.environ.get('TEST_MODE', 'unit').lower() == 'integration':
            with self.assertRaises(NotImplementedError):
                engine.check_risk({'symbol': 'AAPL', 'qty': 10})
        else:
            result = engine.check_risk({'symbol': 'AAPL', 'qty': 10})
            self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
