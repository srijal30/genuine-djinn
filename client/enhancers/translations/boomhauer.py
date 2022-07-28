import re
import string

from word_types import get_nouns


def boomhauer(doc, message: str) -> str:
    """
    Talk like Boomhauer, a fictional character in the animated series King of the Hill.

    Begin every line with 'I'll tell you what'. Before every noun, add 'dang ol'. After
    every sentence, end with ', man'.
    """
    modified_message_list = []
    nouns = get_nouns(doc)
    for word in message.split():
        token = word.strip(string.punctuation)
        new_expression = word

        # Add "dang ol" before every noun.
        if token in nouns:
            new_expression = word.rstrip(string.punctuation).replace(
                token, f"dang ol {word}"
            )

        # Add ", man" after every sentence.
        if word[-1] in string.punctuation:
            new_expression = re.sub(f"[{string.punctuation}]", ", man.", new_expression)

        modified_message_list.append(new_expression)

    boomhauer_message = " ".join(modified_message_list)
    complete_boomhauer_message = (
        f"I'll tell you what man, {boomhauer_message[0].lower()}{boomhauer_message[1:]}"
    )
    return complete_boomhauer_message
