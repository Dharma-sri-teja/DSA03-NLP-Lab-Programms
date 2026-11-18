"""Explore WordNet synsets, definitions, examples, and lemmas with NLTK."""

from nltk.corpus import wordnet as wn


def explore_word(word):
    synsets = wn.synsets(word)
    for synset in synsets:
        print(f"{synset.name()} ({synset.pos()}): {synset.definition()}")
        if synset.examples():
            print(f"  Example: {synset.examples()[0]}")
        print(f"  Lemmas: {', '.join(synset.lemma_names())}")
    return synsets


if __name__ == "__main__":
    try:
        explore_word("bank")
    except LookupError as error:
        print("NLTK WordNet data is missing. Install it with:")
        print("  python -m nltk.downloader wordnet omw-1.4")
        print(error)
