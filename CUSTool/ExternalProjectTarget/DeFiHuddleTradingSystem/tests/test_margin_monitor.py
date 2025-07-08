import pytest
from src.core.margin_monitor import MarginMonitor

class DummyBrokerManager:
    def __init__(self, info):
        self.info = info
    def get_account_info(self):
        return self.info

class DummyLogger:
    logs = []
    @staticmethod
    def info(msg):
        DummyLogger.logs.append(('info', msg))
    @staticmethod
    def error(msg):
        DummyLogger.logs.append(('error', msg))

@pytest.fixture(autouse=True)
def patch_logger(monkeypatch):
    import src.core.logger
    monkeypatch.setattr(src.core.logger, 'Logger', DummyLogger)
    DummyLogger.logs.clear()
    yield
    DummyLogger.logs.clear()

def test_margin_monitor_normal():
    broker = DummyBrokerManager({'margin_usage_pct': 50.0, 'cash_balance': 100000, 'maintenance_margin': 20000})
    config = {'margin_poll_interval': 1, 'margin_usage_threshold': 80, 'margin_error_limit': 3}
    monitor = MarginMonitor(broker, config, logger=DummyLogger)
    monitor.poll()
    assert any('Margin usage' in msg for level, msg in DummyLogger.logs if level == 'info')
    assert not any('exceeds threshold' in msg for level, msg in DummyLogger.logs if level == 'error')

def test_margin_monitor_exceeds_threshold():
    broker = DummyBrokerManager({'margin_usage_pct': 85.0, 'cash_balance': 100000, 'maintenance_margin': 20000})
    config = {'margin_poll_interval': 1, 'margin_usage_threshold': 80, 'margin_error_limit': 3}
    monitor = MarginMonitor(broker, config, logger=DummyLogger)
    monitor.poll()
    assert any('exceeds threshold' in msg for level, msg in DummyLogger.logs if level == 'error')

def test_margin_monitor_error_limit():
    class FailingBroker:
        def get_account_info(self):
            raise Exception('fail')
    broker = FailingBroker()
    config = {'margin_poll_interval': 1, 'margin_usage_threshold': 80, 'margin_error_limit': 2}
    monitor = MarginMonitor(broker, config, logger=DummyLogger)
    monitor.poll()
    monitor.poll()
    assert any('Consecutive errors: 2' in msg for level, msg in DummyLogger.logs if level == 'error')
    monitor.poll()
    assert any('E17003' in msg for level, msg in DummyLogger.logs if level == 'error')
