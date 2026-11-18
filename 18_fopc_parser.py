"""A recursive-descent parser for basic first-order predicate logic (FOPC).

Supported forms include predicates, quantifiers, negation, conjunction,
disjunction, implication, and parentheses. Example: forall x (Human(x) -> Mortal(x))
"""

import re


TOKEN_PATTERN = re.compile(
    r"\s*(->|[(),.&|~]|forall\b|exists\b|[A-Za-z_][A-Za-z_0-9]*)"
)


def tokenize(expression):
    expression = expression.strip()
    tokens = []
    position = 0
    while position < len(expression):
        match = TOKEN_PATTERN.match(expression, position)
        if not match:
            raise SyntaxError(f"Unexpected character at position {position}")
        tokens.append(match.group(1))
        position = match.end()
    return tokens


class FOPCParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def peek(self):
        return self.tokens[self.position] if self.position < len(self.tokens) else None

    def accept(self, expected):
        if self.peek() == expected:
            self.position += 1
            return True
        return False

    def require(self, expected):
        if not self.accept(expected):
            raise SyntaxError(f"Expected {expected!r}, found {self.peek()!r}")

    def parse(self):
        result = self.parse_implication()
        if self.peek() is not None:
            raise SyntaxError(f"Unexpected token {self.peek()!r}")
        return result

    def parse_implication(self):
        left = self.parse_or()
        if self.accept("->"):
            return ("implies", left, self.parse_implication())
        return left

    def parse_or(self):
        expression = self.parse_and()
        while self.accept("|"):
            expression = ("or", expression, self.parse_and())
        return expression

    def parse_and(self):
        expression = self.parse_unary()
        while self.accept("&"):
            expression = ("and", expression, self.parse_unary())
        return expression

    def parse_unary(self):
        if self.accept("~"):
            return ("not", self.parse_unary())
        if self.peek() in {"forall", "exists"}:
            quantifier = self.peek()
            self.position += 1
            variable = self.peek()
            if variable is None or not re.fullmatch(r"[A-Za-z_]\w*", variable):
                raise SyntaxError("Expected a variable after quantifier")
            self.position += 1
            return (quantifier, variable, self.parse_unary())
        if self.accept("("):
            expression = self.parse_implication()
            self.require(")")
            return expression
        return self.parse_predicate()

    def parse_predicate(self):
        name = self.peek()
        if name is None or not re.fullmatch(r"[A-Za-z_]\w*", name):
            raise SyntaxError(f"Expected predicate, found {name!r}")
        self.position += 1
        self.require("(")
        arguments = []
        if not self.accept(")"):
            while True:
                argument = self.peek()
                if argument is None or not re.fullmatch(r"[A-Za-z_]\w*", argument):
                    raise SyntaxError(f"Expected term, found {argument!r}")
                arguments.append(argument)
                self.position += 1
                if self.accept(")"):
                    break
                self.require(",")
        return ("predicate", name, tuple(arguments))


def parse_fopc(expression):
    return FOPCParser(tokenize(expression)).parse()


if __name__ == "__main__":
    sample = "forall x (Human(x) -> Mortal(x))"
    print(parse_fopc(sample))
