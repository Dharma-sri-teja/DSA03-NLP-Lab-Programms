"""A tiny transformation-based POS tagger with hand-written correction rules."""

import re


def initial_tag(word):
    lower = word.lower()
    if lower in {"the", "a", "an"}:
        return "DET"
    if lower in {"is", "am", "are", "was", "were"}:
        return "VERB"
    if lower.endswith("ly"):
        return "ADV"
    if lower.endswith("ing"):
        return "VERB"
    if lower.endswith("s"):
        return "NOUN_PL"
    return "NOUN"


def transformation_tag(tokens):
    tagged = [(word, initial_tag(word)) for word in tokens]

    # Transform an ambiguous word into a verb when it follows a determiner + noun.
    for index in range(2, len(tagged)):
        word, tag = tagged[index]
        if tag in {"NOUN", "NOUN_PL"} and tagged[index - 1][1] in {"NOUN", "NOUN_PL"}:
            if tagged[index - 2][1] == "DET":
                tagged[index] = (word, "VERB")

    # A word after a form of "be" is tagged as a verb in this simple example.
    for index in range(1, len(tagged)):
        if tagged[index - 1][1] == "VERB" and tagged[index][1] == "NOUN":
            tagged[index] = (tagged[index][0], "VERB")

    return tagged


if __name__ == "__main__":
    words = re.findall(r"\w+", "The dogs chase cats")
    print(transformation_tag(words))
