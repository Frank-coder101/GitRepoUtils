import backtrader as bt

class Strategy(bt.Strategy):
    params = dict(rsi_period=14, overbought=70, oversold=30)
    def __init__(self):
        self.rsi = bt.ind.RSI(period=self.p.rsi_period)
    def next(self):
        if not self.position and self.rsi < self.p.oversold:
            self.buy(size=1)
        elif self.position and self.rsi > self.p.overbought:
            self.sell(size=1)
