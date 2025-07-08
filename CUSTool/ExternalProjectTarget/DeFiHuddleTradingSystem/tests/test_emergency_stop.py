import pytest
import os
import json
from src.core.emergency_stop import EmergencyStop, EMERGENCY_STOP_FILE

@pytest.fixture(autouse=True)
def cleanup():
    if os.path.exists(EMERGENCY_STOP_FILE):
        os.remove(EMERGENCY_STOP_FILE)
    yield
    if os.path.exists(EMERGENCY_STOP_FILE):
        os.remove(EMERGENCY_STOP_FILE)

def test_emergency_stop_activation_and_persistence():
    stop = EmergencyStop()
    assert not stop.is_active()
    stop.activate()
    assert stop.is_active()
    # Simulate reload
    stop2 = EmergencyStop()
    assert stop2.is_active()
    stop2.deactivate()
    assert not stop2.is_active()
    # Simulate reload
    stop3 = EmergencyStop()
    assert not stop3.is_active()

def test_emergency_stop_file_corruption():
    with open(EMERGENCY_STOP_FILE, 'w') as f:
        f.write('not json')
    stop = EmergencyStop()
    assert not stop.is_active()
