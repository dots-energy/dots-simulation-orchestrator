import re


class StringHelpers:
    @staticmethod
    def sanitize_string(s: str) -> str:
        s = s.lower()
        s = re.sub(r"[^a-z0-9- ]", "", s)
        s = re.sub(r"[^a-z0-9]+$", "", s)
        s = s.replace(" ", "-")
        return s


class ListHelpers:
    @staticmethod
    def flatten_list_of_lists(list_of_lists: list[list]) -> list:
        return [item for sublist in list_of_lists for item in sublist]
