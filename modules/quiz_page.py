import random
import pandas as pd
import streamlit as st
from core import theme as T

# (topic, question, options, answer_index, explanation)
BANK = [
    ("Logic", "What is the value of p AND (NOT p)?", ["Always True", "Always False", "Depends on p", "Undefined"], 1,
     "p ∧ ¬p is always False — the Law of Contradiction."),
    ("Logic", "p → q is logically equivalent to:", ["p ∧ q", "¬p ∧ q", "¬p ∨ q", "p ∨ ¬q"], 2,
     "p → q ≡ ¬p ∨ q. It is false only when p is true and q is false."),
    ("Logic", "Which of these is a tautology?", ["p ∧ ¬p", "p ∨ q", "p ∨ ¬p", "p ∧ q"], 2,
     "p ∨ ¬p is always True — Law of Excluded Middle."),
    ("Logic", "The contrapositive of p → q is:", ["q → p", "¬p → ¬q", "¬q → ¬p", "¬(p → q)"], 2,
     "The contrapositive ¬q → ¬p is always equivalent to the original implication."),
    ("Logic", "By De Morgan's law, ¬(p ∧ q) equals:", ["¬p ∧ ¬q", "¬p ∨ ¬q", "p ∨ q", "¬p → q"], 1,
     "Negating an AND flips it to an OR of negations: ¬p ∨ ¬q."),
    ("Counting", "In how many ways can 5 different books be arranged on a shelf?", ["25", "60", "120", "720"], 2,
     "5! = 120."),
    ("Counting", "What is C(5, 2)?", ["5", "10", "20", "25"], 1, "C(5,2) = 5!/(2!·3!) = 10."),
    ("Counting", "What is P(4, 2)?", ["6", "8", "12", "24"], 2, "P(4,2) = 4!/2! = 12."),
    ("Counting", "How many ways to seat 5 people around a circular table?", ["5", "24", "60", "120"], 1,
     "Circular arrangements: (n−1)! = 4! = 24."),
    ("Counting", "A password has 3 digits (0–9, repeats allowed). How many passwords?", ["30", "720", "1000", "6561"], 2,
     "10³ = 1000."),
    ("Sets & Pigeonhole", "If |A|=10, |B|=8, |A∩B|=3, then |A∪B| =", ["13", "15", "18", "21"], 1, "10 + 8 − 3 = 15."),
    ("Sets & Pigeonhole", "13 cards drawn from a deck guarantee at least how many of one suit?", ["2", "3", "4", "5"], 2,
     "⌈13/4⌉ = 4."),
    ("Sets & Pigeonhole", "A set with 5 elements has how many subsets?", ["10", "25", "32", "120"], 2, "2⁵ = 32."),
    ("Modular", "What is 17 mod 5?", ["1", "2", "3", "5"], 1, "17 = 5×3 + 2."),
    ("Modular", "What is GCD(48, 18)?", ["3", "6", "9", "12"], 1, "48=18·2+12; 18=12·1+6; 12=6·2 → 6."),
    ("Modular", "The modular inverse of 3 (mod 7) is:", ["2", "3", "5", "6"], 2, "3 × 5 = 15 ≡ 1 (mod 7)."),
    ("Modular", "What is 2¹⁰ mod 11?", ["0", "1", "2", "10"], 1, "Fermat: 2^(11−1) ≡ 1 (mod 11)."),
    ("Modular", "Does 6 have an inverse modulo 9?", ["Yes, it is 2", "Yes, it is 4", "No, gcd = 3", "No, 9 is not prime"], 2,
     "An inverse exists iff gcd(6,9)=1, but gcd = 3."),
    ("Graphs", "Max edges in a simple undirected graph with 5 vertices?", ["5", "8", "10", "20"], 2, "C(5,2) = 10."),
    ("Graphs", "The degree of a vertex is:", ["Number of vertices", "Number of incident edges", "Total edges", "Shortest path length"], 1,
     "Degree = edges touching the vertex."),
    ("Graphs", "Sum of degrees in a graph with 7 edges is:", ["7", "10", "14", "49"], 2, "Handshaking lemma: Σdeg = 2|E| = 14."),
    ("Graphs", "A graph has an Euler circuit iff it is connected and:", ["all degrees are even", "has a cycle", "is a tree", "is bipartite"], 0,
     "Euler's theorem: every vertex has even degree."),
    ("Graphs", "A tree with n vertices has how many edges?", ["n", "n − 1", "n + 1", "n²"], 1, "Trees have exactly n − 1 edges."),
    ("Recurrence", "F(6) in Fibonacci (F1=F2=1) is:", ["5", "8", "13", "21"], 1, "1,1,2,3,5,8."),
    ("Recurrence", "Minimum moves for Tower of Hanoi with 4 disks?", ["7", "15", "16", "31"], 1, "2⁴ − 1 = 15."),
    ("Recurrence", "Which is the 4th Catalan number C(4)?", ["5", "10", "14", "42"], 2, "1, 1, 2, 5, 14 → C(4) = 14."),
]
TOPICS = sorted({q[0] for q in BANK})


