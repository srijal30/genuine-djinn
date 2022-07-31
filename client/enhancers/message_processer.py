import random
import re
import string
from collections import defaultdict
from pathlib import Path
from typing import Dict

import spacy
from spacy.matcher import Matcher

from .translations import boomhauer, emojify, owoify, pig_latin


class AutoTranslater:
    """Use natural language processing to analyze the message and obscure the text."""

    def __init__(self):
        # Create the nlp object using a small English pipeline trained on written
        # web text, like blogs, news, and comments.
        self.nlp: spacy.Language = spacy.load("en_core_web_sm")

        # Initialize the matcher with the shared vocab
        self.matcher: spacy.matcher.Matcher = Matcher(self.nlp.vocab)

        # Initialize a dictionary of messages to their processed texts
        self.messages: Dict[int, spacy.tokens.doc.Doc] = {}
        self.translated_messages: Dict[int, Dict[str, str]] = defaultdict(dict)

    def add_new_message(self, message: str):
        """Add a new message to the NLP processer."""
        doc: spacy.tokens.doc.Doc = self.nlp(message)
        message_hash = hash(message)
        self.messages[message_hash] = doc
        self.auto_translate(doc, message, message_hash)

    def auto_translate(self, doc: spacy.tokens.doc.Doc, message: str, message_hash: int):
        """Translate message."""
        self.translated_messages[message_hash][
            boomhauer.__name__
        ] = boomhauer.boomhauer(doc)
        self.translated_messages[message_hash][emojify.__name__] = emojify.emojify(doc)
        self.translated_messages[message_hash][owoify.__name__] = owoify.owoify(
            self.nlp, doc
        )
        self.translated_messages[message_hash][
            pig_latin.__name__
        ] = pig_latin.pig_latin(doc)

    def auto_translate_to_boomhauer(self, message: str):
        """Translate to Boomhauer."""
        doc: spacy.tokens.doc.Doc = self.nlp(message)
        return boomhauer.boomhauer(doc)

    def auto_translate_to_emojify(self, message: str):
        """Translate to Boomhauer."""
        doc: spacy.tokens.doc.Doc = self.nlp(message)
        return emojify.emojify(doc)

    def auto_translate_to_owoify(self, message: str):
        """Translate to Boomhauer."""
        doc: spacy.tokens.doc.Doc = self.nlp(message)
        return owoify.owoify(self.nlp, doc)

    def auto_translate_to_pig_latin(self, message: str):
        """Translate to Boomhauer."""
        doc: spacy.tokens.doc.Doc = self.nlp(message)
        return pig_latin.pig_latin(doc)


