"""Top-down recursive-descent parser for a small context-free grammar."""

GRAMMAR = {
    "S": [["NP", "VP"]],
    "NP": [["Det", "N"], ["Name"]],
    "VP": [["V", "NP"], ["V"]],
    "Det": [["the"], ["a"]],
    "N": [["cat"], ["dog"], ["mouse"]],
    "Name": [["Alice"], ["Bob"]],
    "V": [["sees"], ["likes"], ["sleeps"]],
}


def parse(tokens, start="S"):
    """Return all parse trees for the token sequence."""
    tokens = tuple(tokens)

    def expand(symbol, position):
        if symbol not in GRAMMAR:
            if position < len(tokens) and tokens[position] == symbol:
                return [(symbol, position + 1)]
            return []

        results = []
        for production in GRAMMAR[symbol]:
            partials = [([], position)]
            for child in production:
                next_partials = []
                for children, current in partials:
                    for tree, end in expand(child, current):
                        next_partials.append((children + [tree], end))
                partials = next_partials
            results.extend(
                ((symbol, children), end)
                for children, end in partials
            )
        return results

    return [tree for tree, end in expand(start, 0) if end == len(tokens)]


if __name__ == "__main__":
    sentence = "the cat sees a mouse".split()
    trees = parse(sentence)
    print(trees[0] if trees else "No parse found.")
