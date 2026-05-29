import datetime as dt
import time
from pathlib import Path

import pyautogui
import pyperclip


PROJECT_DIR = Path(__file__).resolve().parent
SCREENSHOT_DIR = PROJECT_DIR / "screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

CHATGPT_IMAGES_URL = "https://chatgpt.com/images/"

# Calibrated on the current Edge layout: first image under "我的图片".
FIRST_IMAGE_POINT = (235, 795)


def wait(seconds: float) -> None:
    time.sleep(seconds)


def open_images_page() -> None:
    # Close any previous image viewer. Multiple Esc presses are intentional:
    # Edge/ChatGPT sometimes keeps focus in the prompt box or toolbar.
    for _ in range(3):
        pyautogui.press("esc")
        wait(0.4)
    pyautogui.hotkey("ctrl", "l")
    pyperclip.copy(CHATGPT_IMAGES_URL)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
    wait(18.0)
    pyautogui.hotkey("ctrl", "r")
    wait(25.0)
    pyautogui.press("home")
    wait(1.0)


def open_first_image() -> None:
    # Put focus back on the page body before clicking the first gallery item.
    pyautogui.click(950, 620)
    wait(0.8)
    pyautogui.click(*FIRST_IMAGE_POINT)
    wait(8.0)


def capture_review() -> Path:
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    path = SCREENSHOT_DIR / f"latest_image_full_review_{timestamp}.png"
    pyautogui.screenshot(str(path))
    return path


def main() -> None:
    open_images_page()
    open_first_image()
    path = capture_review()
    print(path, flush=True)
    # Leave the browser out of modal/image-viewer mode for the next automation pass.
    pyautogui.press("esc")
    wait(0.5)


if __name__ == "__main__":
    main()
