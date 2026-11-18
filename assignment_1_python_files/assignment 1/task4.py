"""Task 4 - NFA simulation, subset construction, DFA minimisation, Thompson NFA."""
from collections import defaultdict, deque
import re

class NFA:
    def __init__(self, start, finals, transitions):
        self.start, self.finals, self.transitions = start, set(finals), transitions

    def closure(self, states):
        stack, result = list(states), set(states)
        while stack:
            s = stack.pop()
            for nxt in self.transitions.get((s, None), set()):
                if nxt not in result:
                    result.add(nxt); stack.append(nxt)
        return result

    def accepts(self, text):
        states = self.closure({self.start})
        for ch in text:
            nxt = set()
            for s in states:
                nxt |= self.transitions.get((s, ch), set())
            states = self.closure(nxt)
        return bool(states & self.finals)

def subset_construction(nfa, alphabet):
    start = frozenset(nfa.closure({nfa.start}))
    queue, names = deque([start]), {start: "A"}
    dfa, finals = {}, set()
    while queue:
        state = queue.popleft()
        name = names[state]
        if state & nfa.finals: finals.add(name)
        for symbol in alphabet:
            target = frozenset(nfa.closure(
                set().union(*(nfa.transitions.get((s, symbol), set()) for s in state))))
            if target:
                if target not in names:
                    names[target] = chr(ord("A") + len(names)); queue.append(target)
                dfa[(name, symbol)] = names[target]
    return dfa, "A", finals

def minimise_dfa(trans, start, finals, alphabet):
    states = {start} | {s for s, _ in trans} | set(trans.values()) | {"DEAD"}
    part = {s: int(s in finals) for s in states}
    while True:
        signatures = {
            s: (part[s],) + tuple(part[trans.get((s, a), "DEAD")] for a in alphabet)
            for s in states
        }
        ids, new = {}, {}
        for s in states:
            new[s] = ids.setdefault(signatures[s], len(ids))
        if all((part[x] == part[y]) == (new[x] == new[y])
               for x in states for y in states):
            break
        part = new
    groups = defaultdict(list)
    for state, group in new.items(): groups[group].append(state)
    return list(groups.values())

def main():
    # NFA for strings "a" followed by zero or more "b".
    nfa = NFA(0, {1}, {
        (0, "a"): {1}, (1, "b"): {1}
    })
    for word in ("a", "ab", "abbb", "b", "aa"):
        print(word, nfa.accepts(word))
    dfa, start, finals = subset_construction(nfa, {"a", "b"})
    print("DFA:", dfa, "start:", start, "finals:", finals)
    print("Minimised groups:", minimise_dfa(dfa, start, finals, {"a", "b"}))
    print("Regex cross-check:", bool(re.fullmatch(r"ab*", "abbb")))

if __name__ == "__main__":
    main()
