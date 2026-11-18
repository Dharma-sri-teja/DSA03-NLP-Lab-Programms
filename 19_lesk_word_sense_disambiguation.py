"""Word sense disambiguation with NLTK's simplified Lesk algorithm."""

from nltk import word_tokenize
from nltk.wsd import lesk


def disambiguate(sentence, target_word):
    context = word_tokenize(sentence)
    return lesk(context, target_word.lower())


if __name__ == "__main__":
    sentence = "The fisherman sat on the bank of the river."
    try:
        result = disambiguate(sentence, "bank")
        if result is None:
            print("No WordNet sense was selected.")
        else:
            print(f"Sense: {result.name()}")
            print(f"Definition: {result.definition()}")
    except LookupError as error:
        print("Required NLTK tokenizer/WordNet data is missing. Install it with:")
        print("  python -m nltk.downloader punkt punkt_tab wordnet omw-1.4")
        print(error)
