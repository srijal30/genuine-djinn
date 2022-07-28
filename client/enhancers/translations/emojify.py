import emoji
import spacy

EMOJI_NAMES = [value["en"].strip(":").casefold() for value in emoji.EMOJI_DATA.values()]


def emojify(doc: spacy.tokens.doc.Doc) -> str:
    """Replace matching words with emojis."""
    emojified_message = ""
    for token in doc:
        phrase = token.text.casefold()
        if phrase in EMOJI_NAMES:
            emojified_message += emoji.emojize(f":{phrase}:")
        else:
            emojified_message += token.text
        emojified_message += token.whitespace_
    return emojified_message
