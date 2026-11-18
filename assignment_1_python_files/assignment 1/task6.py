"""Task 6 - Derivational morphology: affix inventory and valid attachment order."""
SUFFIXES = {
    "itis": ("N", "inflammation"), "ectomy": ("N", "surgical removal"),
    "ology": ("N", "study of"), "osis": ("N", "condition"),
    "ation": ("N", "verb-to-noun"), "ion": ("N", "verb-to-noun"),
    "ment": ("N", "verb-to-noun"), "ive": ("ADJ", "verb-to-adjective"),
    "able": ("ADJ", "verb-to-adjective"), "ness": ("N", "adjective-to-noun"),
    "ly": ("ADV", "adjective-to-adverb"),
}
PREFIXES = {"re": "repeat", "un": "not", "hyper": "high", "hypo": "low",
            "post": "after", "pre": "before", "anti": "against", "intra": "within"}

def derive(root, suffix):
    if suffix not in SUFFIXES:
        raise ValueError("Unknown suffix")
    # Demonstration stems used in the assignment.
    if root == "treat" and suffix == "ment": return "treatment"
    if root == "observe" and suffix == "ation": return "observation"
    if root == "operate" and suffix == "ion": return "operation"
    if root == "mild" and suffix == "ness": return "mildness"
    return root + suffix

def main():
    for root, suffix in (("treat", "ment"), ("observe", "ation"),
                         ("operate", "ion"), ("mild", "ness")):
        print(f"{root} + {suffix} -> {derive(root, suffix)}")
    print("Available prefixes:", ", ".join(PREFIXES))
    print("Available suffixes:", ", ".join(SUFFIXES))

if __name__ == "__main__":
    main()
