"""Rule-based POS tagging using regular-expression patterns."""

import re


PATTERNS = [
    (r".*ing$", "VBG"),
    (r".*ed$", "VBD"),
    (r".*ly$", "RB"),
    (r".*ous$", "JJ"),
    (r".*s$", "NNS"),
    (r"^(the|a|an)$", "DT"),
    (r"^(and|or|but)$", "CC"),
    (r"^(is|am|are|was|were|be|been)$", "VB"),
    (r".*", "NN"),
]


def tag_text(text):
    tokens = re.findall(r"\w+|[^\w\s]", text)
    tagged = []
    for token in tokens:
        lower = token.lower()
        tag = next(tag for pattern, tag in PATTERNS if re.fullmatch(pattern, lower))
        tagged.append((token, tag))
    return tagged


if __name__ == "__main__":
    print(tag_text("The birds are flying quickly."))
