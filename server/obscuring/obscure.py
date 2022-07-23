import base64
import random
import re
import string
import unittest

import emoji
import language
import zalgolib


def lowercase(message: str) -> str:
    """Make message all lowercase."""
    return message.lower()


def uppercase(message: str) -> str:
    """Make message all uppercase."""
    return message.upper()


def capital_case(message: str) -> str:
    """Capitalize every word in message."""
    return message.title()


def alternating_case(message: str) -> str:
    """Alternate case in message. This mimics the mocking Spongebob meme text."""
    mocking_message = "".join(
        char.lower() if index % 2 else char.upper()
        for index, char in enumerate(message)
    )
    return mocking_message


def inverse_case(message: str) -> str:
    """Inverse cases in message."""
    inverse_case_message = "".join(
        letter.lower() if letter.isupper() else letter.upper() for letter in message
    )
    return inverse_case_message


def reverse(message: str) -> str:
    """Reverse the order of the letters in the message."""
    return message[::-1]


def bold(message: str) -> str:
    """Make the message bold."""
    return f"**{message}**"


def italics(message: str) -> str:
    """Make the message into italics."""
    return f"*{message}*"


def bold_and_italics(message: str) -> str:
    """Make the message bold and italics."""
    return f"***{message}***"


def strikethrough(message: str) -> str:
    """Strikethrough the message."""
    return f"~~{message}~~"


def spoiler(message: str) -> str:
    """Hide the message behind spoiler tags."""
    return f"||{message}||"


def random_letter(message: str) -> str:
    """Change a random character in the message to a random letter."""
    index = random.choice(range(len(message)))
    replacement = random.choice(string.ascii_letters)
    random_letter_message = message[:index] + replacement + message[index + 1:]
    return random_letter_message


def emojify(message: str) -> str:
    """Replace matching words with emojis."""
    emoji_names = [
        value["en"].strip(":").casefold() for value in emoji.EMOJI_DATA.values()
    ]
    emojified_message = []
    for word in message.split():
        token = word.strip(string.punctuation).casefold()
        if token in emoji_names:
            word = word.casefold().replace(token, f":{token}:")
            emojified_message.append(emoji.emojize(word))
        else:
            emojified_message.append(word)
    return " ".join(emojified_message)


def owoify(message: str) -> str:
    """Make message cuter."""
    owoified_message = "".join(
        "w" if char in ["l", "r"] else char for char in message.lower()
    )
    owoified_message = " ".join(
        "haz"
        if word in ["has", "have"]
        else "uu"
        if word == "you"
        else "da"
        if word == "the"
        else word
        for word in owoified_message.split()
    )
    return owoified_message + " UwU"


