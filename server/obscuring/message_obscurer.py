import random
from typing import Dict, List

import spacy
from spacy.matcher import Matcher

# Create the nlp object using a small English pipeline trained on written web text, like blogs, news, and comments.
nlp: spacy.Language = spacy.load("en_core_web_sm")


class MessageObscurer:
    """Use natural language processing to analyze the message and obscure the text."""

    def __init__(self, message: str, intensity: int = 1):
        self.message = message
        self.message_history = [message]
        self.all_obscuring_methods = [self.owoify]
        self._intensity = self._clamp(
            intensity, min_value=0, max_value=len(self.all_obscuring_methods)
        )
        self.obscuring_methods_used: List[str] = []

        # Process a text with the nlp object
        self.doc: spacy.tokens.doc.Doc = nlp(message)

        # Obscure the message based on intensity
        for i in range(self._intensity):
            # Obscure the message using a random obscuring method
            self.random_obscuring()

    def __str__(self):
        return self.obscured_message

    def _clamp(self, num: int, min_value: int, max_value: int):
        """Clamp num between the minimum and maximum value (both inclusive)"""
        return max(min(num, max_value), min_value)

    def get_tokens(self, word_type: str) -> List[str]:
        """Returns tokens of desired word type in a sentence."""
        result: List[str] = []
        for token in self.doc:
            if token.pos_ == word_type:
                result.append(token.text)
        return result

    def get_verbs(self) -> List[str]:
        """Returns list of verbs in a sentence."""
        return self.get_tokens("VERB")

    def get_nouns(self) -> List[str]:
        """Returns list of nouns in a sentence."""
        return self.get_tokens("NOUN")

    def get_original_message(self) -> str:
        """Returns the original message."""
        return self.message_history[0]

    def random_obscuring(self):
        """Use a random obscuring function on the message."""
        # If all obscuring methods are already used, just return the
        # obscured message it has already
        if len(self.obscuring_methods_used) >= len(self.all_obscuring_methods):
            return self.obscured_message

        # Randomly choose an obscuring method for the message
        obscure = random.choice(self.all_obscuring_methods)
        while obscure in self.obscuring_methods_used:
            obscure = random.choice(self.all_obscuring_methods)

        # Save obscuring method to history
        self.obscuring_methods_used.append(obscure.__name__)
        self.obscured_message = obscure()
        self.message_history.append(self.obscured_message)

    @property
    def intensity(self):
        """Returns how many obscuring methods were used on the message."""
        return len(self.obscuring_methods_used)

    def decrease_intensity(self, times: int = 1):
        """Decrease obscuring intensity and rewind the message back to an older message in the history."""
        times = self._clamp(times, 1, len(self.message_history))
        self.obscured_message = self.message_history[-(times + 1)]

        # Don't decrease intensity if it's only the original message in the history.
        if len(self.message_history) > times:
            del self.message_history[-times:]
            del self.obscuring_methods_used[-times:]

    def increase_intensity(self, times: int = 1):
        """Increase obscuring intensity."""
        max_value = len(self.all_obscuring_methods) - len(self.obscuring_methods_used)
        times = self._clamp(times, min_value=1, max_value=max_value)
        for i in range(times):
            self.random_obscuring()

    def owoify(self) -> str:
        """Make message cuter."""
        # Create patterns to find in the message.
        # Match to lemma "have". Lemma is the base form of a word.
        # (e.g., the lemma of "having" is "have")
        have_pattern = MatchPattern(
            name="HAVE_PATTERN", pattern=[{"LEMMA": "have"}], replacement="haz"
        )
        # Match case-insensitive mentions of "you"
        you_pattern = MatchPattern(
            name="YOU_PATTERN", pattern=[{"LOWER": "you"}], replacement="uu"
        )
        # Match case-insensitive mentions of "the"
        the_pattern = MatchPattern(
            name="THE_PATTERN", pattern=[{"LOWER": "the"}], replacement="da"
        )
        patterns = [have_pattern, you_pattern, the_pattern]

        # Initialize the matcher with the shared vocab
        matcher: spacy.matcher.Matcher = Matcher(nlp.vocab)

        # Add the patterns to the matcher
        for pattern in patterns:
            matcher.add(pattern.name, [pattern.pattern])

        # Call the matcher on the doc
        matches = matcher(self.doc)

        pattern_names = {pattern.name: pattern.replacement for pattern in patterns}
        text_list = [token.text for token in self.doc]

        # Iterate over the matches
        for match_id, start, end in matches:
            """
            match_id: hash value of the pattern name
            start: start index of matched span
            end: end index of matched span
            """
            # Get the string id which is the pattern name
            string_id = nlp.vocab.strings[match_id]

            # Overwrite pattern matches with replacements
            text_list[start:end] = [pattern_names.get(string_id)]

        # Owoify the message, replacing where needed and preserving whitespaces
        owoified_message = "".join(
            text.lower().replace("l", "w").replace("r", "w")
            + self.doc[index].whitespace_
            for index, text in enumerate(text_list)
        )

        # Process and assign the new text with the nlp object
        self.doc = nlp(owoified_message)

        return owoified_message


class MatchPattern:
    """Match Pattern"""

    def __init__(self, name: str, pattern: List[Dict], replacement: str):
        self.name = name
        self.pattern = pattern
        self.replacement = replacement
