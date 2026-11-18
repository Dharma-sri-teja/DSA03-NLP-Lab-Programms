"""Task 5 - Inflectional morphology: paradigms and irregular word forms."""
REGULAR = {
    "fracture": {"N.SG": "fracture", "N.PL": "fractures"},
    "operate": {"V.INF": "operate", "V.3SG": "operates", "V.PAST": "operated",
                "V.PASTP": "operated", "V.PROG": "operating"},
    "admit": {"V.INF": "admit", "V.3SG": "admits", "V.PAST": "admitted",
              "V.PASTP": "admitted", "V.PROG": "admitting"},
    "biopsy": {"N.SG": "biopsy", "N.PL": "biopsies"},
    "mild": {"ADJ.POS": "mild", "ADJ.COMP": "milder", "ADJ.SUP": "mildest"},
}
IRREGULAR = {
    "diagnosis": {"N.SG": "diagnosis", "N.PL": "diagnoses"},
    "take": {"V.INF": "take", "V.3SG": "takes", "V.PAST": "took",
             "V.PASTP": "taken", "V.PROG": "taking"},
    "good": {"ADJ.POS": "good", "ADJ.COMP": "better", "ADJ.SUP": "best"},
}

def generate(lemma, feature):
    paradigm = IRREGULAR.get(lemma, REGULAR.get(lemma, {}))
    return paradigm.get(feature)

def analyse(surface):
    return [(lemma, feature) for lemma, paradigm in {**REGULAR, **IRREGULAR}.items()
            for feature, form in paradigm.items() if form == surface]

def main():
    for lemma in ("fracture", "take", "good"):
        paradigm = IRREGULAR.get(lemma, REGULAR.get(lemma, {}))
        print(lemma, paradigm)
    for word in ("fractures", "took", "better", "unknown"):
        print(word, "=>", analyse(word))

if __name__ == "__main__":
    main()
