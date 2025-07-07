import cv2, numpy as np, json, os, ctypes, time
from mss import mss

# Load template images from a config file
with open("triggers.json") as f:
    config = json.load(f)

templates = {}
for name, filepath in config.items():
    full_path = os.path.join(os.path.dirname(__file__), filepath)
    tpl = cv2.imread(full_path)
    if tpl is None:
        raise FileNotFoundError(f"Template {filepath} not found")
    templates[name] = tpl

MATCH_THRESHOLD = 0.9  # similarity threshold
SLEEP_SECONDS = 3  # seconds to wait between checks (configurable)
LOG_FILE = "detection_log.txt"

# Helper to simulate a left mouse click at (x, y)
def click_at(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTDOWN
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # MOUSEEVENTF_LEFTUP

while True:
    # Capture full screen (all monitors)
    with mss() as sct:
        screenshot = np.array(sct.grab(sct.monitors[0]))

    gray_screen = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
    found_buttons = []

    for name, tpl in templates.items():
        tpl_gray = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
        res = cv2.matchTemplate(gray_screen, tpl_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if max_val >= MATCH_THRESHOLD:
            found_buttons.append((name, max_loc, tpl.shape[1], tpl.shape[0]))  # (name, (x, y), w, h)
            print(f"Detected '{name}' button at {max_loc} (confidence {max_val:.2f})")

    if found_buttons:
        for name, (x, y), w, h in found_buttons:
            center_x = x + w // 2
            center_y = y + h // 2
            click_at(center_x, center_y)
            log_msg = f"{time.strftime('%Y-%m-%d %H:%M:%S')} - Clicked '{name}' at ({center_x}, {center_y})\n"
            with open(LOG_FILE, "a") as logf:
                logf.write(log_msg)
            print(log_msg.strip())
        print(f"Sleeping for {SLEEP_SECONDS} seconds after click...")
        time.sleep(SLEEP_SECONDS)
    else:
        print("No trigger buttons detected. Retrying in", SLEEP_SECONDS, "seconds...")
        time.sleep(SLEEP_SECONDS)
