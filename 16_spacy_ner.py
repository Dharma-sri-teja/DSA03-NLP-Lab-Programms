"""Named Entity Recognition with spaCy's pretrained English model."""

import spacy


def extract_entities(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    return [(entity.text, entity.label_) for entity in doc.ents]


if __name__ == "__main__":
    text = "Apple was founded by Steve Jobs in California."
    try:
        for entity, label in extract_entities(text):
            print(f"{entity:25} {label}")
    except OSError as error:
        print("spaCy model not found. Install it with:")
        print("  python -m spacy download en_core_web_sm")
        print(error)
