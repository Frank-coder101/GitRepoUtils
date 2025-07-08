import os, sys
# Ensure both project root and src are on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import bootstrap
import unittest
from src.core.backtest_engine import BacktestEngine
import backtrader as bt
import pandas as pd
from datetime import datetime, timedelta

class DummyData(bt.feeds.PandasData):
    pass

class TestBacktestEngine(unittest.TestCase):
    def test_run(self):
        # Create a DataFrame with a datetime index
        dates = pd.date_range(datetime.now(), periods=5)
        df = pd.DataFrame({
            'open': [1,2,3,4,5],
            'high': [1,2,3,4,5],
            'low': [1,2,3,4,5],
            'close': [1,2,3,4,5],
            'volume': [100,100,100,100,100],
            'openinterest': [0,0,0,0,0]
        }, index=dates)
        data = DummyData(dataname=df)
        engine = BacktestEngine({})
        result = engine.run(data)
        self.assertIsNotNone(result)

    def test_run_with_scenarios(self):
        # Create a DataFrame with a datetime index
        dates = pd.date_range(datetime.now(), periods=5)
        df = pd.DataFrame({
            'open': [1,2,3,4,5],
            'high': [1,2,3,4,5],
            'low': [1,2,3,4,5],
            'close': [1,2,3,4,5],
            'volume': [100,100,100,100,100],
            'openinterest': [0,0,0,0,0]
        }, index=dates)
        data = DummyData(dataname=df)
        engine = BacktestEngine({})
        scenarios = ['normal', 'market_crash']
        results = engine.run(data, scenarios=scenarios)
        self.assertIn('normal', results)
        self.assertIn('market_crash', results)
        self.assertIsNotNone(results['normal'])
        self.assertIsNotNone(results['market_crash'])

    def test_kpi_logging(self):
        dates = pd.date_range(datetime.now(), periods=5)
        df = pd.DataFrame({
            'open': [1,2,3,4,5],
            'high': [1,2,3,4,5],
            'low': [1,2,3,4,5],
            'close': [1,2,3,4,5],
            'volume': [100,100,100,100,100],
            'openinterest': [0,0,0,0,0]
        }, index=dates)
        data = DummyData(dataname=df)
        engine = BacktestEngine({})
        results = engine.run(data)

        for scenario, result in results.items():
            self.assertIn('sharpe_ratio', result[0].analyzers)
            self.assertIn('drawdown', result[0].analyzers)
            self.assertIn('trade_analyzer', result[0].analyzers)

    def test_regime_transitions(self):
        dates = pd.date_range(datetime.now(), periods=5)
        df = pd.DataFrame({
            'open': [1,2,3,4,5],
            'high': [1,2,3,4,5],
            'low': [1,2,3,4,5],
            'close': [1,2,3,4,5],
            'volume': [100,100,100,100,100],
            'openinterest': [0,0,0,0,0]
        }, index=dates)
        data = DummyData(dataname=df)
        engine = BacktestEngine({})
        scenarios = ['normal', 'market_crash']
        results = engine.run(data, scenarios=scenarios)

        self.assertIn('normal', results)
        self.assertIn('market_crash', results)
        self.assertIsNotNone(results['normal'])
        self.assertIsNotNone(results['market_crash'])

if __name__ == "__main__":
    unittest.main()
