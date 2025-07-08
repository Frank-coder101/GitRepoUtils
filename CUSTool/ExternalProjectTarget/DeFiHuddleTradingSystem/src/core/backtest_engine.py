import backtrader as bt
import numpy as np
from src.core.logger import Logger
from src.core.strategy_loader import StrategyLoader
from src.core.scoring_module import ScoringModule

class BacktestEngine:
    def __init__(self, config):
        self.config = config
        self.scoring_module = ScoringModule(config)

    def run(self, data, scenarios=None):
        cerebro = bt.Cerebro()
        # Load strategy from config or use sample_strategy
        strategy_name = self.config.get('strategy', 'sample_strategy')
        strategy_class = StrategyLoader.load_strategy(strategy_name)
        if strategy_class:
            cerebro.addstrategy(strategy_class)
        else:
            Logger.error(f"Falling back to default SampleStrategy.")
            from src.strategies.sample_strategy import Strategy as SampleStrategy
            cerebro.addstrategy(SampleStrategy)

        cerebro.adddata(data)

        # Ensure analyzers are added correctly
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe_ratio')
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trade_analyzer')

        # Run backtest and ensure analyzers are accessible
        results = {}
        scenarios = scenarios or ['normal']
        for scenario in scenarios:
            Logger.info(f"Running backtest for scenario: {scenario}")
            result = cerebro.run()
            if not hasattr(result[0].analyzers, 'sharpe_ratio'):
                Logger.error("SharpeRatio analyzer not found in results.")
            results[scenario] = result

        # Log KPIs
        Logger.info("Logging session-level KPIs.")
        for scenario, result in results.items():
            sharpe_ratio = result[0].analyzers.sharpe_ratio.get_analysis() if hasattr(result[0].analyzers, 'sharpe_ratio') else None
            drawdown = result[0].analyzers.drawdown.get_analysis() if hasattr(result[0].analyzers, 'drawdown') else None
            trade_stats = result[0].analyzers.trade_analyzer.get_analysis() if hasattr(result[0].analyzers, 'trade_analyzer') else None

            total_return = (np.prod([1 + t.pnl for t in trade_stats.get('trades', [])]) - 1) * 100 if trade_stats and 'trades' in trade_stats else 0
            max_drawdown = drawdown.max.drawdown if drawdown else 0
            win_rate = (trade_stats.won.total / trade_stats.total.closed) if trade_stats and trade_stats.total.closed > 0 else 0

            Logger.info(f"Scenario: {scenario}, Total Return: {total_return:.2f}%, Max Drawdown: {max_drawdown:.2f}%, Win Rate: {win_rate:.2f}")

        Logger.info("Backtest complete.")
        return results
