print("=== CUS STARTING - IMPORT PHASE ===")

try:
    import os
    print("os imported")
except Exception as e:
    print(f"os import failed: {e}")
    exit(1)

try:
    import time
    print("time imported")
except Exception as e:
    print(f"time import failed: {e}")
    exit(1)

try:
    import subprocess
    print("subprocess imported")
except Exception as e:
    print(f"subprocess import failed: {e}")
    exit(1)

try:
    import random
    print("random imported")
except Exception as e:
    print(f"random import failed: {e}")
    exit(1)

print("=== BASIC IMPORTS SUCCESSFUL ===")

try:
    from pynput.keyboard import Controller, Key
    print("pynput imported successfully")
except Exception as e:
    print(f"pynput import failed: {e}")
    exit(1)

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    print("watchdog imported successfully")
except Exception as e:
    print(f"watchdog import failed: {e}")
    exit(1)

print("=== ALL IMPORTS SUCCESSFUL ===")
print("=== SCRIPT COMPLETE ===")
