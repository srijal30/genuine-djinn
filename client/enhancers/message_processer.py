from collections import defaultdict
from typing import Dict

import spacy
from spacy.matcher import Matcher
from translations.boomhauer import boomhauer
from translations.owoify import owoify
from translations.pig_latin import pig_latin


class MessageProcesser:
    """Use natural language processing to analyze the message and obscure the text."""

    def __init__(self):
        # Create the nlp object using a small English pipeline trained on written
        # web text, like blogs, news, and comments.
        self.nlp: spacy.Language = spacy.load("en_core_web_sm")

        # Initialize the matcher with the shared vocab
        self.matcher: spacy.matcher.Matcher = Matcher(self.nlp.vocab)

        # Initialize a dictionary of messages to their processed texts
        self.messages: Dict[int, spacy.tokens.doc.Doc] = {}
        self.translations: Dict[int, Dict[str, str]] = defaultdict(dict)

    def add_new_message(self, message: str):
        """Add a new message to the NLP processer."""
        doc: spacy.tokens.doc.Doc = self.nlp(message)
        message_hash = hash(message)
        self.messages[message_hash] = doc
        self.auto_translate(doc, message, message_hash)

    def auto_translate(self, doc, message: str, message_hash: int):
        """Translate message."""
        self.translations[message_hash][owoify.__name__] = owoify(self.nlp, doc)
        self.translations[message_hash][pig_latin.__name__] = pig_latin(doc)
        self.translations[message_hash][boomhauer.__name__] = boomhauer(doc, message)

    def autocorrect(self, message: str):
        """Autocorrect message."""
        ...
