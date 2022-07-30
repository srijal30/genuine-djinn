import random
from collections import defaultdict
from pathlib import Path
from typing import Dict

import spacy
from spacy.matcher import Matcher
from translations import boomhauer, emojify, owoify, pig_latin


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

    def auto_translate(self, doc, message: str, message_hash: int):
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


class AutoCorrecter:
    """Use natural language processing to analyze the message and obscure the text."""

    def __init__(self):
        # Create the nlp object using a small English pipeline trained on written
        # web text, like blogs, news, and comments.
        self.nlp: spacy.Language = spacy.load("en_core_web_sm")

        # Merge named entities into a single token.
        self.nlp.add_pipe("merge_entities")

    def autocorrect(self, message: str) -> str:
        """Autocorrect message."""
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
        file_path = (
            Path(__file__).parent / "word-lists" / f"{entity_label.lower()}s.txt"
        )
        all_lines = open(file_path).read().splitlines()
        line = random.choice(all_lines)
        return line

    def _get_random_entity(self, entity_label: str, entity_text: str) -> str:
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
