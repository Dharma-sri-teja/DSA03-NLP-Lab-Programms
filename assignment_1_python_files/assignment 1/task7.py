"""Task 7 - Small finite-state morphology analyser with lexical and irregular entries."""
LEXICON = {
    "fracture": {"N": ["SG", "PL"]},
    "operate": {"V": ["INF", "3SG", "PAST", "PASTP", "PROG"]},
    "take": {"V": ["INF", "3SG", "PAST", "PASTP", "PROG"]},
    "good": {"ADJ": ["POS", "COMP", "SUP"]},
}
FORMS = {
    "fracture": {"SG": "fracture", "PL": "fractures"},
    "operate": {"INF": "operate", "3SG": "operates", "PAST": "operated",
                "PASTP": "operated", "PROG": "operating"},
    "take": {"INF": "take", "3SG": "takes", "PAST": "took",
             "PASTP": "taken", "PROG": "taking"},
    "good": {"POS": "good", "COMP": "better", "SUP": "best"},
}

class MorphologyFST:
    def generate(self, lemma, feature):
        return FORMS.get(lemma, {}).get(feature)

    def analyse(self, surface):
        analyses = []
        for lemma, forms in FORMS.items():
            for feature, word in forms.items():
                if word == surface.lower():
                    analyses.append((lemma, feature))
        return analyses

def main():
    fst = MorphologyFST()
    for lemma, feature in (("fracture", "PL"), ("take", "PAST"), ("good", "COMP")):
        print("Generate:", lemma, feature, "->", fst.generate(lemma, feature))
    for surface in ("fractures", "took", "taken", "better", "taked"):
        print("Analyse:", surface, "->", fst.analyse(surface))

if __name__ == "__main__":
    main()
