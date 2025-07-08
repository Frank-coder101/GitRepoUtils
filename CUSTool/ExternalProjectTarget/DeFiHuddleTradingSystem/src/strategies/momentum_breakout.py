import backtrader as bt

class Strategy(bt.Strategy):
    params = dict(momentum_period=10, threshold=0.05)
    def __init__(self):
        self.momentum = bt.ind.Momentum(period=self.p.momentum_period)
    def next(self):
        if not self.position and self.momentum[0] > self.p.threshold:
            self.buy(size=1)
        elif self.position and self.momentum[0] < -self.p.threshold:
            self.sell(size=1)
