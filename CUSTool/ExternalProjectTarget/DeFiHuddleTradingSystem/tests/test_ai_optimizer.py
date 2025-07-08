import os, sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from src.ai.optimizer import AIOptimizer

class TestAIOptimizer(unittest.TestCase):
    def test_optimize(self):
        config = {}
        optimizer = AIOptimizer(config)
        params = {'param1': 1}
        result = optimizer.optimize(params)
        self.assertEqual(result, params)

if __name__ == "__main__":
    unittest.main()
