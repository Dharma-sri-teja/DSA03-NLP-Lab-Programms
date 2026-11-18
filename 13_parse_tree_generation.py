"""Generate and display a parse tree for a sentence using an NLTK CFG."""

import nltk


GRAMMAR = nltk.CFG.fromstring(
    """
    S -> NP VP
    NP -> Det N | Name
    VP -> V NP | V
    Det -> 'the' | 'a'
    N -> 'cat' | 'dog' | 'mouse'
    Name -> 'Alice' | 'Bob'
    V -> 'sees' | 'likes' | 'sleeps'
    """
)


def parse_sentence(sentence):
    parser = nltk.ChartParser(GRAMMAR)
    return list(parser.parse(sentence.split()))


if __name__ == "__main__":
    parses = parse_sentence("Alice sees the dog")
    if parses:
        parses[0].pretty_print()
    else:
        print("No parse found.")
