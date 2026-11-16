import math
import matplotlib.patches as mp
import streamlit as st
from core import theme as T


def derangements(n):
    a, b = 1, 0
    if n == 0:
        return 1
    for i in range(2, n + 1):
        a, b = b, (i - 1) * (a + b)
    return b


def render():
    T.header("🔣 Counting Lab", "Permutations, combinations, special counts and a playable Pascal's Triangle")
    t1, t2, t3 = st.tabs(["🔀 nPr & nCr", "🎲 Special Counts", "🔺 Pascal's Triangle"])

    with t1:
        c1, c2 = st.columns(2)
        n = int(c1.number_input("n (total items)", 0, 30, 5))
        r = int(c2.number_input("r (items chosen)", 0, 30, 2))
        if r > n:
            st.error("r cannot be greater than n.")
        else:
            perm, comb = math.perm(n, r), math.comb(n, r)
            a, b = st.columns(2)
            with a:
                T.card("sky", "🔀", f"P({n},{r}) = {perm:,}", "Permutation — order matters")
                T.formula(f"P(n,r) = n!/(n−r)! = {n}!/{n - r}!")
                with st.expander("📖 Step-by-step"):
                    T.step(f"n! = {math.factorial(n):,}")
                    T.step(f"(n−r)! = {math.factorial(n - r):,}")
                    T.step(f"P = {math.factorial(n):,} / {math.factorial(n - r):,} = <b>{perm:,}</b>")
            with b:
                T.card("mint", "🎯", f"C({n},{r}) = {comb:,}", "Combination — order does NOT matter")
                T.formula(f"C(n,r) = n!/(r!(n−r)!) = {n}!/({r}!·{n - r}!)")
                with st.expander("📖 Step-by-step"):
                    T.step(f"r! = {math.factorial(r):,}")
                    T.step(f"C = P / r! = {perm:,} / {math.factorial(r):,} = <b>{comb:,}</b>")
            T.callout(f"Every combination can be arranged in r! = {math.factorial(r):,} ways → "
                      f"P = C × r! → {comb:,} × {math.factorial(r):,} = {perm:,}")

    with t2:
        st.markdown("Explore **repetition, circular seating and derangements**.")
        c1, c2 = st.columns(2)
        n = int(c1.number_input("n", 1, 25, 6, key="sp_n"))
        r = int(c2.number_input("r", 0, 25, 3, key="sp_r"))
        d = st.columns(4)
        d[0].metric("Arrangements with repetition  nʳ", f"{n ** r:,}")
        d[1].metric("Combinations with repetition", f"{math.comb(n + r - 1, r):,}")
        d[2].metric("Circular arrangements (n−1)!", f"{math.factorial(n - 1):,}")
        d[3].metric("Derangements D(n)", f"{derangements(n):,}")
        with st.expander("🧠 What do these mean?"):
            T.step("<b>nʳ</b>: choose r times from n options, repeats allowed, order matters (e.g. PIN codes).")
            T.step("<b>C(n+r−1, r)</b>: choose r items from n types with repeats, order ignored (e.g. ice-cream scoops).")
            T.step("<b>(n−1)!</b>: seat n people round a table; rotations are the same.")
            T.step("<b>D(n)</b>: rearrange n items so that <i>none</i> stays in its original place (secret-santa!).")
        st.markdown("##### 🧮 Binomial expansion of (x + y)ⁿ")
        k = st.slider("Power n", 1, 10, 4, key="binom")
        terms = []
        for i in range(k + 1):
            co = math.comb(k, i)
            x = "" if k - i == 0 else ("x" if k - i == 1 else f"x^{k - i}")
            y = "" if i == 0 else ("y" if i == 1 else f"y^{i}")
            terms.append(f"{co if co > 1 or not (x or y) else ''}{x}{y}")
        T.formula(f"(x + y)^{k} = " + " + ".join(terms))

    with t3:
        rows = st.slider("Rows", 3, 16, 10)
        mode = st.radio("Colour by", ["Value (heat)", "Even / Odd (Sierpiński!)", "Multiples of k"], horizontal=True)
        k = 3
        if mode == "Multiples of k":
            k = st.slider("k", 2, 9, 3)
        fig, ax = T.new_fig(8, 0.55 * rows + 1)
        ax.set_aspect("equal")
        ax.axis("off")
        mx = math.comb(rows - 1, (rows - 1) // 2)
        for i in range(rows):
            for j in range(i + 1):
                v = math.comb(i, j)
                if mode.startswith("Value"):
                    t = math.log(v + 1) / math.log(mx + 1)
                    col = (0.55 + 0.4 * (1 - t), 0.45 + 0.4 * (1 - t), 1.0)
                elif mode.startswith("Even"):
                    col = "#c4b5fd" if v % 2 else "#ffffff"
                else:
                    col = "#fda4af" if v % k == 0 else "#e0f2fe"
                x, y = j - i / 2, -i
                ax.add_patch(mp.Circle((x, y), 0.46, fc=col, ec="#8b5cf6", lw=1))
                ax.text(x, y, str(v), ha="center", va="center", fontsize=max(6, 11 - rows // 3), color="#3b2a8c")
        ax.set_xlim(-rows / 2, rows / 2)
        ax.set_ylim(-rows, 1)
        T.show(fig)
        st.caption("Each number is the sum of the two above it. Try “Even / Odd” with 16 rows to reveal the Sierpiński triangle fractal.")
