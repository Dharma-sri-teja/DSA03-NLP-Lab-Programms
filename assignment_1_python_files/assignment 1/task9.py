"""Task 9 - Porter stemming comparison and simple retrieval evaluation."""
try:
    from nltk.stem import PorterStemmer
    STEMMER = PorterStemmer()
    def porter(word): return STEMMER.stem(word.lower())
except ImportError:
    # Small fallback for a few assignment examples; install nltk for full Porter.
    def porter(word):
        w = word.lower()
        for suffix in ("ing", "ed", "es", "s"):
            if len(w) > len(suffix) + 2 and w.endswith(suffix):
                return w[:-len(suffix)]
        return w

def retrieve(records, query, stem=False):
    key = porter(query) if stem else query.lower()
    hits = []
    for index, record in enumerate(records):
        words = record.lower().split()
        if any((porter(w) if stem else w) == key for w in words):
            hits.append(index)
    return hits

def main():
    words = ["fracture", "fractured", "fractures", "hepatic", "hepatitis",
             "diagnose", "diagnosis", "took", "take"]
    for word in words:
        print(f"{word:12} -> {porter(word)}")
    records = ["fractured femur", "fracture clinic", "hepatic disease"]
    print("Exact fracture:", retrieve(records, "fracture"))
    print("Stemmed fracture:", retrieve(records, "fracture", stem=True))

if __name__ == "__main__":
    main()
