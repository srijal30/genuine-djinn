from typing import Dict, List


class MatchPattern:
    """Class for keeping track of a match pattern."""

    def __init__(self, name: str, pattern: List[Dict], replacement: str):
        self.name = name
        self.pattern = pattern
        self.replacement = replacement
