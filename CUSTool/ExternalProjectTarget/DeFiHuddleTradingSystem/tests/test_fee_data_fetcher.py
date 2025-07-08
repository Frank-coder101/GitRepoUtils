import pytest
from src.data.fee_data_fetcher import FEEDataFetcher

class DummyLogger:
    @staticmethod
    def info(msg):
        print(msg)
    @staticmethod
    def error(msg):
        print(msg)

def test_fee_data_fetcher_success(monkeypatch):
    # Patch requests.get to return a dummy response
    class DummyResponse:
        def raise_for_status(self): pass
        def json(self): return {'fee': 1.23}
        @property
        def headers(self): return {'Date': '2025-07-05T00:00:00Z'}
    monkeypatch.setattr('requests.get', lambda url: DummyResponse())
    fetcher = FEEDataFetcher({'broker_fee_url': 'http://dummy-url'})
    data = fetcher.fetch_fees()
    assert 'broker' in data
    assert data['broker']['data']['fee'] == 1.23

def test_fee_data_fetcher_failure(monkeypatch):
    class DummyResponse:
        def raise_for_status(self): raise Exception('fail')
    monkeypatch.setattr('requests.get', lambda url: DummyResponse())
    fetcher = FEEDataFetcher({'broker_fee_url': 'http://dummy-url'})
    with pytest.raises(Exception):
        fetcher.fetch_fees()

def test_fee_data_fetcher_malformed_json(monkeypatch):
    class DummyResponse:
        def raise_for_status(self): pass
        def json(self): raise ValueError('Malformed JSON')
        @property
        def headers(self): return {'Date': '2025-07-05T00:00:00Z'}
    monkeypatch.setattr('requests.get', lambda url: DummyResponse())
    fetcher = FEEDataFetcher({'broker_fee_url': 'http://dummy-url'})
    with pytest.raises(ValueError):
        fetcher.fetch_fees()

def test_fee_data_fetcher_missing_key(monkeypatch):
    class DummyResponse:
        def raise_for_status(self): pass
        def json(self): return {'not_fee': 0}
        @property
        def headers(self): return {'Date': '2025-07-05T00:00:00Z'}
    monkeypatch.setattr('requests.get', lambda url: DummyResponse())
    fetcher = FEEDataFetcher({'broker_fee_url': 'http://dummy-url'})
    data = fetcher.fetch_fees()
    assert 'fee' not in data.get('broker', {}).get('data', {})

def test_fee_data_fetcher_logs_error(monkeypatch):
    class DummyResponse:
        def raise_for_status(self): raise Exception('fail')
    monkeypatch.setattr('requests.get', lambda url: DummyResponse())
    fetcher = FEEDataFetcher({'broker_fee_url': 'http://dummy-url'}, logger=DummyLogger)
    with pytest.raises(Exception):
        fetcher.fetch_fees()
