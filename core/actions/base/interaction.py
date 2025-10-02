# core/actions/base/interaction.py
from .input import Input
from core.recognizer import Recognizer

from utils import log
import utils.helper as helper


class Interaction:
    def __init__(self, input: Input, recognizer: Recognizer):
        self.input = input
        self.recognizer = recognizer

    def click_element(
        self,
        image_path: str,
        region: tuple = None,
        max_search_time: float = 2.0,
        clicks: int = 1,
        delay: float = 0.2,
        text: str = "",
    ):
        """Click on UI element by image"""
        image = self.recognizer.locate_on_screen(
            template_path=image_path,
            region=region,
            max_search_time=max_search_time,
        )
        if not image:
            log.debug(f"Image not found: {image_path}")
            return False

        center_x, center_y = helper.get_center(image)
        clicked = self.input.tap(center_x, center_y, clicks, delay)

        if clicked:
            log.debug(f"Clicked: {image_path}")
            if text:
                log.info(text)

        return clicked

    def click_coordinates(
        self, x: int, y: int, clicks: int = 1, delay: float = 0.2, text: str = ""
    ):
        """Clcik on coordinates"""
        if x is None or y is None:
            raise ValueError("Invalid coordinates provided")

        clicked = True
        if not self.input.tap(x, y, clicks, delay):
            clicked = False
        if text and clicked:
            log.info(text)

        return clicked

    def click_boxes(
        self, boxes: list | tuple, clicks: int = 1, delay: float = 0.3, text: str = ""
    ):
        """Click on boxes - handles both single box or list of boxes"""
        if not boxes:
            return False

        if isinstance(boxes, list):
            if not boxes:
                return False
            box = boxes[0]
        else:
            box = boxes

        if len(box) != 4:
            log.error(f"Invalid box format: {box}")
            return False

        x, y = helper.get_center(box)
        clicked = self.input.tap(x, y, clicks, delay)

        if clicked and text:
            log.info(text)

        return clicked

    def swipe_between_points(
        self, x1: int, y1: int, x2: int, y2: int, duration: int = 200
    ) -> bool:
        """Swipe between two coordinate points"""
        return self.input.swipe(x1, y1, x2, y2, duration)

    def swipe_between_elements(
        self, from_element, to_element, duration: int = 200
    ) -> bool:
        """Swipe from one UI element to another"""
        from_center = helper.get_center(from_element)
        to_center = helper.get_center(to_element)
        return self.swipe_between_points(
            from_center[0], from_center[1], to_center[0], to_center[1], duration
        )

    def swipe_up(
        self,
        start_x: int = 400,
        start_y: int = 850,
        distance: int = 250,
        duration: int = 700,
    ) -> bool:
        """Swipe up from position"""
        return self.swipe_between_points(
            start_x, start_y, start_x, start_y - distance, duration
        )

    def swipe_for_scroll(
        self, start_x: int = 400, start_y: int = 850, distance: int = 250, duration=400
    ) -> bool:
        """Standard swipe for scrolling lists (default value is for race list scrolling)"""
        success = False
        if self.swipe_up(start_x, start_y, distance, duration):
            self.click_coordinates(start_x, start_y)
            success = True
        helper.sleep(0.5)
        return success
