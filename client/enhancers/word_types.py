from typing import List

from spacy.tokens.doc import Doc


def get_tokens(word_type: str, doc: Doc) -> List[str]:
    """Returns tokens of desired word type in a sentence."""
    result: List[str] = []
    for token in doc:
        if token.pos_ == word_type:
            result.append(token.text)
    return result


def get_verbs(doc: Doc) -> List[str]:
    """Returns list of verbs in a sentence."""
    return get_tokens("VERB", doc)


def get_nouns(doc: Doc) -> List[str]:
    """Returns list of nouns in a sentence."""
    return get_tokens("NOUN", doc)
