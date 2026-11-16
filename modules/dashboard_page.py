import datetime
import pandas as pd
import streamlit as st
from core import theme as T

MODULES = [
    ("violet", "🔢", "Logic & Truth Tables", "Step-by-step truth tables, DNF/CNF, equivalence checker and a live Law Lab."),
    ("sky", "🔣", "Counting Lab", "nPr, nCr, derangements, circular seating, binomials and a colourful Pascal's Triangle."),
    ("peach", "🧮", "Set Counting", "Venn diagrams, Inclusion–Exclusion, Pigeonhole visual and set playground."),
    ("lilac", "⚙️", "Modular Arithmetic", "GCD, Bézout, inverses, mod clock, sieve, fast power and CRT."),
    ("rose", "🕸️", "Graph Theory", "BFS/DFS, Dijkstra, MST, colouring, bipartite & planarity — with presets."),
    ("teal", "🔁", "Recurrence Relations", "Playable Tower of Hanoi, Catalan, AP/GP and a characteristic-equation solver."),
    ("mint", "📝", "Practice Quiz", "26 questions, topic filters, per-topic analysis and a downloadable report."),
    ("lemon", "📚", "Cheat Sheet", "Searchable formula sheet for all six units."),
]
FACTS = [
    "There are more possible orderings of a 52-card deck (52!) than atoms on Earth.",
    "Among any 367 people, two must share a birthday — pure pigeonhole.",
    "Euler founded graph theory in 1736 by solving the Königsberg bridge puzzle.",
    "The Tower of Hanoi with 64 disks would need 2⁶⁴−1 moves — about 585 billion years at one move per second.",
    "RSA encryption keeps the internet safe using modular arithmetic and huge primes.",
    "Fibonacci ratios F(n+1)/F(n) converge to the golden ratio φ ≈ 1.618.",
    "The Four-Colour Theorem says any map needs at most four colours — proved with computer help in 1976.",
    "Catalan numbers appear in over 200 different counting problems.",
]
UNITS = pd.DataFrame({
    "Unit": [f"Unit {i}" for i in range(1, 7)],
    "Topic": ["Logic and Proofs", "Basic Counting", "Advanced Combinatorial Techniques",
              "Recurrence Relations & Generating Functions", "Modular Arithmetic", "Graph Theory"],
    "Hours": [5, 5, 4, 5, 4, 5],
    "LogicLab Module": ["🔢 Logic", "🔣 Counting Lab", "🧮 Set Counting", "🔁 Recurrence", "⚙️ Modular", "🕸️ Graphs"],
})


def render(visited, best):
    T.header("🧠 LogicLab", "Your colourful, interactive Discrete Mathematics playground")
    cols = st.columns(4)
    v = len([x for x in visited if x not in ("🏠 Dashboard",)])
    for c, (val, lab) in zip(cols, [(f"{v}/8", "modules explored"), (f"{best}%" if best else "—", "best quiz score"),
                                    ("26", "quiz questions"), ("6", "syllabus units")]):
        c.markdown(T.stat(val, lab), unsafe_allow_html=True)
    st.progress(v / 8, text="Exploration progress")

    fact = FACTS[datetime.date.today().toordinal() % len(FACTS)]
    T.callout(f"<b>Maths fact of the day:</b> {fact}")

    st.markdown("### 🗂️ Modules")
    names = ["🔢 Logic & Truth Tables", "🔣 Counting Lab", "🧮 Set Counting", "⚙️ Modular Arithmetic",
             "🕸️ Graph Theory", "🔁 Recurrence Relations", "📝 Practice Quiz", "📚 Cheat Sheet"]
    c1, c2 = st.columns(2)
    for i, ((color, icon, title, body), nm) in enumerate(zip(MODULES, names)):
        with (c1 if i % 2 == 0 else c2):
            T.card(color, icon, title, body + ("  <span class='pill-ok'>explored</span>" if nm in visited else ""))
            st.button("Open →", key=f"open_{i}", on_click=lambda n=nm: st.session_state.update(nav=n))

    st.markdown("### 📋 Syllabus coverage")
    T.dataframe(UNITS, hide_index=True)
