import base64
import random
import string


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
    """Encode the message into binary."""
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


ciphers = [
    rot13,
    random_shift,
    opposite_alphabetical_substitution,
    encode_integer,
    encode_binary,
    encode_base16,
    encode_base32,
    encode_base64,
    encode_a85,
]

cipher_weights = {
    rot13.__name__: 4,
    random_shift.__name__: 1,
    opposite_alphabetical_substitution.__name__: 1,
    encode_integer.__name__: 1,
    encode_binary.__name__: 1,
    encode_base16.__name__: 1,
    encode_base32.__name__: 1,
    encode_base64.__name__: 1,
    encode_a85.__name__: 1,
}


def random_cipher(message: str) -> str:
    """Encode a message using a random cipher based on probability weights."""
    cipher = random.choices(ciphers, [*cipher_weights.values()])[0]

    # Reduce weight of chosen cipher method.
    cipher_weights[cipher.__name__] -= 1

    return cipher(message)
