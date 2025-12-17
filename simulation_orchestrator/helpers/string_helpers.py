import re


class StringHelpers:
    @staticmethod
    def sanitize_string(s: str) -> str:
        s = s.lower()
        s = re.sub(r"[^a-z0-9- ]", "", s)
        s = re.sub(r"[^a-z0-9]+$", "", s)
        s = s.replace(" ", "-")
        return s
