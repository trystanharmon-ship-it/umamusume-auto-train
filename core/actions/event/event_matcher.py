import Levenshtein
import re


class EventMatcher:
    def __init__(self):
        pass

    def find_best_match(self, text: str, event_list: list[dict]) -> tuple[str, float]:
        """Find the best matching skill and similarity score"""
        if not text or not event_list:
            return "", 0.0

        best_match = ""
        best_similarity = 0.0

        for event in event_list:
            event_name = event["event_name"]
            clean_text = re.sub(
                r"\s*\((?!Year 2\))[^\)]*\)", "", event_name
            ).strip()  # remove parentheses
            clean_text = re.sub(r"[^\x00-\x7F]", "", clean_text)  # remove non-ASCII
            similarity = Levenshtein.ratio(text.lower(), clean_text.lower())
            if similarity > best_similarity:
                best_similarity = similarity
                best_match = event_name

        return best_match, best_similarity
