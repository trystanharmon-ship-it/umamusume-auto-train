import os
import subprocess

import cv2
import numpy as np


class ADB:
    def __init__(self, adb_dir="../adb", device_id="127.0.0.1:5555"):
        # Path to adb.exe inside the project
        self.adb_path = os.path.join(os.path.dirname(__file__), adb_dir, "adb.exe")
        self.device_id = device_id

    def run(self, cmd):
        """
        Execute adb command on the target device.
        """
        base_cmd = [self.adb_path]
        if self.device_id:
            base_cmd += ["-s", self.device_id]

        result = subprocess.run(
            base_cmd + cmd.split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.stderr.strip():
            print(f"[ADB ERROR] {result.stderr.strip()}")
        return result.stdout.strip()

    def devices(self):
        """
        List all connected devices.
        """
        return subprocess.run(
            [self.adb_path, "devices"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.strip()

    def connect(self):
        """
        Connect to an emulator/device using device id.
        """
        return subprocess.run(
            [self.adb_path, "connect", self.device_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.strip()

    def disconnect(self):
        """
        Disconnect a device.
        """
        return subprocess.run(
            [self.adb_path, "disconnect", self.device_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        ).stdout.strip()

    def tap(self, x, y):
        """
        Simulate tap on screen.
        """
        return self.run(f"shell input tap {x} {y}")

    def swipe(self, x1, y1, x2, y2, duration=300):
        """
        Simulate swipe from (x1,y1) to (x2,y2) within given duration (ms).
        """
        return self.run(f"shell input swipe {x1} {y1} {x2} {y2} {duration}")

    def long_tap(self, x, y, duration=3000):
        """
        Simulate long tap at (x, y).
        Duration in milliseconds.
        """
        return self.run(f"shell input swipe {x} {y} {x} {y} {duration}")

    def text(self, content):
        """
        Input text to the device.
        """
        return self.run(f"shell input text {content}")

    def screenshot(self, crop=None, save_path=None):
        """
        Capture a screenshot from emulator and return as NumPy array (BGR).

        Return: (left, top, right, bottom)

        Params:
        - crop: tuple (x1, y1, x2, y2) or None / left, top, right, bottom
        - save_path: str, e.g. 'screenshot.png'
        """
        proc = subprocess.Popen(
            [self.adb_path, "-s", "127.0.0.1:5555", "exec-out", "screencap", "-p"],
            stdout=subprocess.PIPE,
        )
        data, _ = proc.communicate()

        # Decode PNG bytes to NumPy array
        img = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)

        if crop:
            x1, y1, x2, y2 = crop
            img = img[y1:y2, x1:x2]

        if save_path:
            cv2.imwrite(save_path, img)
            print(f"[INFO] Screenshot saved to {save_path}")

        return img