def render():
    T.header("📝 Practice Quiz", f"{len(BANK)} questions across {len(TOPICS)} topics — pick your challenge")
    ss = st.session_state
    ss.setdefault("quiz", None)
    ss.setdefault("best", 0)

    if ss.quiz is None:
        c1, c2 = st.columns([3, 1])
        chosen = c1.multiselect("Topics", TOPICS, default=TOPICS)
        pool = [i for i, q in enumerate(BANK) if q[0] in chosen]
        n = c2.number_input("Questions", 1, max(1, len(pool)), min(10, max(1, len(pool))))
        if st.button("🚀 Start quiz", disabled=not pool):
            ss.quiz = {"ids": random.sample(pool, int(n)), "done": False, "ans": {}}
            ss.quiz_gen = ss.get("quiz_gen", 0) + 1
            st.rerun()
        if ss.best:
            st.metric("🏆 Best score this session", f"{ss.best}%")
        return

    qz = ss.quiz
    ids = qz["ids"]
    if not qz["done"]:
        with st.form("quiz_form"):
            for k, i in enumerate(ids):
                topic, q, opts, _, _ = BANK[i]
                st.markdown(f"**Q{k + 1}.** {q}  <span class='pill-todo'>{topic}</span>", unsafe_allow_html=True)
                st.radio(f"q{k}", opts, index=None, key=f"qa_{ss.get('quiz_gen', 0)}_{k}", label_visibility="collapsed")
                st.divider()
            sub = st.form_submit_button("🎯 Submit")
        if sub:
            for k, i in enumerate(ids):
                v = ss.get(f"qa_{ss.get('quiz_gen', 0)}_{k}")
                qz["ans"][k] = BANK[i][2].index(v) if v is not None else None
            qz["done"] = True
            st.rerun()
        if st.button("↩ Cancel"):
            ss.quiz = None
            st.rerun()
        return

    score = sum(qz["ans"][k] == BANK[i][3] for k, i in enumerate(ids))
    pct = round(100 * score / len(ids))
    ss.best = max(ss.best, pct)
    msg = ("🏆 Outstanding!" if pct >= 80 else "👍 Good job — keep practising!" if pct >= 60 else "📚 Review the explanations below — you'll get there!")
    T.card("mint" if pct >= 80 else "peach" if pct >= 60 else "rose", "🎯", f"{score}/{len(ids)} correct ({pct}%)", msg)
    by = {}
    for k, i in enumerate(ids):
        t = by.setdefault(BANK[i][0], [0, 0])
        t[1] += 1
        t[0] += qz["ans"][k] == BANK[i][3]
    st.markdown("##### 📊 Performance by topic")
    st.bar_chart(pd.DataFrame({"Score %": {t: 100 * a / b for t, (a, b) in by.items()}}), color="#7c5cff")
    weak = [t for t, (a, b) in by.items() if a < b]
    if weak:
        T.callout("Revise: " + ", ".join(weak))
    lines = []
    for k, i in enumerate(ids):
        topic, q, opts, ans, why = BANK[i]
        mine = qz["ans"][k]
        ok = mine == ans
        lines.append(f"Q{k + 1} [{topic}] {'OK' if ok else 'WRONG'} — {q} | yours: {opts[mine] if mine is not None else '-'} | correct: {opts[ans]}")
        with st.expander(f"{'✅' if ok else '❌'} Q{k + 1}: {q}"):
            if ok:
                st.success(f"Your answer: {opts[ans]}")
            else:
                st.error(f"Your answer: {opts[mine] if mine is not None else 'Not answered'}")
                st.success(f"Correct: {opts[ans]}")
            st.info(f"💡 {why}")
    c1, c2 = st.columns(2)
    c1.download_button("⬇️ Download report", "\n".join(lines) + f"\n\nScore: {score}/{len(ids)} ({pct}%)", "logiclab_quiz_report.txt")
    if c2.button("🔄 New quiz"):
        ss.quiz = None
        st.rerun()
