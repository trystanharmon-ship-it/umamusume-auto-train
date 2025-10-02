# core/actions/race/race_manager.py
from .race_strategy import G1RaceStrategy, AptitudeRaceStrategy
from .position_manager import PositionManager
from .race_executor import RaceExecutor

from core.actions.base import Interaction, Navigation
import core.config as config

from utils.log import info, debug
from utils.helper import sleep, get_secs
from utils import assets_repository


class RaceManager:
    def __init__(self, interaction: Interaction, navigation: Navigation, ocr):
        self.interaction = interaction
        self.navigation = navigation
        self.ocr = ocr

        self.position_manager = PositionManager(interaction, ocr)
        self.race_executor = RaceExecutor(interaction, self.position_manager)
        self.consecutive_races_canceled = False

    def handle_race_day(self, is_finale: bool = False) -> bool:
        """Handle race day flow"""
        if is_finale:
            info("URA Finale flow.")
            button_name = "ura_race_btn"
        else:
            info("Race day flow.")
            button_name = "race_day_btn"

        return self._navigate_and_execute_race(button_name)

    def handle_g1_race(self, race_name: str) -> bool:
        """Handle G1 race participation"""
        if not self._navigate_to_races():
            return False

        if not self._handle_consecutive_races():
            return False

        strategy = G1RaceStrategy(self.interaction, self.navigation, race_name)
        return self._execute_race_strategy(strategy)

    def handle_goal_race(self) -> bool:
        """Handle goal-based race participation"""
        if not self._navigate_to_races():
            return False

        if not self._handle_consecutive_races():
            return False

        strategy = AptitudeRaceStrategy(self.interaction, self.navigation)
        return self._execute_race_strategy(strategy)

    def _navigate_and_execute_race(self, button_name: str) -> bool:
        """Generic race navigation and execution"""
        # Navigate to race screen
        if not self.interaction.click_element(
            assets_repository.get_button(button_name), 
            max_search_time=get_secs(10)
        ):
            return False

        self.interaction.click_element(
            assets_repository.get_button("ok_btn"), 
            max_search_time=get_secs(1)
        )
        sleep(0.5)

        # Race button clicks
        for i in range(2):
            if not self.interaction.click_element(
                assets_repository.get_button("race_btn"), 
                max_search_time=get_secs(2)
            ):
                return False
            sleep(0.5)

        sleep(5)
        return self.race_executor.execute_race()

    def _navigate_to_races(self) -> bool:
        """Navigate to races screen"""
        return self.interaction.click_element(
            assets_repository.get_button("races_btn"), max_search_time=get_secs(10)
        )

    def _handle_consecutive_races(self) -> bool:
        """Handle consecutive race warning"""
        cancel_btn = self.interaction.recognizer.locate_on_screen(
            assets_repository.get_button("cancel_btn"), max_search_time=get_secs(0.7)
        )

        if not cancel_btn:
            return True

        if config.CANCEL_CONSECUTIVE_RACE:
            info("Cancelling consecutive race, doing training instead.")
            return self.interaction.click_element(
                assets_repository.get_button("cancel_btn")
            )
        else:
            return self.interaction.click_element(
                assets_repository.get_button("ok_btn")
            )

    def _execute_race_strategy(self, strategy) -> bool:
        """Execute race selection strategy"""
        success = strategy.select_race()

        if not success:
            self.navigation.go_back("Race not found. Proceeding to training.")
            sleep(0.5)
            return False

        self.race_executor.execute_race()
        return True

    def _execute_race_day(self) -> bool:
        """Execute race day flow"""
        self.race_executor.execute_race()
        return True
