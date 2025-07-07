import time
import random
import os
from pynput.keyboard import Controller, Key
from PIL import Image, ImageGrab, ImageChops
import numpy as np

# === CONFIGURATION ===
TEXT_OPTIONS = ["proceed", "ok", "yes"]
RANDOMIZATION_RANGE = 10  # seconds between checks
RANDOMIZATION_I_O = 0.2  # seconds between I/O operations

# Screenshot comparison configuration
SCREENSHOT_FOLDER = "screenshot"
IGNORE_BOTTOM_PIXELS = 40  # pixels from the bottom to ignore (e.g., taskbar)

# Tolerance for pixel differences (%)
PIXEL_DIFF_TOLERANCE = 0.5  # percent
# ======================

keyboard = Controller()

def simulate_keyboard_input(text: str):
    keyboard.type(text)
    time.sleep(RANDOMIZATION_I_O)  # Allow OS time
    keyboard.press(Key.enter)
    time.sleep(RANDOMIZATION_I_O)  # Allow OS time
    keyboard.release(Key.enter)

def take_screenshot(filename):
    if not os.path.exists(SCREENSHOT_FOLDER):
        os.makedirs(SCREENSHOT_FOLDER)
    filepath = os.path.join(SCREENSHOT_FOLDER, filename)
    img = ImageGrab.grab()
    width, height = img.size
    img_cropped = img.crop((0, 0, width, height - IGNORE_BOTTOM_PIXELS))
    img_cropped.save(filepath)
    img_cropped.close()
    time.sleep(RANDOMIZATION_I_O)  # Allow OS time to flush file write
    return filepath

def are_images_same(file1, file2, tolerance=PIXEL_DIFF_TOLERANCE):
    try:
        if not file1 or not file2:
            return False
        if not os.path.exists(file1) or not os.path.exists(file2):
            print(f"[COMPARE] One of the files does not exist: {file1}, {file2}")
            return False

        img1 = Image.open(file1).convert("RGB")
        img2 = Image.open(file2).convert("RGB")

        diff = ImageChops.difference(img1, img2)
        bbox = diff.getbbox()

        img1.close()
        img2.close()

        if bbox is None:
            return True  # Perfect match
        else:
            diff_np = np.array(diff)
            nonzero = np.count_nonzero(diff_np)
            total = diff_np.size
            percent_diff = (nonzero / total) * 100

            print(f"[COMPARE] Percent difference: {percent_diff:.4f}%")
            return percent_diff < tolerance

    except Exception as e:
        print(f"[COMPARE] Error during image comparison: {e}")
        return False

def cleanup_screenshots(exclude_file):
    for f in os.listdir(SCREENSHOT_FOLDER):
        full_path = os.path.join(SCREENSHOT_FOLDER, f)
        if full_path != exclude_file:
            os.remove(full_path)

def main():
    print(f"Running screen-checking keyboard simulator with {TEXT_OPTIONS} entries.")
    last_screenshot = None

    try:
        while True:
            temp_screenshot = take_screenshot("temp.png")
            time.sleep(RANDOMIZATION_I_O*10)

            print(f"Comparing: {temp_screenshot} with {last_screenshot}")
            if are_images_same(temp_screenshot, last_screenshot):
                cleanup_screenshots(temp_screenshot)

                interval = random.uniform(0,RANDOMIZATION_I_O)
                time.sleep(interval)

                text_to_type = random.choice(TEXT_OPTIONS)
                simulate_keyboard_input(text_to_type)

            # Promote temp.png to current.png
            current_path = os.path.join(SCREENSHOT_FOLDER, "current.png")
            if os.path.exists(current_path):
                os.remove(current_path)
            os.rename(temp_screenshot, current_path)
            time.sleep(RANDOMIZATION_I_O)

            # Copy current.png to last.png
            last_screenshot = os.path.join(SCREENSHOT_FOLDER, "last.png")
            with Image.open(current_path).convert("RGB") as img:
                img.save(last_screenshot)
            time.sleep(RANDOMIZATION_I_O)

            wait_after = random.uniform(0, RANDOMIZATION_RANGE)
            time.sleep(wait_after)

    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == "__main__":
    main()
