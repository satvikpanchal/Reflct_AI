import re
from datetime import datetime
from pathlib import Path
import mss
from PIL import Image

# --- core screenshot ---
def take_screenshot(monitor: int = 1, out_dir: str = "logs") -> str:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    path = Path(out_dir) / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_monitor{monitor}.png"
    with mss.mss() as sct:
        if monitor < 0 or monitor >= len(sct.monitors):
            raise ValueError(f"Monitor {monitor} not found (available: 1..{len(sct.monitors)-1}, or 0 for 'all').")
        mon = sct.monitors[monitor]
        grabbed = sct.grab(mon)
    img = Image.frombytes("RGB", grabbed.size, grabbed.bgra, "raw", "BGRX")
    img.save(path)
    return str(path)

# --- tiny natural-language router ---
_WORD_NUM = {
    "zero": 0, "all": 0, "one": 1, "first": 1, "two": 2, "second": 2, "three": 3, "third": 3,
    "primary": 1, "main": 1, "left": 1, "right": 2
}

def parse_monitor(text: str, default: int = 1) -> int:
    text = text.lower().strip()

    m = re.search(r"\bmonitor\s*(\d+)\b", text)
    if m:
        return int(m.group(1))

    for word, num in _WORD_NUM.items():
        if re.search(rf"\b{word}\b", text):
            return num

    m = re.search(r"\b(\d+)\b", text)  # last resort: any lone number
    return int(m.group(1)) if m else default

def handle_request(text: str) -> str:
    mon = parse_monitor(text)
    path = take_screenshot(mon)
    return f"Screenshot saved: {path}"

# # test
# if __name__ == "__main__":
#     # Simulate LLM messages:
#     print(handle_request("take a screenshot on monitor 2"))
#     print(handle_request("screenshot primary"))
#     print(handle_request("screenshot all monitors"))
