"""Task 2 - Basic regular-expression entity patterns and greedy matching."""
import re

PATTERNS = {
    "PID": r"\bMRN-(?:20\d{2})-\d{6}\b",
    "DATE": r"\b(?:0[1-9]|[12]\d|3[01])[/-](?:0[1-9]|1[0-2])[/-](?:19|20)\d{2}\b|\b(?:[1-9]|[12]\d|3[01]) (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) (?:19|20)\d{2}\b",
    "DRUG": r"\b(?i:paracetamol|amoxicillin|ibuprofen|metformin|aspirin|insulin|atorvastatin|omeprazole|ceftriaxone|morphine|diclofenac|pantoprazole|furosemide|heparin|warfarin|azithromycin|ondansetron|tramadol)\s+\d{1,4}\s?(?:mg|g|mcg|ml)\b",
    "FREQ": r"\b(?:OD|BD|TDS|QID|SOS|q\d{1,2}h|[01]-[01]-[01]|twice daily|three times daily|once daily)\b",
    "LAB": r"\b(?:Hb|Na|K|Creatinine|Glucose|CRP|Urea)\s+\d{1,3}(?:\.\d)?\s?(?:g/dL|mmol/L|mg/dL|mg/L)\b",
    "BP": r"\b(?:[7-9]\d|1\d\d|2[0-4]\d)/(?:[4-9]\d|1[0-4]\d)\s+mmHg\b",
    "TEMP": r"\b(?:3[5-9]|4[0-2])\.\d\s?°?\s?C\b|\b(?:9[5-9]|10[0-8])\.\d\s?°?\s?F\b",
    "ICD": r"\b[A-TV-Z]\d{2}(?:\.\d{1,3}[A-Z]?)?\b",
    "WARD": r"\bWard \d[A-D], Bed \d{1,2}\b",
    "PHONE": r"(?<![\d.])(?:\+91 \d{5} \d{5}|[6-9]\d{9}|0\d{2,3}-\d{4} \d{4})(?!\d)",
    "AGE": r"\b(?:\d{1,3}-year-old|aged \d{1,3}|\d{1,3} (?:yrs|years)|\d{1,2} months old)\b",
    "DURATION": r"\b\d{1,3} (?:hours|days|weeks|months)\b",
}

def extract_entities(text):
    return [(kind, m.group(), m.start(), m.end())
            for kind, pattern in PATTERNS.items()
            for m in re.finditer(pattern, text)]

def main():
    sample = ("Patient MRN-2024-004512 visited on 12/03/2024. "
              "Paracetamol 500 mg BD. Hb 11.2 g/dL, BP 120/80 mmHg.")
    for entity in extract_entities(sample):
        print(entity)
    dose = "Paracetamol 500 mg and Aspirin 75 mg"
    print("Greedy:", re.search(r"Paracetamol.*mg", dose).group())
    print("Non-greedy:", re.search(r"Paracetamol.*?mg", dose).group())

if __name__ == "__main__":
    main()
