import backtrader as bt

class Strategy(bt.Strategy):
    params = dict(fast=12, slow=26, signal=9)
    def __init__(self):
        self.macd = bt.ind.MACD(period_me1=self.p.fast, period_me2=self.p.slow, period_signal=self.p.signal)
    def next(self):
        if not self.position and self.macd.macd > self.macd.signal:
            self.buy(size=1)
        elif self.position and self.macd.macd < self.macd.signal:
            self.sell(size=1)
