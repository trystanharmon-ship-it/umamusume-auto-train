# core/skill/skill_buyer.py
from .skill_matcher import SkillMatcher

from core.actions.base import Interaction
from core.ocr import OCR

from utils import assets_repository
from utils.log import info, debug
from utils.helper import sleep, crop_screen


class SkillBuyer:
    def __init__(
        self,
        interaction: Interaction,
        ocr: OCR,
        skill_matcher: SkillMatcher,
    ):
        self.interaction = interaction
        self.ocr = ocr
        self.matcher = skill_matcher
        self.found_skill = False

    def buy_skills(self, skill_list: list[str]) -> bool:
        """Main skill buying flow"""
        self.found_skill = False

        for i in range(10):  # Max scroll attempts
            sleep(0.5)
            screen = self.interaction.input.take_screenshot()

            if self._process_skill_page(screen, skill_list):
                return True

            self._scroll_skills()

        return self.found_skill

    def _process_skill_page(self, screen, skill_list: list[str]) -> bool:
        """Process current page of skills"""
        buy_skill_icons = self.interaction.recognizer.match_template(
            template_path=assets_repository.get_icon("buy_skill"), screen=screen
        )

        if not buy_skill_icons:
            return False

        for x, y, w, h in buy_skill_icons:
            skill_text = self._extract_skill_text(screen, x, y, w, h)

            if self.matcher.is_skill_match(skill_text, skill_list):
                if self._can_buy_skill((x, y, w, h), screen):
                    self._buy_skill_at_position(x, y, skill_text)
                else:
                    info(f"{skill_text} found but not enough skill points.")

        return False

    def _extract_skill_text(self, screen, x: int, y: int, w: int, h: int) -> str:
        """Extract skill text from skill icon position"""
        region = (x - 420, y - 40, 295, h + 2)
        cropped = crop_screen(screen, region)
        return self.ocr.extract_text(cropped)

    def _can_buy_skill(self, button_region, screen) -> bool:
        """Check if skill can be bought (button active)"""
        return self.interaction.recognizer.is_btn_active(
            button_region, threshold=100, screen=screen
        )

    def _buy_skill_at_position(self, x: int, y: int, skill_text):
        """Buy skill at specific position"""
        self.interaction.click_coordinates(x + 5, y + 5)
        info(f"Buying {skill_text}")
        self.found_skill = True

    def _scroll_skills(self):
        """Scroll skill list"""
        self.interaction.swipe_for_scroll(distance=400, duration=700)
