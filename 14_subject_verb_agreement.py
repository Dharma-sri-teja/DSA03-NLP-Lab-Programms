"""Check subject-verb number agreement with a simple CFG."""

import nltk


AGREEMENT_GRAMMAR = nltk.CFG.fromstring(
    """
    S -> NP_SG VP_SG | NP_PL VP_PL
    NP_SG -> Det_SG N_SG | Name
    NP_PL -> Det_PL N_PL
    VP_SG -> V_SG | V_SG NP
    VP_PL -> V_PL | V_PL NP
    NP -> Det_SG N_SG | Det_PL N_PL | Name
    Det_SG -> 'the' | 'a'
    Det_PL -> 'the'
    N_SG -> 'cat' | 'dog'
    N_PL -> 'cats' | 'dogs'
    Name -> 'alice' | 'bob'
    V_SG -> 'runs' | 'sleeps' | 'sees'
    V_PL -> 'run' | 'sleep' | 'see'
    """
)


def agrees(sentence):
    parser = nltk.ChartParser(AGREEMENT_GRAMMAR)
    return next(parser.parse(sentence.lower().split()), None) is not None


if __name__ == "__main__":
    for example in ("the cat runs", "the cats run", "the cats runs"):
        print(f"{example}: {'agrees' if agrees(example) else 'does not agree'}")
