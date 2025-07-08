import backtrader as bt

class Strategy(bt.Strategy):
    params = dict(period=20, devfactor=2)
    def __init__(self):
        self.bbands = bt.ind.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
    def next(self):
        if not self.position and self.data.close < self.bbands.bot:
            self.buy(size=1)
        elif self.position and self.data.close > self.bbands.top:
            self.sell(size=1)
