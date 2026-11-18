"""Earley parsing using NLTK's chart parser."""

import nltk


GRAMMAR = nltk.CFG.fromstring(
    """
    S -> NP VP
    NP -> Det N
    VP -> V NP | V
    Det -> 'the' | 'a'
    N -> 'cat' | 'dog' | 'mouse'
    V -> 'sees' | 'likes' | 'sleeps'
    """
)


def parse_sentence(sentence):
    parser = nltk.EarleyChartParser(GRAMMAR)
    return list(parser.parse(sentence.lower().split()))


if __name__ == "__main__":
    parses = parse_sentence("the cat sees a mouse")
    if parses:
        for tree in parses:
            print(tree)
    else:
        print("No parse found.")
