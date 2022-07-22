from typing import List

import spacy

nlp: spacy.Language = spacy.load("en_core_web_sm")


def get_verbs(sentence: str) -> List[str]:
    """Returns list of verbs in a sentence"""
    result: List[str] = []
    tokens: spacy.tokens.doc.Doc = nlp(sentence)
    for token in tokens:
        if token.pos_ == "VERB":
            result.append(token.text)
    return result
