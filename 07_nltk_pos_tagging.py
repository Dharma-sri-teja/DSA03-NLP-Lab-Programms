"""Part-of-speech tagging with NLTK's pretrained English tagger."""

import nltk


def tag_text(text):
    tokens = nltk.word_tokenize(text)
    return nltk.pos_tag(tokens)


if __name__ == "__main__":
    sample = "The quick brown fox jumps over the lazy dog."
    try:
        for word, tag in tag_text(sample):
            print(f"{word:12} {tag}")
    except LookupError as error:
        print("NLTK data is missing. Install the required tokenizer/tagger data:")
        print('  python -m nltk.downloader punkt punkt_tab averaged_perceptron_tagger_eng')
        print(error)
