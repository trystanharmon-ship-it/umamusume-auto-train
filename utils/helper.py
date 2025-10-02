import cv2
import numpy as np
import time
import core.config as config


def xywh_to_ltrb(region):
    x, y, w, h = region
    return (x, y, x + w, y + h)


def crop_screen(screen, box):
    """
    Crop the screen based on box (x, y, w, h)

    return:
    (x, y, w, h)
    """
    x, y, w, h = box
    return screen[y : y + h, x : x + w]


def enhance_img(img, scale: float = 2.0, threshold: int = 180):
    """
    Enhance image for better OCR accuracy
    - Convert to grayscale
    - Resize (make text clearer)
    - Apply threshold (binarization)
    - Small morphology ops to clean noise

    params:
    - img: np.array
    - scale: resize image
    - threshold: int
    """
    if img is None or img.size == 0:
        return img

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # resize (enlarge image for better OCR readability)
    if scale != 1.0:
        gray = cv2.resize(gray, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # apply threshold (black & white)
    _, binary = cv2.threshold(gray, threshold, 255, cv2.THRESH_BINARY)

    # optional: morphology (remove small noise)
    kernel = np.ones((1, 1), np.uint8)
    clean = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

    return clean


def sleep(seconds=1):
    time.sleep(seconds * config.SLEEP_TIME_MULTIPLIER)


def get_secs(seconds=1):
    return seconds * config.SLEEP_TIME_MULTIPLIER


def get_center(box):
    x, y, w, h = box
    return x + w // 2, y + h // 2
