# core/race/race_strategy.py
from abc import ABC, abstractmethod

from core.actions import Interaction, Navigation

from utils.log import info, debug
from utils.helper import sleep, get_secs
from utils import assets_repository


class RaceStrategy(ABC):
    def __init__(self, interaction: Interaction, navigation: Navigation):
        self.interaction = interaction
        self.navigation = navigation

    @abstractmethod
    def select_race(self) -> bool:
        pass


class G1RaceStrategy(RaceStrategy):
    def __init__(self, interaction, navigation, race_name: str):
        super().__init__(interaction, navigation)
        self.race_name = race_name

    def select_race(self) -> bool:
        """Select specific G1 race by name"""
        info(f"Looking for {self.race_name}.")

        for i in range(2):  # 2 scroll attempts
            if self._try_select_race():
                return True
            self.interaction.swipe_for_scroll()

        return False

    def _try_select_race(self) -> bool:
        """Try to select the target race"""
        if self.interaction.click_element(
            assets_repository.get_race(self.race_name),
            max_search_time=get_secs(0.7),
            text=f"{self.race_name} found.",
        ):
            return self._confirm_race_selection()
        return False

    def _confirm_race_selection(self) -> bool:
        """Confirm race selection by clicking race button twice"""
        for _ in range(2):
            if not self.interaction.click_element(
                assets_repository.get_button("race_btn"), max_search_time=get_secs(2)
            ):
                return False
            sleep(0.5)
        return True


class AptitudeRaceStrategy(RaceStrategy):
    def select_race(self) -> bool:
        """Find and select race matching aptitude"""
        info("Looking for aptitude matching race.")

        for i in range(4):  # 4 scroll attempts
            if self._try_find_aptitude_race():
                return True
            self.interaction.swipe_for_scroll()

        return False

    def _try_find_aptitude_race(self) -> bool:
        """Try to find aptitude matching race"""
        match_aptitude = self.interaction.recognizer.locate_on_screen(
            assets_repository.get_ui("match_track"), max_search_time=get_secs(0.7)
        )

        if not match_aptitude:
            return False

        # Check if race is unlocked
        if not self.interaction.recognizer.is_btn_active(match_aptitude, threshold=200):
            info("Race found, but it's locked.")
            return False

        info("Race found.")
        return self._select_and_confirm_race(match_aptitude)

    def _select_and_confirm_race(self, race_element) -> bool:
        """Select race and confirm"""
        if not self.interaction.click_boxes(race_element):
            return False

        for i in range(2):
            if not self.interaction.click_element(
                assets_repository.get_button("race_btn"), max_search_time=get_secs(2)
            ):
                return False
            sleep(0.5)
        return True
