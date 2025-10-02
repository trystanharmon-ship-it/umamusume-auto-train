# core/actions/base/navigation.py
from .interaction import Interaction

from utils import assets_repository


class Navigation:
    def __init__(self, interaction: Interaction):
        self.interaction = interaction

    def go_to_training(self):
        """Navigate to training"""
        return self.interaction.click_element(
            assets_repository.get_button("training_btn")
        )

    def go_back(self, text: str = ""):
        """Navigate to lobby career"""
        return self.interaction.click_element(
            assets_repository.get_button("back_btn"), text=text
        )

    def go_to_race(self):
        """Navigate to race list"""
        return self.interaction.click_element(assets_repository.get_button("races_btn"))

    def go_to_skills(self):
        """Navigate to skill menu"""
        return self.interaction.click_element(
            assets_repository.get_button("skills_btn")
        )

    def do_rest(self, is_summer):
        """Perform rest"""
        if is_summer:
            return self.interaction.click_element(
                assets_repository.get_button("rest_summer_btn")
            )
        else:
            return self.interaction.click_element(
                assets_repository.get_button("rest_btn")
            )

    def do_recreation(self, is_summer):
        """Perform recreation"""
        if is_summer:
            return self.interaction.click_element(
                assets_repository.get_button("rest_summer_btn")
            )
        else:
            return self.interaction.click_element(
                assets_repository.get_button("recreation_btn")
            )
