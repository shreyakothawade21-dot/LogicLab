"""Safe propositional-logic engine (no eval). Tokenizer -> parser -> AST -> evaluator."""
import itertools
import re

TOKEN_RE = re.compile(r"\s*(<->|<=>|↔|->|=>|→|∧|∨|¬|⊕|&&|\|\||[()&|~!^]|[A-Za-z]+|[01])")
KEYWORDS = {"and": "and", "or": "or", "not": "not", "xor": "xor", "true": "1", "false": "0"}
SYMBOLS = {"&&": "and", "&": "and", "∧": "and", "||": "or", "|": "or", "∨": "or", "~": "not", "!": "not",
           "¬": "not", "^": "xor", "⊕": "xor", "->": "imp", "=>": "imp", "→": "imp",
           "<->": "iff", "<=>": "iff", "↔": "iff"}
GLYPH = {"and": "∧", "or": "∨", "xor": "⊕", "imp": "→", "iff": "↔"}


class LogicError(ValueError):
    pass


def tokenize(text):
    pos, out = 0, []
    text = text.strip()
    while pos < len(text):
        m = TOKEN_RE.match(text, pos)
        if not m:
            raise LogicError(f"Unexpected character near '{text[pos:pos + 5]}'")
        tok = m.group(1)
        pos = m.end()
        if tok in SYMBOLS:
            out.append(("op", SYMBOLS[tok]))
        elif tok in "()":
            out.append((tok, tok))
        elif tok in ("0", "1"):
            out.append(("const", tok == "1"))
        else:
            low = tok.lower()
            if low in KEYWORDS:
                k = KEYWORDS[low]
                out.append(("const", k == "1") if k in "01" else ("op", k))
            elif len(tok) == 1:
                out.append(("var", tok))
            else:
                raise LogicError(f"'{tok}' is not a valid variable (use single letters like p, q, r)")
    if not out:
        raise LogicError("Please enter an expression.")
    return out


class _Parser:
    # precedence (low→high):  <->   ->(right)   or   xor   and   not
    def __init__(self, toks):
        self.t, self.i = toks, 0

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else (None, None)

    def eat(self):
        tok = self.peek()
        self.i += 1
        return tok

    def parse(self):
        node = self.iff()
        if self.i != len(self.t):
            raise LogicError("Unexpected token — check your brackets and operators.")
        return node

    def _bin(self, op, nxt):
        node = nxt()
        while self.peek() == ("op", op):
            self.eat()
            node = (op, node, nxt())
        return node

    def iff(self):
        return self._bin("iff", self.imp)

    def imp(self):
        left = self.orr()
        if self.peek() == ("op", "imp"):
            self.eat()
            return ("imp", left, self.imp())
        return left

    def orr(self):
        return self._bin("or", self.xor)

    def xor(self):
        return self._bin("xor", self.andd)

    def andd(self):
        return self._bin("and", self.nott)

    def nott(self):
        if self.peek() == ("op", "not"):
            self.eat()
            return ("not", self.nott())
        return self.atom()

    def atom(self):
        kind, val = self.eat()
        if kind == "var":
            return ("var", val)
        if kind == "const":
            return ("const", val)
        if kind == "(":
            node = self.iff()
            if self.eat()[0] != ")":
                raise LogicError("Missing closing bracket ')'.")
            return node
        raise LogicError("Expression ended unexpectedly or has a misplaced operator.")


def parse(text):
    return _Parser(tokenize(text)).parse()


def variables(ast):
    if ast[0] == "var":
        return {ast[1]}
    if ast[0] == "const":
        return set()
    return set().union(*(variables(c) for c in ast[1:]))


def evaluate(ast, env):
    k = ast[0]
    if k == "var":
        return env[ast[1]]
    if k == "const":
        return ast[1]
    if k == "not":
        return not evaluate(ast[1], env)
    a, b = evaluate(ast[1], env), evaluate(ast[2], env)
    return {"and": a and b, "or": a or b, "xor": a != b, "imp": (not a) or b, "iff": a == b}[k]


def to_str(ast, top=True):
    k = ast[0]
    if k == "var":
        return ast[1]
    if k == "const":
        return "T" if ast[1] else "F"
    if k == "not":
        return "¬" + to_str(ast[1], False)
    s = f"{to_str(ast[1], False)} {GLYPH[k]} {to_str(ast[2], False)}"
    return s if top else f"({s})"


def subexpressions(ast):
    """Non-trivial sub-expressions in evaluation order (for step-by-step columns)."""
    seen, out = set(), []

    def walk(n):
        if n[0] in ("var", "const"):
            return
        for c in n[1:]:
            walk(c)
        s = to_str(n)
        if s not in seen:
            seen.add(s)
            out.append((s, n))
    walk(ast)
    return out


def assignments(vs):
    return [dict(zip(vs, c)) for c in itertools.product([True, False], repeat=len(vs))]


def truth_vector(ast, vs):
    return [evaluate(ast, env) for env in assignments(vs)]


def classify(vec):
    if all(vec):
        return "Tautology"
    if not any(vec):
        return "Contradiction"
    return "Contingency"


def normal_forms(ast, vs):
    """Return (DNF, CNF) strings derived from the truth table."""
    envs = assignments(vs)
    vec = [evaluate(ast, e) for e in envs]
    lit = lambda v, val: v if val else f"¬{v}"
    minterms = ["(" + " ∧ ".join(lit(v, e[v]) for v in vs) + ")" for e, r in zip(envs, vec) if r]
    maxterms = ["(" + " ∨ ".join(lit(v, not e[v]) for v in vs) + ")" for e, r in zip(envs, vec) if not r]
    dnf = " ∨ ".join(minterms) if minterms else "F (contradiction)"
    cnf = " ∧ ".join(maxterms) if maxterms else "T (tautology)"
    return dnf, cnf


# Classic equivalence laws used in the "Law Lab"
LAWS = [
    ("De Morgan's (AND)", "not (p and q)", "not p or not q"),
    ("De Morgan's (OR)", "not (p or q)", "not p and not q"),
    ("Implication as OR", "p -> q", "not p or q"),
    ("Contrapositive", "p -> q", "not q -> not p"),
    ("Biconditional split", "p <-> q", "(p -> q) and (q -> p)"),
    ("Double negation", "not not p", "p"),
    ("Distributive (AND over OR)", "p and (q or r)", "(p and q) or (p and r)"),
    ("Distributive (OR over AND)", "p or (q and r)", "(p or q) and (p or r)"),
    ("Absorption", "p or (p and q)", "p"),
    ("Exportation", "(p and q) -> r", "p -> (q -> r)"),
    ("XOR definition", "p xor q", "(p or q) and not (p and q)"),
    ("Negated implication", "not (p -> q)", "p and not q"),
]