class AutoCorrecter:
    """Use natural language processing to analyze the message and obscure the text."""

    def __init__(self):
        # Create the nlp object using a small English pipeline trained on written
        # web text, like blogs, news, and comments.
        self.nlp: spacy.Language = spacy.load("en_core_web_sm")

        # Merge named entities into a single token.
        self.nlp.add_pipe("merge_entities")

    def autocorrect_string(self, message: str) -> str:
        """Autocorrect message by manipulating the string."""
        obscuring_methods = [
            self.lowercase,
            self.uppercase,
            self.capital_case,
            self.alternating_case,
            self.inverse_case,
            self.reverse,

            # Need markdown support

            # self.bold,
            # self.italics,
            # self.bold_and_italics,
            # self.strikethrough,
            # self.spoiler,

            self.stutter,
            self.confused_screaming,
            # self.reverse_smiley,
            self.censor,
            # self.random_letter,
        ]
        random_obscuring_method = random.choice(obscuring_methods)
        return random_obscuring_method(message)

    def autocorrect_entities(self, message: str) -> str:
        """Autocorrect message by replacing entities."""
        doc: spacy.tokens.doc.Doc = self.nlp(message)
        token_list = [token.text for token in doc]

        # Replace with entities labels for now.
        for ent in doc.ents:
            # print(ent.text, ent.start, ent.end, ent.label_, spacy.explain(ent.label_))
            # token_list[ent.start: ent.end] = [f"\u007b{ent.label_}\u007d"]
            random_entity = self._get_random_entity(ent.label_, ent.text)
            token_list[ent.start: ent.end] = [random_entity]

        autocorrected_message = ""
        for i in range(len(token_list)):
            autocorrected_message += token_list[i] + doc[i].whitespace_
        return autocorrected_message

    def _get_random_line(self, entity_label: str):
        """Get a random line from the entity file."""
        file_path = (
            Path(__file__).parent / "word-lists" / f"{entity_label.lower()}s.txt"
        )
        all_lines = open(file_path).read().splitlines()
        line = random.choice(all_lines)
        return line

    def _get_random_entity(self, entity_label: str, entity_text: str) -> str:
        """Get a random entity in the same category."""
        entity_list = [
            "EVENT",
            "FAC",
            "GPE",
            "LANGAUGE",
            "LOC",
            "NORP",
            "ORG",
            "PERSON",
            "PRODUCT",
            "WORK_OF_ART",
        ]
        if entity_label in entity_list:
            return self._get_random_line(entity_label)
        return entity_text

    def lowercase(self, message: str) -> str:
        """Make message all lowercase."""
        return message.lower()

    def uppercase(self, message: str) -> str:
        """Make message all uppercase."""
        return message.upper()

    def capital_case(self, message: str) -> str:
        """Capitalize every word in message."""
        return message.title()

    def alternating_case(self, message: str) -> str:
        """Alternate case in message. This mimics the mocking Spongebob meme text."""
        mocking_message = "".join(
            char.lower() if index % 2 else char.upper()
            for index, char in enumerate(message)
        )
        return mocking_message

    def inverse_case(self, message: str) -> str:
        """Inverse cases in message."""
        inverse_case_message = "".join(
            letter.lower() if letter.isupper() else letter.upper() for letter in message
        )
        return inverse_case_message

    def reverse(self, message: str) -> str:
        """Reverse the order of the letters in the message."""
        return message[::-1]

    def bold(self, message: str) -> str:
        """Make the message bold."""
        return f"**{message}**"

    def italics(self, message: str) -> str:
        """Make the message into italics."""
        return f"*{message}*"

    def bold_and_italics(self, message: str) -> str:
        """Make the message bold and italics."""
        return f"***{message}***"

    def strikethrough(self, message: str) -> str:
        """Strikethrough the message."""
        return f"~~{message}~~"

    def spoiler(self, message: str) -> str:
        """Hide the message behind spoiler tags."""
        return f"||{message}||"

    def stutter(self, message: str) -> str:
        """Stutter the message: Repeat the first letter of every word."""
        stuttering_message = " ".join(
            f"{word[0]}-{word.lower()}" for word in message.split()
        )
        return stuttering_message

    def confused_screaming(self, message: str) -> str:
        """Scream out the message with every vowel replaced with 'E'."""
        confused_screaming_message = (
            re.sub("[AIOU]", "E", message.upper()).rstrip(string.punctuation) + "?!"
        )
        return confused_screaming_message

    def reverse_smiley(self, message: str) -> str:
        """Turn that frown upside down... or a smile downside up."""
        smileys = {":)": ":(", ":(": ":)", "(:": "):", "):": "(:", "🙂": "🙁", "🙁": "🙂"}
        reversed_smiley_message = " ".join(
            smileys.get(word, word) if word in smileys.keys() else word
            for word in message.split()
        )
        return reversed_smiley_message

    def censor(self, message: str) -> str:
        """Censor words while only showing the first letter."""
        censored_message = " ".join(
            "".join(
                word[i]
                if i == 0
                else "#"
                if word[i] not in string.punctuation
                else word[i]
                for i in range(len(word))
            )
            for word in message.split()
        )
        return censored_message

    def random_letter(self, message: str) -> str:
        """Change a random character in the message to a random letter."""
        index = random.choice(range(len(message)))
        replacement = random.choice(string.ascii_letters)
        random_letter_message = message[:index] + replacement + message[index + 1:]
        return random_letter_message
