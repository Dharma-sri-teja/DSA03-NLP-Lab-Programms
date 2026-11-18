"""Parse a sentence using a probabilistic context-free grammar (PCFG)."""

import nltk


GRAMMAR = nltk.PCFG.fromstring(
    """
    S -> NP VP [1.0]
    NP -> Det N [0.7] | Name [0.3]
    VP -> V NP [0.6] | V [0.4]
    Det -> 'the' [0.6] | 'a' [0.4]
    N -> 'cat' [0.5] | 'mouse' [0.5]
    Name -> 'Alice' [1.0]
    V -> 'sees' [0.6] | 'sleeps' [0.4]
    """
)


def parse_sentence(sentence):
    parser = nltk.ViterbiParser(GRAMMAR)
    return list(parser.parse(sentence.split()))


if __name__ == "__main__":
    parses = parse_sentence("Alice sees the mouse")
    if parses:
        print(max(parses, key=lambda tree: tree.prob()))
    else:
        print("No parse found.")
