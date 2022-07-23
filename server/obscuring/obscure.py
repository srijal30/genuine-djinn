import random
import re
import string

import emoji


def random_letter(message: str) -> str:
    """Change a random character in the message to a random letter."""
    index = random.choice(range(len(message)))
    replacement = random.choice(string.ascii_letters)
    random_letter_message = message[:index] + replacement + message[index + 1:]
    return random_letter_message


def owoify(message: str) -> str:
    """Make message cuter."""
    owoified_message = "".join(
        "w" if char in ["l", "r"] else char.lower() for char in message
    )
    owoified_message = " ".join(
        "haz"
        if word in ["has", "have"]
        else "uu"
        if word == "you"
        else "da"
        if word == "the"
        else word
        for word in message.split()
    )
    ending = random.choice(["", "OwO", "UwU"])
    return owoified_message + f" {ending}"


def mocking_spongebob(message: str) -> str:
    """Add a mocking tone to message."""
    mocking_message = "".join(
        char.lower() if index % 2 else char.upper()
        for index, char in enumerate(message)
    )
    return mocking_message


def emojify(message: str) -> str:
    """Replace matching words with emojis."""
    emoji_names = [
        value["en"].strip(":").casefold() for value in emoji.EMOJI_DATA.values()
    ]
    emojified_message = " ".join(
        emoji.emojize(f":{word}:") if word.casefold() in emoji_names else word
        for word in message.split()
    )
    return emojified_message


def censor(message: str) -> str:
    """Randomly censor words while only showing the first letter."""
    censored_message = " ".join(
        f"{word[0]}{'#'*(len(word)-1)}" if random.random() >= 0.5 else word
        for word in message.split()
    )
    return censored_message


def reverse_smiley(message: str) -> str:
    """Turn that frown upside down... or a smile downside up."""
    smileys = {":)": ":(", ":(": ":)", "(:": "):", "):": "(:", "🙂": "🙁", "🙁": "🙂"}
    reversed_smiley_message = " ".join(
        smileys.get(word, word) if word in smileys.keys() else word
        for word in message.split()
    )
    return reversed_smiley_message


def confused_screaming(message: str) -> str:
    """Scream out the message with every vowel replaced with 'E'."""
    confused_screaming_message = re.sub("[AIOU]", "E", message.upper()) + "!"
    return confused_screaming_message


def make_love_not_war(message: str) -> str:
    """Replace 'hate' with 'love'."""
    if "hate" in message.casefold():
        love_message = message.casefold().replace("hate", "LOVE")
        return love_message
    return message
