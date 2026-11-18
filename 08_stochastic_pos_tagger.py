"""A small stochastic POS tagger using a first-order HMM and Viterbi decoding."""

import math
import re
from collections import Counter, defaultdict


TRAINING_SENTENCES = [
    [("the", "DET"), ("cat", "NOUN"), ("sleeps", "VERB")],
    [("a", "DET"), ("dog", "NOUN"), ("runs", "VERB")],
    [("the", "DET"), ("dog", "NOUN"), ("sees", "VERB"), ("a", "DET"), ("cat", "NOUN")],
    [("a", "DET"), ("cat", "NOUN"), ("runs", "VERB")],
]


class HMMTagger:
    def __init__(self, tagged_sentences):
        self.tags = set()
        self.emissions = defaultdict(Counter)
        self.transitions = defaultdict(Counter)
        self.tag_counts = Counter()
        self.vocabulary = set()

        for sentence in tagged_sentences:
            previous = "<START>"
            for word, tag in sentence:
                word = word.lower()
                self.tags.add(tag)
                self.vocabulary.add(word)
                self.emissions[tag][word] += 1
                self.tag_counts[tag] += 1
                self.transitions[previous][tag] += 1
                previous = tag
            self.transitions[previous]["<END>"] += 1

    def _emission_log_probability(self, word, tag):
        word = word.lower()
        # Add-one smoothing permits words absent from this tiny training corpus.
        numerator = self.emissions[tag][word] + 1
        denominator = self.tag_counts[tag] + len(self.vocabulary) + 1
        return math.log(numerator / denominator)

    def tag(self, words):
        if not words:
            return []

        states = {"<START>": (0.0, [])}
        for word in words:
            next_states = {}
            for previous, (score, path) in states.items():
                total = sum(self.transitions[previous].values())
                for tag in self.tags:
                    count = self.transitions[previous][tag]
                    transition_probability = (count + 1) / (total + len(self.tags) + 1)
                    candidate = (
                        score
                        + math.log(transition_probability)
                        + self._emission_log_probability(word, tag),
                        path + [tag],
                    )
                    if tag not in next_states or candidate[0] > next_states[tag][0]:
                        next_states[tag] = candidate
            states = next_states

        best_score, best_path = max(states.values(), key=lambda item: item[0])
        del best_score
        return list(zip(words, best_path))


if __name__ == "__main__":
    tagger = HMMTagger(TRAINING_SENTENCES)
    sentence = re.findall(r"\w+", "The cat runs.")
    print(tagger.tag(sentence))
