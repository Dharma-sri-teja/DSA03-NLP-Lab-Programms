"""Rank documents for a query using TF-IDF and cosine similarity."""

import math
import re
from collections import Counter


def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


def rank_documents(documents, query):
    tokenized_documents = [tokenize(document) for document in documents]
    document_count = len(documents)
    if document_count == 0:
        return []

    document_frequencies = Counter()
    for tokens in tokenized_documents:
        document_frequencies.update(set(tokens))

    def vector(tokens):
        counts = Counter(tokens)
        return {
            term: (1 + math.log(count))
            * (math.log((document_count + 1) / (document_frequencies[term] + 1)) + 1)
            for term, count in counts.items()
        }

    query_vector = vector(tokenize(query))
    scores = []
    for index, tokens in enumerate(tokenized_documents):
        document_vector = vector(tokens)
        dot_product = sum(
            weight * document_vector.get(term, 0.0)
            for term, weight in query_vector.items()
        )
        query_norm = math.sqrt(sum(weight * weight for weight in query_vector.values()))
        document_norm = math.sqrt(
            sum(weight * weight for weight in document_vector.values())
        )
        score = dot_product / (query_norm * document_norm) if query_norm and document_norm else 0.0
        scores.append((index, score, documents[index]))

    return sorted(scores, key=lambda item: item[1], reverse=True)


if __name__ == "__main__":
    documents = [
        "Natural language processing helps computers understand text.",
        "Information retrieval finds relevant documents from a collection.",
        "Language models generate text and predict words.",
    ]
    for index, score, document in rank_documents(documents, "language text"):
        print(f"{score:.3f}  Document {index + 1}: {document}")
