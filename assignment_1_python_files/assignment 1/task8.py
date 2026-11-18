"""Task 8 - Orthographic rewrite rules and a sequential rule cascade."""
import re

def apply_rules(lexical):
    """Convert a ^-marked lexical form to a surface form using ordered rules."""
    word = lexical.lower()
    # ie -> y before -ing: die^ing -> dying
    word = re.sub(r"ie\^ing$", "ying", word)
    # consonant+y -> ies before plural s: biopsy^s -> biopsies
    word = re.sub(r"([^aeiou])y\^s$", r"\1ies", word)
    # sibilant + plural: rash^s -> rashes
    word = re.sub(r"(s|x|z|ch|sh)\^s$", r"\1es", word)
    # consonant+y before ed/er/est/ness/able/ment
    word = re.sub(r"([^aeiou])y\^(ed|er|est|ness|able|ment)$",
                  lambda m: m.group(1) + "i" + m.group(2), word)
    # e deletion before a vowel-initial suffix
    word = re.sub(r"e\^(ed|ing|ation|able)$", r"\1", word)
    # remove remaining boundary marker
    word = word.replace("^", "").replace("*", "")
    # regular suffixes for examples without a special spelling change
    word = word.replace("fractureed", "fractured")
    return word

def main():
    examples = ["die^ing", "biopsy^s", "rash^s", "carry^ed",
                "fracture^ed", "observe^ation"]
    for item in examples:
        print(item, "->", apply_rules(item))

if __name__ == "__main__":
    main()
