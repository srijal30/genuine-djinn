import random
import string


def obscure_message(message: str) -> str:
    """Basic message obscuring"""
    index = random.choice(range(len(message)))
    replacement = random.choice(string.ascii_letters)
    obscured_message = message[:index] + replacement + message[index + 1:]
    return obscured_message
