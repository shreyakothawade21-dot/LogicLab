import streamlit as st
from core import theme as T

UNITS = [
    ("🔢 Unit 1 — Logic & Proofs", "violet", [
        "p → q ≡ ¬p ∨ q ≡ ¬q → ¬p", "¬(p ∧ q) ≡ ¬p ∨ ¬q      ¬(p ∨ q) ≡ ¬p ∧ ¬q", "p ↔ q ≡ (p → q) ∧ (q → p)",
        "Tautology: always T · Contradiction: always F · Contingency: both", "Proof styles: direct, contrapositive, contradiction, induction"]),
    ("🔣 Unit 2 — Basic Counting", "sky", [
        "Sum rule: m + n      Product rule: m × n", "P(n,r) = n!/(n−r)!      C(n,r) = n!/(r!(n−r)!)",
        "Circular: (n−1)!      With repetition: nʳ and C(n+r−1, r)", "Pascal: C(n,r) = C(n−1,r−1) + C(n−1,r)"]),
    ("🧮 Unit 3 — Advanced Counting", "peach", [
        "|A∪B| = |A|+|B|−|A∩B|", "|A∪B∪C| = Σ|A| − Σ|A∩B| + |A∩B∩C|", "Pigeonhole: ⌈n/m⌉ in some box",
        "Derangements: D(n) = n!·Σ(−1)ᵏ/k!"]),
    ("🔁 Unit 4 — Recurrence Relations", "teal", [
        "Linear homogeneous: aₙ = c₁aₙ₋₁ + c₂aₙ₋₂ → solve r² − c₁r − c₂ = 0", "Distinct roots: aₙ = αr₁ⁿ + βr₂ⁿ",
        "Repeated root: aₙ = (α + βn)rⁿ", "Hanoi: T(n) = 2T(n−1)+1 = 2ⁿ−1      Catalan: C(n) = C(2n,n)/(n+1)"]),
    ("⚙️ Unit 5 — Modular Arithmetic", "lilac", [
        "a ≡ b (mod m) ⇔ m | (a−b)", "gcd(a,b)=gcd(b, a mod b)      lcm = ab/gcd", "a⁻¹ mod m exists ⇔ gcd(a,m)=1",
        "Fermat: aᵖ⁻¹ ≡ 1 (mod p)      CRT: unique solution mod m₁m₂…mₖ"]),
    ("🕸️ Unit 6 — Graph Theory", "rose", [
        "Σdeg(v) = 2|E|", "Kₙ has n(n−1)/2 edges      Tree: |E| = |V|−1", "Euler circuit ⇔ connected & all degrees even",
        "Bipartite ⇔ no odd cycle ⇔ 2-colourable", "Planar: Euler's formula V − E + F = 2"]),
]


def render():
    T.header("📚 Formula Cheat Sheet", "Every key result from the six units — perfect for last-minute revision")
    q = st.text_input("🔎 Filter formulas", placeholder="e.g. Fermat, tree, De Morgan …").lower()
    for title, color, items in UNITS:
        shown = [i for i in items if q in i.lower()] if q else items
        if not shown:
            continue
        T.card(color, "", title, "")
        for it in shown:
            T.formula(it)
