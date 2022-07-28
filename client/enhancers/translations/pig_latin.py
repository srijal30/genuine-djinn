import spacy


def pig_latin(nlp: spacy.Language, doc: spacy.tokens.doc.Doc) -> str:
    """Translate the message into pig latin."""
    vowels = "aeiou"
    pig_latin_message = ""
    for token in doc:
        if any(vowel in token.text for vowel in vowels):
            first_vowel = next(
                i for i in range(len(token.text)) if token.text[i].casefold() in vowels
            )
            token_start = token.text[first_vowel:]
            token_end = token.text[:first_vowel]
            new_text = (
                # Make first letter uppercase if it was originally uppercase.
                f"{token_start[0].upper() if token.text[0].isupper() else token_start[0]}"
                # Add "ay" at the end of the word.
                f"{token_start[1:]}{token_end.lower()}{'y' * (token.text[0] in vowels)}ay"
            )
        else:
            new_text = token.text
        pig_latin_message += new_text + token.whitespace_
    return pig_latin_message
