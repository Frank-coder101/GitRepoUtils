import backtrader as bt

class Strategy(bt.Strategy):
    params = dict(param1=1)
    def __init__(self):
        pass
    def next(self):
        if not self.position:
            self.buy(size=1)
        elif len(self) > 3:
            self.sell(size=1)
