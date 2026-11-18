"""Task 12 - Robustness extension: OCR repair and code-mixed token routing."""
import re
from difflib import get_close_matches

LOOKALIKE = {"0": "o", "1": "l", "5": "s", "8": "b", "|": "l"}
KNOWN_WORDS = {
    "muscle", "ligament", "colitis", "admission", "complication",
    "hypertension", "fracture", "renal", "pulmonary", "medicine",
}
REGIONAL_WORDS = {"panninen", "kal", "se", "tha", "abhi"}

def repair_ocr(token, vocabulary=KNOWN_WORDS):
    candidate = "".join(LOOKALIKE.get(ch, ch) for ch in token.lower())
    if candidate in vocabulary:
        return candidate
    matches = get_close_matches(candidate, vocabulary, n=1, cutoff=0.72)
    return matches[0] if matches else None

def route_token(token):
    word = token.lower()
    if word in REGIONAL_WORDS:
        return ("REGIONAL", word)
    repaired = repair_ocr(word)
    if repaired:
        return ("OCR_REPAIRED", repaired)
    if re.fullmatch(r"[a-z]+", word):
        return ("PORTER_FALLBACK", simple_stem(word))
    return ("UNHANDLED", word)

def simple_stem(word):
    for suffix in ("ing", "ed", "es", "s"):
        if len(word) > len(suffix) + 2 and word.endswith(suffix):
            return word[:-len(suffix)]
    return word

def main():
    samples = ["rnuscle", "ligamcnt", "c0litis", "panninen",
               "kal", "fractured", "unknown"]
    for token in samples:
        print(token, "->", route_token(token))

if __name__ == "__main__":
    main()
