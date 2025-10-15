# core_emu/actions/base/input.py
from utils.adb_helper import ADB
from utils import log
import utils.helper as helper


class Input:
    def __init__(self, adb: ADB, bot_ref=None):
        self.adb = adb
        self.bot_ref = bot_ref

    def _should_stop(self) -> bool:
        """Check if bot should stop immediately"""
        return self.bot_ref and not self.bot_ref.is_running

    def tap(self, x: int, y: int, clicks: int = 1, delay=0.2):
        if self._should_stop():
            log.debug("Bot stopped - skipping tap")
            return False

        try:
            for _ in range(clicks):
                if self._should_stop():
                    log.debug("Bot stopped during tap sequence")
                    return False

                self.adb.tap(x, y)
                helper.sleep(delay)
            return True
        except Exception as e:
            log.error(f"Tap failed at ({x}, {y}): {e}")
            return False

    def swipe(self, x1, y1, x2, y2, duration=0.2):
        if self._should_stop():
            log.debug("Bot stopped - skipping swipe")
            return False

        try:
            if not all([x1, y1, x2, y2]):
                raise ValueError("Invalid coordinates provided")
            self.adb.swipe(x1, y1, x2, y2, duration=duration)
            return True
        except Exception as e:
            log.error(f"Swipe error at ({x1}, {y1}, {x2}, {y2}): {e}")
            return False

    def take_screenshot(self, region: tuple = None):
        if self._should_stop():
            log.debug("Bot stopped - skipping screenshot")
            return False

        try:
            return self.adb.screenshot(crop=region)
        except Exception as e:
            log.error(f"Screen shot failed: {e}")
            return None
