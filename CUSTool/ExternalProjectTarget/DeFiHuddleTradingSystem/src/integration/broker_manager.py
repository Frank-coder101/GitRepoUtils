# Assumption (2025-07-04): Using ib_insync for TWS/Client Portal integration. Credentials are username/password for simplicity. OAuth and advanced flows can be added later.
from src.core.logger import Logger
import os
import time

TEST_MODE = os.environ.get('TEST_MODE', 'unit').lower()
EXECUTION_MODE = os.environ.get('EXECUTION_MODE', 'backtest').lower()

if TEST_MODE == 'integration':
    try:
        from ib_insync import IB, Stock, util
    except ImportError:
        IB = None
        Logger.error('ib_insync is not installed. Integration mode will not work.')
else:
    IB = None

class BrokerManager:
    def __init__(self, config):
        self.config = config
        self.connected = False
        self.ib = None
        self.connect()

    def connect(self):
        # Validate IBKR environment variables for live and integration modes
        if EXECUTION_MODE in ['live', 'integration']:
            required_env_vars = ['IBKR_HOST', 'IBKR_PORT', 'IBKR_CLIENT_ID']
            for var in required_env_vars:
                if not os.environ.get(var):
                    raise EnvironmentError(f"Environment variable {var} is required for {EXECUTION_MODE} mode but not set.")

        if EXECUTION_MODE == 'integration':
            if IB is None:
                Logger.error('ib_insync is not available. Cannot connect to IBKR.')
                self.connected = False
                raise RuntimeError('ib_insync is not available. Cannot connect to IBKR.')
            self.ib = IB()
            try:
                host = os.environ.get('IBKR_HOST', self.config['broker'].get('host', '127.0.0.1'))
                port = int(os.environ.get('IBKR_PORT', self.config['broker'].get('port', 7497)))
                clientId = int(os.environ.get('IBKR_CLIENT_ID', self.config['broker'].get('clientId', 1)))
                Logger.info(f"[INTEGRATION] Connecting to IBKR at {host}:{port} (clientId={clientId})")
                self.ib.connect(host, port, clientId=clientId)
                self.connected = self.ib.isConnected()
                if not self.connected:
                    Logger.error('Failed to connect to IBKR. Is TWS or IB Gateway running?')
                    raise RuntimeError('Failed to connect to IBKR. Is TWS or IB Gateway running?')
            except Exception as e:
                Logger.error(f'Exception during IBKR connection: {e}')
                self.connected = False
                raise RuntimeError(f'Exception during IBKR connection: {e}')
        elif EXECUTION_MODE == 'live':
            # ...live connection logic if needed...
            pass
        else:
            Logger.info(f"[{EXECUTION_MODE.upper()}] Simulated broker connection: {self.config['broker']}")
            self.connected = True

    def is_connected(self):
        return self.connected

    def get_ib(self):
        return self.ib

    def get_account_info(self):
        """
        Retrieve account info including cash balance, maintenance margin, and margin usage percentage.
        Returns a dict with keys: 'cash_balance', 'maintenance_margin', 'margin_usage_pct'.
        """
        if TEST_MODE == 'integration' and self.ib is not None:
            account_values = {v.tag: v.value for v in self.ib.accountValues()}
            try:
                cash_balance = float(account_values.get('TotalCashValue', 0))
                maintenance_margin = float(account_values.get('MaintMarginReq', 0))
                margin_usage_pct = float(account_values.get('MarginRatio', 0)) * 100
            except Exception as e:
                Logger.error(f"Error parsing account info: {e}")
                cash_balance = maintenance_margin = margin_usage_pct = 0
            return {
                'cash_balance': cash_balance,
                'maintenance_margin': maintenance_margin,
                'margin_usage_pct': margin_usage_pct
            }
        else:
            # Simulated values for unit test mode
            return {
                'cash_balance': 100000.0,
                'maintenance_margin': 20000.0,
                'margin_usage_pct': 50.0
            }

    def place_order(self, order):
        if not self.is_connected():
            raise RuntimeError("Broker not connected")
        try:
            contract = self.ib.qualifyContracts(self.ib.Stock(order['symbol'], 'SMART', 'USD'))[0]
            action = order.get('side', 'BUY').upper()
            qty = int(order.get('qty', 1))
            ib_order = self.ib.marketOrder(action, qty)
            trade = self.ib.placeOrder(contract, ib_order)
            Logger.info(f"Order placed: {order}")
            return trade
        except Exception as e:
            Logger.error(f"Order placement failed: {e}")
            raise

    def get_account_data(self):
        if not self.is_connected():
            raise RuntimeError("Broker not connected")
        try:
            account_values = {v.tag: v.value for v in self.ib.accountValues()}
            return {
                'cash_balance': float(account_values.get('TotalCashValue', 0)),
                'maintenance_margin': float(account_values.get('MaintMarginReq', 0)),
                'margin_usage_pct': float(account_values.get('MarginRatio', 0)) * 100
            }
        except Exception as e:
            Logger.error(f"Failed to retrieve account data: {e}")
            raise

    def retry_api_call(self, func, *args, **kwargs):
        max_retries = 3
        delay = 1
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                Logger.error(f"API call failed (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(delay)
                delay *= 2

    def check_capabilities(self):
        """
        Check broker account for required capabilities: order types, limits, permissions.
        Warn user if any required capability is missing.
        """
        required_order_types = {'market', 'limit', 'bracket', 'trailing_stop'}
        required_permissions = {'real_time_data'}
        missing = []
        if TEST_MODE == 'integration' and self.ib is not None:
            # Example: check order types and permissions (stub logic)
            supported_order_types = {'market', 'limit', 'bracket'}  # TODO: Query from API
            if not required_order_types.issubset(supported_order_types):
                missing.append('order_types')
            max_orders = 100  # TODO: Query from API
            if max_orders < 10:
                missing.append('max_orders')
            permissions = {'real_time_data'}  # TODO: Query from API
            if not required_permissions.issubset(permissions):
                missing.append('permissions')
        else:
            # Simulate all capabilities present in unit test mode
            missing = []
        if missing:
            Logger.error(f"[CAPABILITY] Missing broker capabilities: {missing}. Trading cycles will not start.")
            return False
        Logger.info("[CAPABILITY] All required broker capabilities present.")
        return True
