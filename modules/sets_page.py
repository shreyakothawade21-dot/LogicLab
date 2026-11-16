import math
import matplotlib.patches as mp
import streamlit as st
from core import theme as T


def venn3(A, B, C, AB, AC, BC, ABC):
    only = {"A": A - AB - AC + ABC, "B": B - AB - BC + ABC, "C": C - AC - BC + ABC,
            "AB": AB - ABC, "AC": AC - ABC, "BC": BC - ABC, "ABC": ABC}
    fig, ax = T.new_fig(5.6, 4.6)
    ax.set_aspect("equal")
    ax.axis("off")
    for (x, y), c in zip([(-0.9, 0.5), (0.9, 0.5), (0, -1.0)], ["#7c5cff", "#0ea5e9", "#f97316"]):
        ax.add_patch(mp.Circle((x, y), 1.5, fc=c, alpha=0.25, ec=c, lw=2))
    pos = {"A": (-1.55, 0.9), "B": (1.55, 0.9), "C": (0, -1.9), "AB": (0, 1.0), "AC": (-0.85, -0.45),
           "BC": (0.85, -0.45), "ABC": (0, 0.1)}
    for k, (x, y) in pos.items():
        ax.text(x, y, str(only[k]), ha="center", va="center", fontsize=13, fontweight="bold", color="#2b2a3a")
    ax.text(-2.3, 2.1, "A", fontsize=15, color="#5b3fd6", fontweight="bold")
    ax.text(2.1, 2.1, "B", fontsize=15, color="#0369a1", fontweight="bold")
    ax.text(0.15, -2.95, "C", fontsize=15, color="#c2410c", fontweight="bold")
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3.2, 2.6)
    return fig, only


def parse_set(txt):
    return {x.strip() for x in txt.split(",") if x.strip()}


def render():
    T.header("🧮 Set Counting", "Venn diagrams, Inclusion–Exclusion, Pigeonhole and a set-operations playground")
    t1, t2, t3 = st.tabs(["🔵 Inclusion–Exclusion + Venn", "🕊️ Pigeonhole", "🧰 Set Playground"])

    with t1:
        T.formula("|A∪B∪C| = |A|+|B|+|C| − |A∩B| − |A∩C| − |B∩C| + |A∩B∩C|")
        c = st.columns(3)
        A, B, C = (int(c[i].number_input(l, 0, 10000, v)) for i, (l, v) in enumerate([("|A|", 30), ("|B|", 25), ("|C|", 20)]))
        c = st.columns(4)
        AB, AC, BC, ABC = (int(c[i].number_input(l, 0, 10000, v)) for i, (l, v) in
                           enumerate([("|A∩B|", 10), ("|A∩C|", 8), ("|B∩C|", 7), ("|A∩B∩C|", 3)]))
        only = {"A": A - AB - AC + ABC, "B": B - AB - BC + ABC, "C": C - AC - BC + ABC,
                "AB": AB - ABC, "AC": AC - ABC, "BC": BC - ABC}
        valid = ABC <= min(AB, AC, BC) and all(v >= 0 for v in only.values())
        if not valid:
            st.error("These numbers are inconsistent (a region would have a negative count). Adjust the intersections.")
        else:
            total = A + B + C - AB - AC - BC + ABC
            left, right = st.columns([3, 2])
            with left:
                fig, _ = venn3(A, B, C, AB, AC, BC, ABC)
                T.show(fig)
            with right:
                T.card("violet", "🔵", f"|A ∪ B ∪ C| = {total}", "Elements in at least one set")
                with st.expander("📖 Step-by-step", expanded=True):
                    T.step(f"{A} + {B} + {C} = {A + B + C}")
                    T.step(f"− ({AB} + {AC} + {BC}) = − {AB + AC + BC}")
                    T.step(f"+ {ABC}  →  <b>{total}</b>")
                U = st.number_input("Universe size (optional)", 0, 100000, max(total, 0) + 10)
                if U >= total:
                    st.metric("Outside all three sets", U - total)

    with t2:
        st.info("**Pigeonhole:** put *n* items into *m* boxes → some box holds at least ⌈n/m⌉ items.")
        c1, c2 = st.columns(2)
        n = int(c1.number_input("Pigeons (n)", 1, 100000, 13))
        m = int(c2.number_input("Holes (m)", 1, 100000, 4))
        k = math.ceil(n / m)
        T.card("peach", "🕊️", f"At least {k} in one hole", f"⌈{n}/{m}⌉ = {k}")
        T.step(f"If every hole had ≤ {k - 1}, total ≤ {(k - 1) * m} < {n} → contradiction!")
        fig, ax = T.new_fig(7, 1.9 + m * 0.0)
        ax.axis("off")
        counts = [n // m + (1 if i < n % m else 0) for i in range(min(m, 12))]
        for i, cnt in enumerate(counts):
            ax.add_patch(mp.FancyBboxPatch((i * 1.2, 0), 1.0, 1.0, boxstyle="round,pad=0.02",
                                           fc="#ede9ff" if cnt < k else "#fecdd3", ec="#7c5cff"))
            ax.text(i * 1.2 + 0.5, 0.5, f"●×{cnt}" if cnt > 3 else "●" * cnt, ha="center", va="center", fontsize=11, color="#5b3fd6")
        ax.set_xlim(-0.2, len(counts) * 1.2)
        ax.set_ylim(-0.2, 1.2)
        T.show(fig)
        st.caption("Pink holes hold the guaranteed maximum. (Showing up to 12 holes.)")
        c1, c2, c3 = st.columns(3)
        c1.info("🎂 **Birthdays**\n\n367 people → two share a birthday")
        c2.info("🧦 **Socks**\n\n13 socks, 12 colours → a matching pair")
        c3.info("🃏 **Cards**\n\n5 cards, 4 suits → two of one suit")

    with t3:
        c1, c2 = st.columns(2)
        a = parse_set(c1.text_input("Set A", "1, 2, 3, 4, 5"))
        b = parse_set(c2.text_input("Set B", "4, 5, 6, 7"))
        srt = lambda s: "{ " + ", ".join(sorted(s, key=lambda x: (len(x), x))) + " }" if s else "∅"
        ops = [("A ∪ B", a | b), ("A ∩ B", a & b), ("A − B", a - b), ("B − A", b - a), ("A Δ B", a ^ b)]
        cols = st.columns(len(ops))
        for col, (nm, res) in zip(cols, ops):
            col.markdown(f'<div class="stat"><span>{nm}</span><b style="font-size:1rem">{srt(res)}</b><span>size {len(res)}</span></div>',
                         unsafe_allow_html=True)
        st.write("")
        st.write(f"**|A| = {len(a)}**, **|B| = {len(b)}**, A ⊆ B? **{a <= b}**, disjoint? **{not (a & b)}**, "
                 f"|P(A)| = 2^{len(a)} = **{2 ** len(a):,}**")
        if len(a) <= 4:
            import itertools
            ps = [set(c) for r in range(len(a) + 1) for c in itertools.combinations(sorted(a), r)]
            with st.expander("Show power set P(A)"):
                st.write(", ".join(srt(s) for s in ps))
