import tkinter as tk
from tkinter import ttk
import pyautogui
import keyboard
import time
import threading
from PIL import ImageGrab


class ColorAndCoordPicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Color and Coordinate Picker with History")
        self.running = False
        self.mode = "live"  # live, record, manual

        # GUI Components
        ttk.Label(root, text="X:").grid(row=0, column=0, padx=10, pady=5)
        self.x_label = ttk.Label(root, text="0")
        self.x_label.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(root, text="Y:").grid(row=1, column=0, padx=10, pady=5)
        self.y_label = ttk.Label(root, text="0")
        self.y_label.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(root, text="RGB:").grid(row=2, column=0, padx=10, pady=5)
        self.rgb_label = ttk.Label(root, text="(0, 0, 0)")
        self.rgb_label.grid(row=2, column=1, padx=10, pady=5)

        # Buttons for Modes
        ttk.Button(root, text="Live", command=self.set_live_mode).grid(row=3, column=0, padx=10, pady=5)
        ttk.Button(root, text="Record", command=self.set_record_mode).grid(row=3, column=1, padx=10, pady=5)
        ttk.Button(root, text="Manual", command=self.set_manual_mode).grid(row=3, column=2, padx=10, pady=5)

        # Stop Button
        self.stop_button = ttk.Button(root, text="Stop", command=self.stop, state="disabled")
        self.stop_button.grid(row=4, column=1, padx=10, pady=5)

        # Scrollable Listbox for History
        self.history_frame = ttk.Frame(root)
        self.history_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

        self.history_listbox = tk.Listbox(self.history_frame, height=10, width=50)
        self.history_listbox.pack(side="left", fill="y")

        self.scrollbar = ttk.Scrollbar(self.history_frame, orient="vertical", command=self.history_listbox.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.history_listbox.config(yscrollcommand=self.scrollbar.set)

        # Start Live Updates
        threading.Thread(target=self.update_display, daemon=True).start()

    def get_mouse_info(self):
        # Get mouse position
        x, y = pyautogui.position()

        # Get screen color at mouse position
        img = ImageGrab.grab(bbox=(x, y, x + 1, y + 1))  # Capture 1x1 pixel
        rgb = img.getpixel((0, 0))
        return x, y, rgb

    def update_display(self):
        while True:
            if self.mode == "live":
                x, y, rgb = self.get_mouse_info()
                self.update_labels(x, y, rgb)
                self.add_to_history(x, y, rgb, "Live", "red")
            elif self.mode == "record" and self.running:
                x, y, rgb = self.get_mouse_info()
                self.update_labels(x, y, rgb)
                self.add_to_history(x, y, rgb, "Record", "green")
                time.sleep(0.5)  # 0.5-second interval
            elif self.mode == "manual Press S" and keyboard.is_pressed("s"):
                x, y, rgb = self.get_mouse_info()
                self.update_labels(x, y, rgb)
                self.add_to_history(x, y, rgb, "Manual", "blue")
                time.sleep(0.3)  # Prevent multiple detections per press
            time.sleep(0.1)  # General loop delay

    def update_labels(self, x, y, rgb):
        self.x_label.config(text=str(x))
        self.y_label.config(text=str(y))
        self.rgb_label.config(text=str(rgb))

    def add_to_history(self, x, y, rgb, mode, color):
        entry = f"({x}, {y}) - RGB: {rgb} [{mode}]"
        self.history_listbox.insert("end", entry)
        self.history_listbox.itemconfig("end", foreground=color)
        self.history_listbox.yview_moveto(1)  # Scroll to bottom automatically

    def set_live_mode(self):
        self.mode = "live"
        self.running = False
        self.stop_button.config(state="disabled")

    def set_record_mode(self):
        self.mode = "record"
        self.running = True
        self.stop_button.config(state="normal")

    def set_manual_mode(self):
        self.mode = "manual"
        self.running = False
        self.stop_button.config(state="disabled")

    def stop(self):
        self.running = False
        self.stop_button.config(state="disabled")


if __name__ == "__main__":
    root = tk.Tk()
    app = ColorAndCoordPicker(root)
    root.mainloop()
