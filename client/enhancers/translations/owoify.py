import spacy
from spacy.matcher import Matcher

from ..match_pattern import MatchPattern


def owoify(nlp: spacy.Language, doc: spacy.tokens.doc.Doc) -> str:
    """Make message cuter."""
    # Create patterns to find in the message.
    # Match to lemma "have". Lemma is the base form of a word.
    # (e.g., the lemma of "having" is "have")
    have_pattern = MatchPattern(
        name="HAVE_PATTERN", pattern=[{"LEMMA": "have"}], replacement="haz"
    )
    # Match case-insensitive mentions of "you"
    you_pattern = MatchPattern(
        name="YOU_PATTERN", pattern=[{"LOWER": "you"}], replacement="uu"
    )
    # Match case-insensitive mentions of "the"
    the_pattern = MatchPattern(
        name="THE_PATTERN", pattern=[{"LOWER": "the"}], replacement="da"
    )
    patterns = [have_pattern, you_pattern, the_pattern]

    # Initialize the matcher with the shared vocab
    matcher: spacy.matcher.Matcher = Matcher(nlp.vocab)

    # Add the patterns to the matcher
    for pattern in patterns:
        matcher.add(pattern.name, [pattern.pattern])

    # Call the matcher on the doc
    matches = matcher(doc)

    pattern_names = {pattern.name: pattern.replacement for pattern in patterns}
    text_list = [token.text for token in doc]

    # Iterate over the matches
    for match_id, start, end in matches:
        """
        match_id: hash value of the pattern name
        start: start index of matched span
        end: end index of matched span
        """
        # Get the string id which is the pattern name
        string_id = nlp.vocab.strings[match_id]

        # Overwrite pattern matches with replacements
        text_list[start:end] = [pattern_names.get(string_id)]

    # Owoify the message, replacing where needed and preserving whitespaces
    owoified_message = "".join(
        text.lower().replace("l", "w").replace("r", "w") + doc[index].whitespace_
        for index, text in enumerate(text_list)
    )

    return owoified_message
