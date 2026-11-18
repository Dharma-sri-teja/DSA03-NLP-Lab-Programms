"""Task 3 - Maximal-munch tokenisation and safe text normalisation."""
import re

TOKEN_RE = re.compile(
    r"MRN-\d{4}-\d{6}|"
    r"\d{1,3}(?:\.\d+)?\s?(?:g/dL|mmol/L|mg/dL|mg/L|mg|mcg|ml)|"
    r"\d{1,3}/\d{1,3}\s?mmHg|"
    r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|"
    r"[A-Za-z]+(?:[-'][A-Za-z]+)*|"
    r"\d+(?:\.\d+)?|[^\w\s]",
    re.IGNORECASE
)

ABBREVIATIONS = {
    "bd": "twice daily", "tds": "three times daily",
    "od": "once daily", "qid": "four times daily",
}

def tokenise(text):
    return TOKEN_RE.findall(text)

def normalise(text):
    text = text.casefold()
    text = re.sub(r"\b(\d+)\s+(mg|mcg|ml|g/dl|mmol/l|mg/dl|mg/l)\b",
                  r"\1\2", text)
    text = re.sub(r"\b(bd|tds|od|qid)\b",
                  lambda m: ABBREVIATIONS[m.group()], text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def main():
    sample = "Operation note: MRN-2024-004512; Hb 11.2 g/dL; Paracetamol 500 mg BD."
    print("Tokens:", tokenise(sample))
    print("Normalised:", normalise(sample))

if __name__ == "__main__":
    main()
