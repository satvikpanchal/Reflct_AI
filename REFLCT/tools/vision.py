import mss, os
from PIL import Image
from datetime import datetime

def take_screenshot():
    with mss.mss() as sct:
        sct_img = sct.grab(sct.monitors[1])
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")

        os.makedirs("logs", exist_ok=True)
        path = f"logs/{datetime.now().strftime('%Y%m%d_%H%M%S')}_screenshot.png"
        img.save(path)
        print(f"Screenshot saved to {path}")
        return img
