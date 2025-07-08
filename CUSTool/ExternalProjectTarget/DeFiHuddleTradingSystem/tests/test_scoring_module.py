import unittest
import pandas as pd
from src.core.scoring_module import ScoringModule

class TestScoringModule(unittest.TestCase):
    def setUp(self):
        self.config = {
            'weights': {
                'sma_crossover': 0.5,
                'rsi_divergence': 0.5
            }
        }
        self.scoring_module = ScoringModule(self.config)

    def test_calculate_score(self):
        # Create a dummy dataset
        data = pd.DataFrame({
            'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        })
        score = self.scoring_module.calculate_score(data)
        self.assertIsInstance(score, (int, float))

    def test_bollinger_bands(self):
        # Create a dummy dataset
        data = pd.DataFrame({
            'close': [100, 102, 104, 103, 101, 99, 98, 97, 96, 95, 94, 93, 92, 91, 90, 89, 88, 87, 86, 85]
        })
        self.config['weights'] = {'bollinger_bands': 1.0}
        self.scoring_module = ScoringModule(self.config)
        score = self.scoring_module.calculate_score(data)
        self.assertIsInstance(score, (int, float))

    def test_macd(self):
        # Create a dummy dataset
        data = pd.DataFrame({
            'close': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        })
        self.config['weights'] = {'macd': 1.0}
        self.scoring_module = ScoringModule(self.config)
        score = self.scoring_module.calculate_score(data)
        self.assertIsInstance(score, (int, float))

    def test_fibonacci_retracement(self):
        # Create a dummy dataset
        data = pd.DataFrame({
            'close': [100, 105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195]
        })
        self.config['weights'] = {'fibonacci_retracement': 1.0}
        self.scoring_module = ScoringModule(self.config)
        score = self.scoring_module.calculate_score(data)
        self.assertIsInstance(score, (int, float))

if __name__ == "__main__":
    unittest.main()