def censor(message: str) -> str:
    """Censor words while only showing the first letter."""
    censored_message = " ".join(
        "".join(
            word[i] if i == 0 else "#" if word[i] not in string.punctuation else word[i]
            for i in range(len(word))
        )
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
    confused_screaming_message = (
        re.sub("[AIOU]", "E", message.upper()).rstrip(string.punctuation) + "?!"
    )
    return confused_screaming_message


def make_love_not_war(message: str) -> str:
    """Replace 'hate' with 'love'."""
    love_message = " ".join(
        "LOVE" if word.casefold() == "hate" else word for word in message.split()
    )
    return love_message


def stutter(message: str) -> str:
    """Stutter the message: Repeat the first letter of every word."""
    stuttering_message = " ".join(
        f"{word[0]}-{word.lower()}" for word in message.split()
    )
    return stuttering_message


def pig_latin(message: str) -> str:
    """Translate the message into pig latin."""
    pig_latin_message = []
    for word in message.split():
        token = word.strip(string.punctuation)
        vowels = "aeiou"
        first_vowel = next(
            i for i in range(len(token)) if token[i].casefold() in vowels
        )
        token_start = token[first_vowel:]
        token_end = token[:first_vowel]
        pig_latinized_token = (
            # Make first letter uppercase if it was originally uppercase.
            f"{token_start[0].upper() if token_end[0].isupper() else token_start[0]}"
            # Add "ay" at the end of the word.
            f"{token_start[1:]}{token_end.lower()}ay"
        )
        word = word.replace(token, pig_latinized_token)
        pig_latin_message.append(word)
    return " ".join(pig_latin_message)


def rickroll(message: str) -> str:
    """Change every link to the Rickroll music video."""
    rickroll_link = "https://youtube.com/watch?v=dQw4w9WgXcQ"
    link_regex = r"(?:(?:https?)://)?[\w/\-?=%.]+\.[\w/\-&?=%.]+"
    rickroll_message = " ".join(
        rickroll_link if re.match(link_regex, word) else word
        for word in message.split()
    )
    return rickroll_message


def zalgo(message: str, intensity=2) -> str:
    """Make message look glitchy by adding diacritic marks."""
    return zalgolib.enzalgofy(message, intensity=intensity)


def boomhauer(message: str) -> str:
    """
    Talk like Boomhauer, a fictional character in the animated series King of the Hill.

    Begin every line with 'I'll tell you what'. Before every noun, add 'dang ol'. After
    every sentence, end with ', man'.
    """
    modified_message_list = []
    nouns = language.get_nouns(message)
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


def porky_pig(message: str) -> str:
    """Talk like Porky Pig from Looney Tunes."""
    nouns = language.get_nouns(message)
    porky_pig_message_list = []
    for word in message.split():
        if word.strip(string.punctuation) in nouns:
            vowel_index = next(
                i for i in range(len(word)) if word[i].casefold() in "aeiouy"
            )
            stutter = word[:vowel_index]
            if vowel_index == 1:
                stutter += "eh"
            new_expression = f"eh-{stutter}-{stutter.upper()}-eh-{word}"
            porky_pig_message_list.append(new_expression)
        else:
            porky_pig_message_list.append(word)
    return " ".join(porky_pig_message_list)


def caesar_cipher(message: str, shift: int) -> str:
    """Encode the message using the Caesar cipher with the desired shift count."""
    lowercase_alphabet = string.ascii_lowercase
    uppercase_alphabet = string.ascii_uppercase
    shifted_lowercase_alphabet = lowercase_alphabet[shift:] + lowercase_alphabet[:shift]
    shifted_uppercase_alphabet = uppercase_alphabet[shift:] + uppercase_alphabet[:shift]
    mapping = message.maketrans(
        lowercase_alphabet, shifted_lowercase_alphabet
    ) | message.maketrans(uppercase_alphabet, shifted_uppercase_alphabet)
    return message.translate(mapping)


def rot13(message: str) -> str:
    """Shift 13 positions in the alphabet."""
    return caesar_cipher(message, 13)


def random_shift(message: str) -> str:
    """Randomly shift the letters of the alphabet in the message."""
    random_shift = random.choice(range(23))
    return caesar_cipher(message, random_shift)


def opposite_alphabetical_substitution(message: str) -> str:
    """
    Replace plaintext alphabet with ciphertext alphabet.

    abcdefghijklmnopqrstuvwxyz => zyxwvutsrqponmlkjihgfedcba
    """
    lowercase_alphabet = string.ascii_lowercase
    uppercase_alphabet = string.ascii_uppercase
    shifted_lowercase_alphabet = lowercase_alphabet[::-1]
    shifted_uppercase_alphabet = uppercase_alphabet[::-1]
    mapping = message.maketrans(
        lowercase_alphabet, shifted_lowercase_alphabet
    ) | message.maketrans(uppercase_alphabet, shifted_uppercase_alphabet)
    return message.translate(mapping)


def encode_integer(message: str) -> str:
    """Encode the message into integers that represent the Unicode code point of each character."""
    return " ".join(map(str, map(ord, message)))


def encode_binary(message: str) -> str:
    """Encode th emessage into binary."""
    binary_message = "".join(
        format(i, "08b") for i in bytearray(message, encoding="utf-8")
    )
    return binary_message


def encode_base16(message: str) -> str:
    """Encode the message to Base16."""
    base16_message = base64.b16encode(bytearray(message, "ascii")).decode()
    return base16_message


def encode_base32(message: str) -> str:
    """Encode the message to Base32."""
    base32_message = base64.b32encode(bytearray(message, "ascii")).decode()
    return base32_message


def encode_base64(message: str) -> str:
    """Encode the message to Base64."""
    base64_message = base64.b64encode(bytearray(message, "ascii")).decode()
    return base64_message


def encode_a85(message: str) -> str:
    """Encode the message to Ascii85."""
    a85_message = base64.a85encode(bytearray(message, "ascii")).decode()
    return a85_message


class TestMessageObscuring(unittest.TestCase):
    """Run unit tests on each message obscuring function."""

    def test_lowercase(self):  # noqa: D102
        self.assertEqual(lowercase("Hello, world!"), "hello, world!")

    def test_uppercase(self):  # noqa: D102
        self.assertEqual(uppercase("Hello, world!"), "HELLO, WORLD!")

    def test_capital_case(self):  # noqa: D102
        self.assertEqual(capital_case("Hello, world!"), "Hello, World!")

    def test_alternating_case(self):  # noqa: D102
        self.assertEqual(alternating_case("Hello, world!"), "HeLlO, wOrLd!")

    def test_inverse(self):  # noqa: D102
        self.assertEqual(inverse_case("Hello, world!"), "hELLO, WORLD!")

    def test_reverse(self):  # noqa: D102
        self.assertEqual(reverse("Hello, world!"), "!dlrow ,olleH")

    def test_bold(self):  # noqa: D102
        self.assertEqual(bold("Hello, world!"), "**Hello, world!**")

    def test_italics(self):  # noqa: D102
        self.assertEqual(italics("Hello, world!"), "*Hello, world!*")

    def test_bold_and_italics(self):  # noqa: D102
        self.assertEqual(bold_and_italics("Hello, world!"), "***Hello, world!***")

    def test_strikethrough(self):  # noqa: D102
        self.assertEqual(strikethrough("Hello, world!"), "~~Hello, world!~~")

    def test_spoiler(self):  # noqa: D102
        self.assertEqual(spoiler("Hello, world!"), "||Hello, world!||")

    def test_emojify(self):  # noqa: D102
        self.assertEqual(emojify("Hello, panda!"), "Hello, 🐼!")

    def test_owoify(self):  # noqa: D102
        self.assertEqual(
            owoify("Hello, do you have the time?"), "hewwo, do uu haz da time? UwU"
        )

    def test_censor(self):  # noqa: D102
        self.assertEqual(censor("Hello, world!"), "H####, w####!")

    def test_reverse_smiley(self):  # noqa: D102
        self.assertEqual(reverse_smiley("Hello, world :)"), "Hello, world :(")
        self.assertEqual(reverse_smiley("Yes 🙂 or no?"), "Yes 🙁 or no?")
        self.assertEqual(reverse_smiley(":( Goodbye, friend"), ":) Goodbye, friend")

    def test_confused_screaming(self):  # noqa: D102
        self.assertEqual(confused_screaming("Hello, world!"), "HELLE, WERLD?!")

    def test_make_love_not_war(self):  # noqa: D102
        self.assertEqual(make_love_not_war("I hate cats!"), "I LOVE cats!")

    def test_stutter(self):  # noqa: D102
        self.assertEqual(stutter("Hello, world!"), "H-hello, w-world!")

    def test_pig_latin(self):  # noqa: D102
        self.assertEqual(pig_latin("Hello, world!"), "Ellohay, orldway!")

    def test_rickroll(self):  # noqa: D102
        self.assertEqual(
            rickroll(
                "Hey, check out the python discord website! https://www.pythondiscord.com/"
            ),
            "Hey, check out the python discord website! https://youtube.com/watch?v=dQw4w9WgXcQ",
        )

    def test_boomhauer(self):  # noqa: D102
        self.assertEqual(
            boomhauer("My car is stuck!"),
            "I'll tell you what man, my dang ol car is stuck, man.",
        )
        self.assertEqual(
            boomhauer("That Y2K was a letdown."),
            "I'll tell you what man, that Y2K was a dang ol letdown, man.",
        )

    def test_porky_pig(self):  # noqa: D102
        self.assertEqual(
            porky_pig("Hello, world!"),
            "Hello, eh-weh-WEH-eh-world!",
        )
        self.assertEqual(
            porky_pig("The boy sat in the chair next to the desk."),
            "The eh-beh-BEH-eh-boy sat in the eh-ch-CH-eh-chair next to the eh-deh-DEH-eh-desk.",
        )

    def test_rot13(self):  # noqa: D102
        self.assertEqual(rot13("Hello, world!"), "Uryyb, jbeyq!")

    def test_opposite_alphabetical_substituion(self):  # noqa: D102
        self.assertEqual(
            opposite_alphabetical_substitution("Hello, world!"), "Svool, dliow!"
        )

    def test_integer(self):  # noqa: D102
        self.assertEqual(
            encode_integer("Hello, world!"),
            "72 101 108 108 111 44 32 119 111 114 108 100 33",
        )

    def test_encode_binary(self):  # noqa: D102
        self.assertEqual(
            encode_binary("Hello, world!"),
            "01001000011001010110110001101100011011110010110000100000011101110110111101110010011011000110010000100001",
        )

    def test_encode_base16(self):  # noqa: D102
        self.assertEqual(encode_base16("Hello, world!"), "48656C6C6F2C20776F726C6421")

    def test_encode_base32(self):  # noqa: D102
        self.assertEqual(encode_base32("Hello, world!"), "JBSWY3DPFQQHO33SNRSCC===")

    def test_encode_base64(self):  # noqa: D102
        self.assertEqual(encode_base64("Hello, world!"), "SGVsbG8sIHdvcmxkIQ==")

    def test_encode_a85(self):  # noqa: D102
        self.assertEqual(encode_a85("Hello, world!"), "87cURD_*#TDfTZ)+T")


if __name__ == "__main__":
    unittest.main()
