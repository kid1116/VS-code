import sys
import os
import ctypes
import logging
import warnings

# Enable DPI awareness on Windows BEFORE tkinter imports.
if sys.platform == "win32":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # Per-Monitor
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

import tkinter as tk
from tkinter import messagebox

# Suppress noisy logs from easyocr/torch.
logging.getLogger("easyocr").setLevel(logging.WARNING)
logging.getLogger("torch").setLevel(logging.WARNING)
warnings.filterwarnings("ignore")

import easyocr
import numpy as np
import pyperclip
from PIL import ImageGrab, Image

# Force UTF-8 output on Windows terminals.
os.environ.setdefault("PYTHONIOENCODING", "utf-8")
for stream in (sys.stdout, sys.stderr):
    try:
        stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class AreaSelector:
    """Show a full-screen screenshot in a window; user drags to select a region."""

    def __init__(self, screenshot: Image.Image):
        self.screenshot = screenshot

        self.root = tk.Tk()
        self.root.title("框选文字区域 - 按 Esc 取消")
        self._photo = self._pil_to_tk(screenshot)

        # Size the window to fit the screen (but not exceed it).
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        iw, ih = screenshot.size
        cw = min(iw, sw - 40)
        ch = min(ih, sh - 80)
        self.root.geometry(f"{cw}x{ch}+{max((sw-cw)//2,0)}+{max((sh-ch)//2,0)}")

        # Scrollable canvas for large images.
        self.canvas = tk.Canvas(self.root, highlightthickness=0, cursor="cross")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Store the image on the canvas.
        self._canvas_img = self.canvas.create_image(0, 0, anchor=tk.NW, image=self._photo)

        # Scroll bindings.
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

        self.start_x = None
        self.start_y = None
        self.rect = None
        self.bbox = None

        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Escape>", lambda e: self._quit(None))

        self.root.protocol("WM_DELETE_WINDOW", lambda: self._quit(None))

    @staticmethod
    def _pil_to_tk(img: Image.Image):
        """Convert PIL Image to tkinter PhotoImage."""
        import io

        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return tk.PhotoImage(data=buf.getvalue())

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def _normalize(self, x1, y1, x2, y2):
        return (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

    def on_press(self, event):
        # Convert canvas-relative coords to image-pixel coords.
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        if self.rect:
            self.canvas.delete(self.rect)

    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        x1, y1, x2, y2 = self._normalize(self.start_x, self.start_y, cx, cy)
        self.rect = self.canvas.create_rectangle(
            x1, y1, x2, y2, outline="red", width=2, fill=""
        )

    def on_release(self, event):
        if self.start_x is None:
            return
        cx = self.canvas.canvasx(event.x)
        cy = self.canvas.canvasy(event.y)
        x1, y1, x2, y2 = self._normalize(self.start_x, self.start_y, cx, cy)
        # Clamp to image bounds.
        iw, ih = self.screenshot.size
        self.bbox = (
            max(0, int(x1)),
            max(0, int(y1)),
            min(iw, int(x2)),
            min(ih, int(y2)),
        )
        self.root.destroy()

    def _quit(self, _):
        self.bbox = None
        self.root.destroy()

    def run(self):
        self.root.mainloop()
        return self.bbox


def main():
    print("正在截取全屏...")
    full = ImageGrab.grab()

    selector = AreaSelector(full)
    bbox = selector.run()

    if bbox is None:
        print("已取消。")
        sys.exit(0)

    if bbox[2] - bbox[0] < 5 or bbox[3] - bbox[1] < 5:
        print("选中区域过小，已取消。")
        sys.exit(0)

    print(f"选中区域: {bbox}")
    print("正在识别文字...")
    crop = full.crop(bbox)

    reader = easyocr.Reader(["ch_sim", "en"], gpu=False, verbose=False)
    results = reader.readtext(np.array(crop))

    if not results:
        print("未识别到文字。")
        sys.exit(0)

    for _, text, confidence in results:
        print(f"[{confidence:.2f}] {text}")

    full_text = "\n".join(t for _, t, _ in results)
    pyperclip.copy(full_text)
    print("\n---")
    print("文字已复制到剪贴板。")
    print(full_text)


if __name__ == "__main__":
    main()
