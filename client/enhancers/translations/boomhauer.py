from string import punctuation

import spacy

from ..word_types import get_nouns


def boomhauer(doc: spacy.tokens.doc.Doc) -> str:
    """
    Talk like Boomhauer, a fictional character in the animated series King of the Hill.

    Begin every line with 'I'll tell you what'. Before every noun, add 'dang ol'. After
    every sentence, end with ', man'.
    """
    boomhauer_message = ""
    nouns = get_nouns(doc)
    for token in doc:
        # Add "dang ol" before every noun.
        if token.text in nouns:
            boomhauer_message += (
                f"{'D' if len(boomhauer_message) < 2 or boomhauer_message[-2]== '.' else 'd'}ang ol {token.text}"
            )
        # Add ", man" after every sentence.
        elif token.text in punctuation:
            boomhauer_message += ", man."
        else:
            boomhauer_message += token.text
        boomhauer_message += token.whitespace_

    complete_boomhauer_message = f"I'll tell you what, man. {boomhauer_message}"
    return complete_boomhauer_message
