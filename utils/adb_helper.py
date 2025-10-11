import os
import subprocess

import cv2
import numpy as np
from adbutils import adb


class ADB:
    def __init__(self, device_id="127.0.0.1:5555"):
        # Path to adb.exe inside the project
        self.device_id = device_id
        self.device = adb.device(device_id)

    def devices(self):
        """
        List all connected devices.
        """
        return adb.devices()

    def connect(self):
        """
        Connect to an emulator/device using device id.
        """
        adb.connect(self.device_id)

    def disconnect(self):
        """
        Disconnect a device.
        """
        adb.disconnect(self.device_id)

    def tap(self, x, y):
        """
        Simulate tap on screen.
        """
        return self.device.click(x, y)

    def swipe(self, x1, y1, x2, y2, duration=0.3):
        """
        Simulate swipe from (x1,y1) to (x2,y2) within given duration (ms).
        """
        return self.device.swipe(x1, y1, x2, y2, duration)

    def long_tap(self, x, y, duration=3):
        """
        Simulate long tap at (x, y).
        Duration in milliseconds.
        """
        return self.device.swipe(x, y, x, y, duration)

    def text(self, content):
        """
        Input text to the device.
        """
        return self.device.send_keys(content)

    def screenshot(self, crop=None, save_path=None):
        """
        Capture a screenshot from emulator and return as NumPy array (BGR).

        Return: (left, top, right, bottom)

        Params:
        - crop: tuple (x1, y1, x2, y2) or None / left, top, right, bottom
        - save_path: str, e.g. 'screenshot.png'
        """
        data = self.device.screenshot(error_ok=False)

        # Decode PNG bytes to NumPy array
        img = cv2.cvtColor(np.array(data, dtype=np.uint8), cv2.COLOR_RGB2BGR)

        if crop:
            x1, y1, x2, y2 = crop
            img = img[y1:y2, x1:x2]

        if save_path:
            cv2.imwrite(save_path, img)
            print(f"[INFO] Screenshot saved to {save_path}")

        return img
