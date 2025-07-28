
import mss
from PIL import Image
from datetime import datetime
import os

def take_screenshot():
    """Captures the screen and returns a PIL Image object."""
    with mss.mss() as sct:
        # Get a screenshot of the primary monitor
        sct_img = sct.grab(sct.monitors[1])
        
        # Convert to a PIL Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        # Save the image to a log file for debugging
        if not os.path.exists("logs"):
            os.makedirs("logs")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = f"logs/{timestamp}_screenshot.png"
        img.save(image_path)
        print(f"Screenshot saved to {image_path}")
        
        return img
