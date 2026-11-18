"""Generate a short sentence with a word-level bigram model."""

import random
from collections import defaultdict


def train_bigram_model(text):
    """Map each word to possible following words from the training text."""
    transitions = defaultdict(list)
    words = ["<START>"] + text.split() + ["<END>"]
    for current, following in zip(words, words[1:]):
        transitions[current].append(following)
    return transitions


def generate_text(model, max_words=20, seed=None):
    """Generate text by sampling a next word from observed transitions."""
    rng = random.Random(seed)
    current = "<START>"
    result = []
    for _ in range(max_words):
        choices = model.get(current)
        if not choices:
            break
        current = rng.choice(choices)
        if current == "<END>":
            break
        result.append(current)
    return " ".join(result)


if __name__ == "__main__":
    corpus = (
        "language models predict the next word. "
        "language models learn from text. "
        "text helps models predict words."
    )
    bigram_model = train_bigram_model(corpus)
    print(generate_text(bigram_model, seed=7))
