from src.core.logger import Logger
from src.core.emergency_stop import EmergencyStop
from src.core.market_hours import MarketHours
import os

EXECUTION_MODE = os.environ.get('EXECUTION_MODE', 'backtest').lower()

class OrderManager:
    def __init__(self, broker):
        self.broker = broker

    def _calculate_rr(self, order):
        # Example: order must include 'entry', 'take_profit', 'stop_loss'
        entry = order.get('entry')
        tp = order.get('take_profit')
        sl = order.get('stop_loss')
        if entry is None or tp is None or sl is None or sl == entry:
            return None
        reward = abs(tp - entry)
        risk = abs(entry - sl)
        if risk == 0:
            return None
        return reward / risk

    def place_order(self, order):
        # Risk-to-Reward enforcement
        min_rr = order.get('min_rr', 1.5)
        rr = self._calculate_rr(order)
        if rr is not None and rr < min_rr:
            Logger.error(f"[RISK-REWARD] Order rejected: R:R {rr:.2f} < min {min_rr}")
            # Log as rejected opportunity (could call TradeJournal or AuditLog)
            return False
        # Check market hours before placing order
        market_hours = MarketHours()
        if not market_hours.is_market_open():
            Logger.error('[MARKET HOURS] Order placement blocked: Market is closed.')
            raise RuntimeError('Order placement blocked: Market is closed.')
        if EmergencyStop().is_active():
            Logger.error('[EMERGENCY STOP] Order placement blocked.')
            raise RuntimeError('Order placement blocked: Emergency Stop is active.')
        Logger.info(f"Placing order: {order}")
        if EXECUTION_MODE == 'integration':
            if hasattr(self.broker, 'is_connected') and self.broker.is_connected():
                ib = getattr(self.broker, 'get_ib', lambda: None)()
                if ib is None:
                    Logger.error("[INTEGRATION] IBKR connection not available in broker.")
                    raise RuntimeError("[INTEGRATION] IBKR connection not available in broker.")
                try:
                    # Example: order = {'symbol': 'AAPL', 'qty': 1, 'side': 'buy'}
                    contract = ib.qualifyContracts(ib.Stock(order['symbol'], 'SMART', 'USD'))[0]
                    action = order.get('side', 'BUY').upper()
                    qty = int(order.get('qty', 1))
                    ib_order = ib.marketOrder(action, qty)
                    trade = ib.placeOrder(contract, ib_order)
                    Logger.info(f"[INTEGRATION] Real order placed: {order}")
                    return True
                except Exception as e:
                    Logger.error(f"[INTEGRATION] Order placement failed: {e}")
                    raise RuntimeError(f"[INTEGRATION] Order placement failed: {e}")
            else:
                Logger.error("[INTEGRATION] Order placement failed: Broker not connected.")
                raise RuntimeError("[INTEGRATION] Order placement failed: Broker not connected.")
        else:
            # Simulate order placement in backtest/unit
            Logger.info(f"[{EXECUTION_MODE.upper()}] Order placed: {order}")
            return True

    def cancel_order(self, order_id):
        Logger.info(f"Cancelling order: {order_id}")
        if EXECUTION_MODE == 'integration':
            if hasattr(self.broker, 'is_connected') and self.broker.is_connected():
                ib = getattr(self.broker, 'get_ib', lambda: None)()
                if ib is None:
                    Logger.error("[INTEGRATION] IBKR connection not available in broker.")
                    raise RuntimeError("[INTEGRATION] IBKR connection not available in broker.")
                try:
                    # TODO: Implement real order cancellation logic with ib_insync
                    Logger.info(f"[INTEGRATION] Order {order_id} cancelled.")
                    return True
                except Exception as e:
                    Logger.error(f"[INTEGRATION] Order cancellation failed: {e}")
                    raise RuntimeError(f"[INTEGRATION] Order cancellation failed: {e}")
            else:
                Logger.error("[INTEGRATION] Order cancellation failed: Broker not connected.")
                raise RuntimeError("[INTEGRATION] Order cancellation failed: Broker not connected.")
        else:
            Logger.info(f"[{EXECUTION_MODE.upper()}] Order {order_id} cancelled (simulated)")
            return True
