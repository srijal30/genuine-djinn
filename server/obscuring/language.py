from typing import List

import spacy

nlp: spacy.Language = spacy.load("en_core_web_sm")


def get_tokens(word_type: str, sentence: str) -> List[str]:
    """Returns tokens of desired word type in a sentence."""
    result: List[str] = []
    tokens: spacy.tokens.doc.Doc = nlp(sentence)
    for token in tokens:
        if token.pos_ == word_type:
            result.append(token.text)
    return result


def get_verbs(sentence: str) -> List[str]:
    """Returns list of verbs in a sentence."""
    return get_tokens("VERB", sentence)


def get_nouns(sentence: str) -> List[str]:
    """Returns list of nouns in a sentence."""
    return get_tokens("NOUN", sentence)
