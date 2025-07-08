import os
import json
from src.core.logger import Logger

EMERGENCY_STOP_FILE = 'emergency_stop_state.json'

class EmergencyStop:
    def __init__(self):
        self.state = self.load_state()

    def activate(self):
        self.state = {'active': True}
        self.save_state()
        Logger.error('[EMERGENCY STOP] Activated! All orders will be cancelled and trading halted.')

    def deactivate(self):
        self.state = {'active': False}
        self.save_state()
        Logger.info('[EMERGENCY STOP] Deactivated. Trading may resume.')

    def is_active(self):
        return self.state.get('active', False)

    def load_state(self):
        if os.path.exists(EMERGENCY_STOP_FILE):
            try:
                with open(EMERGENCY_STOP_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, ValueError):
                Logger.error('[EMERGENCY STOP] State file corrupted, resetting to default.')
                return {'active': False}
        return {'active': False}

    def save_state(self):
        with open(EMERGENCY_STOP_FILE, 'w') as f:
            json.dump(self.state, f)
