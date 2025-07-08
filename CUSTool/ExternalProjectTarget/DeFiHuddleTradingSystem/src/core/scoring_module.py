import numpy as np

class ScoringModule:
    def __init__(self, config):
        self.config = config

    def calculate_score(self, data):
        """
        Calculate the score for the given data based on configured analysis methods.
        """
        score = 0
        weights = self.config.get('weights', {})

        # Example: SMA crossover analysis
        if 'sma_crossover' in weights:
            score += self._sma_crossover(data) * weights['sma_crossover']

        # Example: RSI divergence analysis
        if 'rsi_divergence' in weights:
            score += self._rsi_divergence(data) * weights['rsi_divergence']

        if 'bollinger_bands' in weights:
            score += self._bollinger_bands(data) * weights['bollinger_bands']

        if 'macd' in weights:
            score += self._macd(data) * weights['macd']

        if 'fibonacci_retracement' in weights:
            score += self._fibonacci_retracement(data) * weights['fibonacci_retracement']

        return score

    def _sma_crossover(self, data):
        """Calculate SMA crossover score."""
        sma_short = data['close'].rolling(window=5).mean()
        sma_long = data['close'].rolling(window=20).mean()
        crossover = (sma_short > sma_long).astype(int).diff().fillna(0)
        return crossover.sum()

    def _rsi_divergence(self, data):
        """Calculate RSI divergence score."""
        delta = data['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        divergence = (rsi > 70).astype(int).sum() - (rsi < 30).astype(int).sum()
        return divergence

    def _bollinger_bands(self, data):
        """Calculate Bollinger Bands score."""
        sma = data['close'].rolling(window=20).mean()
        std_dev = data['close'].rolling(window=20).std()
        upper_band = sma + (2 * std_dev)
        lower_band = sma - (2 * std_dev)
        breaches = ((data['close'] > upper_band) | (data['close'] < lower_band)).astype(int).sum()
        return breaches

    def _macd(self, data):
        """Calculate MACD score."""
        ema_12 = data['close'].ewm(span=12, adjust=False).mean()
        ema_26 = data['close'].ewm(span=26, adjust=False).mean()
        macd = ema_12 - ema_26
        signal = macd.ewm(span=9, adjust=False).mean()
        crossovers = ((macd > signal).astype(int).diff().fillna(0)).sum()
        return crossovers

    def _fibonacci_retracement(self, data):
        """Calculate Fibonacci retracement score."""
        high = data['close'].max()
        low = data['close'].min()
        levels = [0.236, 0.382, 0.5, 0.618, 0.786]
        retracements = [(high - (level * (high - low))) for level in levels]
        breaches = sum((data['close'] < level).sum() for level in retracements)
        return breaches
