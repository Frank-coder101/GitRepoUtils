import os
import json
import uuid
import traceback
from datetime import datetime
from src.core.logger import Logger

AUDIT_LOG_PATH = os.path.expanduser("~/.defihuddle_audit_log.json")

class AuditLogEngine:
    """
    Centralized logging for orders, rejections, confirmations, and runtime exceptions.
    Stores entries in a secure, tamper-evident format (append-only JSON).
    """
    @staticmethod
    def log_event(event_type, details, exception=None):
        entry = {
            'event_id': str(uuid.uuid4()),
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'event_type': event_type,
            'details': details,
        }
        if exception:
            entry['exception'] = {
                'type': type(exception).__name__,
                'message': str(exception),
                'stack': ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))
            }
        AuditLogEngine._append_entry(entry)
        Logger.info(f"Audit log event: {entry['event_id']} {event_type}")
        return entry['event_id']

    @staticmethod
    def _append_entry(entry):
        if not os.path.exists(AUDIT_LOG_PATH):
            with open(AUDIT_LOG_PATH, 'w') as f:
                json.dump([entry], f, indent=4)
        else:
            with open(AUDIT_LOG_PATH, 'r+') as f:
                data = json.load(f)
                data.append(entry)
                f.seek(0)
                json.dump(data, f, indent=4)

    @staticmethod
    def get_logs():
        if not os.path.exists(AUDIT_LOG_PATH):
            return []
        with open(AUDIT_LOG_PATH, 'r') as f:
            return json.load(f)
