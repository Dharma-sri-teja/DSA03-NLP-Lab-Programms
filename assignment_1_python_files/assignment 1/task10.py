"""Task 10 - End-to-end miniature hospital-record normalisation and search pipeline."""
import re
from collections import defaultdict

ENTITY_PATTERNS = {
    "PID": re.compile(r"\bMRN-\d{4}-\d{6}\b", re.I),
    "DATE": re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b"),
    "BP": re.compile(r"\b\d{2,3}/\d{2,3}\s*mmHg\b", re.I),
    "DRUG": re.compile(r"\b(?:paracetamol|aspirin|ibuprofen|metformin)\s+\d+\s?mg\b", re.I),
}
TOKEN_RE = re.compile(r"[A-Za-z]+(?:[-'][A-Za-z]+)*|\d+(?:\.\d+)?|[^\w\s]")

IRREGULAR = {"took": "take", "taken": "take", "better": "good",
             "best": "good", "children": "child", "men": "man"}

def extract_entities(text):
    return [(kind, m.group()) for kind, pattern in ENTITY_PATTERNS.items()
            for m in pattern.finditer(text)]

def tokenise(text):
    return TOKEN_RE.findall(text)

def normalise_word(word):
    word = word.lower()
    if word in IRREGULAR:
        return IRREGULAR[word]
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("ing") and len(word) > 5:
        return word[:-3]
    if word.endswith("ed") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and len(word) > 3:
        return word[:-1]
    return word

def build_index(records):
    index = defaultdict(set)
    for record_id, text in enumerate(records):
        for token in tokenise(text):
            if token.isalpha():
                index[normalise_word(token)].add(record_id)
    return index

def search(index, query):
    return sorted(index.get(normalise_word(query), set()))

def main():
    records = [
        "Patient has fractured femur and takes aspirin 75 mg.",
        "History of fracture; patient took paracetamol 500 mg.",
        "Children reviewed in fracture clinic. BP 120/80 mmHg.",
    ]
    for i, record in enumerate(records):
        print("Record", i, "entities:", extract_entities(record))
    index = build_index(records)
    for query in ("fracture", "fractures", "take"):
        print("Search", query, "-> record IDs", search(index, query))

if __name__ == "__main__":
    main()
