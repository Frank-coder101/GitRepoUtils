import os
import json
from src.data.audit_log import AuditLogEngine

def test_log_event_and_get_logs(tmp_path, monkeypatch):
    # Patch the log path to a temp file
    test_log_path = tmp_path / "audit_log.json"
    monkeypatch.setattr('src.data.audit_log.AUDIT_LOG_PATH', str(test_log_path))
    # Log an event
    event_id = AuditLogEngine.log_event('order', {'order_id': 123, 'status': 'filled'})
    logs = AuditLogEngine.get_logs()
    assert any(e['event_id'] == event_id for e in logs)
    assert logs[0]['event_type'] == 'order'
    assert logs[0]['details']['order_id'] == 123

def test_log_event_with_exception(tmp_path, monkeypatch):
    test_log_path = tmp_path / "audit_log.json"
    monkeypatch.setattr('src.data.audit_log.AUDIT_LOG_PATH', str(test_log_path))
    try:
        raise ValueError('test error')
    except Exception as e:
        event_id = AuditLogEngine.log_event('exception', {'info': 'fail'}, exception=e)
    logs = AuditLogEngine.get_logs()
    assert any(e['event_id'] == event_id for e in logs)
    assert logs[0]['event_type'] == 'exception'
    assert 'exception' in logs[0]
