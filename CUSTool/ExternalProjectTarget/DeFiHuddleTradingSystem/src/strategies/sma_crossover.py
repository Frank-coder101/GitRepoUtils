import backtrader as bt

class Strategy(bt.Strategy):
    params = dict(fast=10, slow=30)
    def __init__(self):
        self.sma_fast = bt.ind.SMA(period=self.p.fast)
        self.sma_slow = bt.ind.SMA(period=self.p.slow)
    def next(self):
        if not self.position and self.sma_fast > self.sma_slow:
            self.buy(size=1)
        elif self.position and self.sma_fast < self.sma_slow:
            self.sell(size=1)
