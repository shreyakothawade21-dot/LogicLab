# 🧠 LogicLab — Interactive Discrete Mathematics Learning Lab

> **Python + Streamlit · VIT Computer Engineering · AY 2026-27**
> A light, colourful playground covering all six units of the Discrete Mathematics syllabus.

## ✨ What's new in v2

| Area | Upgrades |
|------|----------|
| 🎨 **Frontend** | Light pastel theme (`.streamlit/config.toml` + custom CSS), calm static hero banners (no animations), clean cards, progress tracker, "maths fact of the day" |
| 🔢 **Logic** | Safe parser (no `eval`) · symbols `∧ ∨ ¬ ⊕ → ↔` · step-by-step sub-expression columns · DNF/CNF generator · **Law Lab** that proves 12 classic laws live |
| 🔣 **Counting** | Derangements, circular & repetition counts, binomial expansion, **Pascal's Triangle** with heat / Sierpiński / multiples-of-k colouring |
| 🧮 **Sets** | **Venn diagram** with region counts · consistency check · pigeonhole visual · set-operations playground with power set |
| ⚙️ **Modular** | Bézout / extended-Euclid table · **mod clock** · Sieve of Eratosthenes grid · square-and-multiply · **Chinese Remainder Theorem** |
| 🕸️ **Graphs** | Preset graphs (K₃,₃, Petersen…) · weights · BFS/DFS reveal slider · Dijkstra · MST · colouring · bipartite / planar / Euler checks |
| 🔁 **Recurrence** | **Playable Tower of Hanoi** · Catalan bracket generator · AP/GP · characteristic-equation solver with closed form |
| 📝 **Quiz** | 26 questions · topic filters · per-topic chart · weak-topic hints · downloadable report |
| 📚 **Cheat Sheet** | Searchable formula sheet for all 6 units |

## 🚀 Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```
Opens at **http://localhost:8501**.

## 📁 Structure

```
LogicLab/
├── app.py                    # entry point: navigation + page routing
├── requirements.txt
├── .streamlit/config.toml    # light theme
├── core/
│   ├── theme.py              # CSS + UI helpers (cards, badges, figures)
│   └── logic_engine.py       # tokenizer → parser → evaluator for propositional logic
└── modules/                  # one file per page
    ├── dashboard_page.py   logic_page.py      counting_page.py
    ├── sets_page.py        modular_page.py    graph_page.py
    ├── recurrence_page.py  quiz_page.py       cheatsheet_page.py
```

## 🎤 Demo script (≈5 min)

1. **Dashboard** — progress tracker, fact of the day, syllabus map.
2. **Logic** — `(p -> q) and (q -> r) -> (p -> r)` → tautology; then **Law Lab** → De Morgan.
3. **Counting** — Pascal's Triangle in *Even / Odd* mode (Sierpiński).
4. **Sets** — Venn diagram with the default numbers.
5. **Modular** — Mod Clock, then CRT `2,3; 3,5; 2,7` → x ≡ 23 (mod 105).
6. **Graphs** — preset *Weighted roads* → Dijkstra A→F and the MST.
7. **Recurrence** — Tower of Hanoi, drag the move slider.
8. **Quiz** — take 10 questions, show the topic chart.

*Made with 💜 using Python & Streamlit*
