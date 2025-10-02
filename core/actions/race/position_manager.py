# core/actions/race/position_manager.py
import re

import core.config as config
from core.ocr import OCR
from core.actions.base import Interaction

from utils.log import info, debug
from utils.helper import sleep, get_secs
from utils import assets_repository


class PositionManager:
    def __init__(self, interaction: Interaction, ocr: OCR):
        self.interaction = interaction
        self.ocr = ocr
        self.preferred_position_set = False

    def select_position(self):
        """Select optimal position based on configuration"""
        if not config.POSITION_SELECTION_ENABLED:
            return

        if config.ENABLE_POSITIONS_BY_RACE:
            self._select_position_by_race_type()
        elif not self.preferred_position_set:
            self._select_preferred_position()

    def _select_position_by_race_type(self):
        """Select position based on race type analysis"""
        race_type = self._analyze_race_type()
        if not race_type:
            return

        position = config.POSITIONS_BY_RACE.get(race_type)
        if position:
            info(f"Selecting position {position} based on race type {race_type}")
            self._apply_position(position)

    def _analyze_race_type(self) -> str:
        """Analyze race type from race info"""
        if not self.interaction.click_element(
            assets_repository.get_button("info_btn"), max_search_time=get_secs(5)
        ):
            return None

        sleep(0.5)

        # Extract race type from race info
        from utils import constants

        race_info_screen = self.interaction.input.take_screenshot(
            constants.RACE_INFO_TEXT_REGION
        )
        race_info_text = self.ocr.extract_text(race_info_screen)
        debug(f"Race info text: {race_info_text}")

        # Close info window
        self.interaction.click_element(
            assets_repository.get_button("close_btn"), max_search_time=get_secs(2)
        )

        # Extract race type from parentheses
        match = re.search(r"\(([^)]+)\)", race_info_text)
        return match.group(1).strip().lower() if match else None

    def _select_preferred_position(self):
        """Select configured preferred position"""
        position = config.PREFERRED_POSITION
        self._apply_position(position)
        self.preferred_position_set = True

    def _apply_position(self, position: str):
        """Apply specific position selection"""
        if not self.interaction.click_element(
            assets_repository.get_button("change_btn"), max_search_time=get_secs(7)
        ):
            return

        self.interaction.click_element(
            assets_repository.get_button(f"positions/{position}_position_btn"),
            max_search_time=get_secs(2),
        )

        self.interaction.click_element(
            assets_repository.get_button("confirm_btn"), max_search_time=get_secs(2)
        )
