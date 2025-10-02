# core/skill/skill_matcher.py
import Levenshtein

from utils.log import debug


class SkillMatcher:
    def __init__(self, threshold: float = 0.8):
        self.threshold = threshold

    def is_skill_match(self, text: str, skill_list: list[str]) -> bool:
        """Check if text matches any skill in the list"""
        if not text or not skill_list:
            return False

        for skill in skill_list:
            similarity = Levenshtein.ratio(text.lower(), skill.lower())
            debug(f"{text} has {similarity * 100:.2f}% similarity with {skill}")

            if similarity >= self.threshold:
                return True
        return False

    def find_best_match(self, text: str, skill_list: list[str]) -> tuple[str, float]:
        """Find the best matching skill and similarity score"""
        if not text or not skill_list:
            return "", 0.0

        best_match = ""
        best_similarity = 0.0

        for skill in skill_list:
            similarity = Levenshtein.ratio(text.lower(), skill.lower())
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = skill

        return best_match, best_similarity
