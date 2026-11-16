import math
import cmath
import matplotlib.patches as mp
import pandas as pd
import streamlit as st
from core import theme as T


def hanoi_states(n):
    pegs = [list(range(n, 0, -1)), [], []]
    moves, states = [], [[p[:] for p in pegs]]

    def go(k, a, b, c):
        if k == 0:
            return
        go(k - 1, a, c, b)
        pegs[b].append(pegs[a].pop())
        moves.append((k, "ABC"[a], "ABC"[b]))
        states.append([p[:] for p in pegs])
        go(k - 1, c, b, a)
    go(n, 0, 2, 1)
    return moves, states


def draw_hanoi(state, n):
    fig, ax = T.new_fig(7, 3)
    ax.axis("off")
    cols = ["#c4b5fd", "#7dd3fc", "#86efac", "#fdba74", "#f9a8d4", "#fde68a", "#5eead4"]
    for i, peg in enumerate(state):
        x = i * 4 + 2
        ax.plot([x, x], [0, n + 1], color="#a78bfa", lw=4, solid_capstyle="round", zorder=1)
        ax.text(x, -0.7, "ABC"[i], ha="center", color="#5b3fd6", fontweight="bold")
        for h, d in enumerate(peg):
            w = 0.45 + d * 0.22
            ax.add_patch(mp.FancyBboxPatch((x - w, h + 0.05), 2 * w, 0.85, boxstyle="round,pad=0.02",
                                           fc=cols[(d - 1) % len(cols)], ec="#7c5cff", zorder=3))
    ax.plot([-0.5, 12.5], [0, 0], color="#7c5cff", lw=3)
    ax.set_xlim(-0.5, 12.5)
    ax.set_ylim(-1.1, n + 1.4)
    return fig


def render():
    T.header("🔁 Recurrence Relations", "Fibonacci, Catalan, a playable Tower of Hanoi, sequences and a recurrence solver")
    tabs = st.tabs(["🌀 Fibonacci", "📊 Catalan", "🗼 Tower of Hanoi", "➕ AP / GP", "🧮 Recurrence Solver"])

    with tabs[0]:
        T.formula("F(1)=F(2)=1,  F(n) = F(n−1) + F(n−2)")
        n = st.slider("Number of terms", 2, 40, 12)
        fib = [1, 1]
        while len(fib) < n:
            fib.append(fib[-1] + fib[-2])
        fib = fib[:n]
        l, r = st.columns([1, 2])
        T.dataframe_in(l, pd.DataFrame({"n": range(1, n + 1), "F(n)": fib}), hide_index=True, height=330)
        with r:
            fig, ax = T.new_fig(6, 3.4)
            ratios = [fib[i] / fib[i - 1] for i in range(1, n)]
            ax.plot(range(2, n + 1), ratios, "o-", color="#7c5cff")
            ax.axhline((1 + 5 ** .5) / 2, color="#f97316", ls="--", label="φ ≈ 1.618")
            ax.set_xlabel("n")
            ax.set_ylabel("F(n)/F(n−1)")
            ax.legend()
            T.show(fig)
        T.callout(f"F({n})/F({n - 1}) = {fib[-1] / fib[-2]:.8f} → converging to the golden ratio φ = 1.6180339…")

    with tabs[1]:
        T.formula("C(n) = (2n)! / ((n+1)! n!) = C(2n,n)/(n+1)")
        N = st.slider("How many", 4, 16, 10, key="cat")
        cat = [math.comb(2 * k, k) // (k + 1) for k in range(N)]
        l, r = st.columns([1, 2])
        T.dataframe_in(l, pd.DataFrame({"n": range(N), "C(n)": cat}), hide_index=True, height=330)
        with r:
            fig, ax = T.new_fig(6, 3.4)
            ax.bar(range(N), cat, color="#a78bfa")
            ax.set_yscale("log")
            ax.set_xlabel("n")
            ax.set_ylabel("C(n)  (log scale)")
            T.show(fig)
        T.callout("Catalan numbers count balanced bracket strings, binary trees, polygon triangulations and Dyck paths.")
        k = st.slider("Valid bracket strings of length 2k", 1, 4, 3)
        out = []

        def gen(s, o, c):
            if len(s) == 2 * k:
                out.append(s)
                return
            if o < k:
                gen(s + "(", o + 1, c)
            if c < o:
                gen(s + ")", o, c + 1)
        gen("", 0, 0)
        st.code("   ".join(out))
        st.caption(f"{len(out)} strings = C({k}) = {cat[k]} ✔")

    with tabs[2]:
        n = st.slider("Disks", 1, 6, 3)
        moves, states = hanoi_states(n)
        T.card("rose", "🗼", f"{n} disks → {2 ** n - 1} minimum moves", f"T(n) = 2·T(n−1) + 1  ⇒  T(n) = 2ⁿ − 1")
        k = st.slider("Move number", 0, len(moves), 0, key=f"hn_{n}")
        T.show(draw_hanoi(states[k], n))
        if k:
            d, a, b = moves[k - 1]
            T.step(f"Move {k}: disk {d} from <b>{a}</b> → <b>{b}</b>")
        else:
            st.caption("Drag the slider to watch the solution unfold, one move at a time.")
        with st.expander("📋 Full move list"):
            st.write(" · ".join(f"{i}. d{d}:{a}→{b}" for i, (d, a, b) in enumerate(moves, 1)))

    with tabs[3]:
        kind = st.radio("Type", ["Arithmetic", "Geometric"], horizontal=True)
        c = st.columns(3)
        a = c[0].number_input("First term a", value=2.0 if kind == "Geometric" else 1.0)
        d = c[1].number_input("Common difference d" if kind == "Arithmetic" else "Common ratio r",
                              value=3.0 if kind == "Arithmetic" else 2.0)
        n = int(c[2].number_input("Terms n", 1, 40, 8))
        if kind == "Arithmetic":
            seq = [a + i * d for i in range(n)]
            S = n * (2 * a + (n - 1) * d) / 2
            T.formula("aₙ = a + (n−1)d    Sₙ = n/2 · (2a + (n−1)d)")
        else:
            seq = [a * d ** i for i in range(n)]
            S = a * n if d == 1 else a * (d ** n - 1) / (d - 1)
            T.formula("aₙ = a·rⁿ⁻¹    Sₙ = a(rⁿ − 1)/(r − 1)")
        l, r = st.columns([1, 2])
        T.dataframe_in(l, pd.DataFrame({"n": range(1, n + 1), "aₙ": seq}), hide_index=True, height=300)
        with r:
            fig, ax = T.new_fig(6, 3.2)
            ax.plot(range(1, n + 1), seq, "o-", color="#0ea5e9")
            T.show(fig)
        st.success(f"Sum of first {n} terms  S = {S:g}")

    with tabs[4]:
        st.markdown("Solve **aₙ = c₁·aₙ₋₁ + c₂·aₙ₋₂** — the characteristic-equation method.")
        c = st.columns(4)
        c1, c2 = c[0].number_input("c₁", value=1.0), c[1].number_input("c₂", value=1.0)
        a0, a1 = c[2].number_input("a₀", value=0.0), c[3].number_input("a₁", value=1.0)
        T.formula(f"Characteristic equation:  r² − ({c1:g})r − ({c2:g}) = 0")
        disc = c1 * c1 + 4 * c2
        r1, r2 = (c1 + cmath.sqrt(disc)) / 2, (c1 - cmath.sqrt(disc)) / 2
        terms = [a0, a1]
        for _ in range(14):
            terms.append(c1 * terms[-1] + c2 * terms[-2])
        if disc > 1e-12:
            R1, R2 = r1.real, r2.real
            A = (a1 - a0 * R2) / (R1 - R2)
            B = a0 - A
            T.card("sky", "✨", "Two distinct real roots", f"r₁ = {R1:.4g}, r₂ = {R2:.4g}")
            T.formula(f"aₙ = {A:.4g}·({R1:.4g})ⁿ + {B:.4g}·({R2:.4g})ⁿ")
            ok = all(abs(A * R1 ** n + B * R2 ** n - terms[n]) < 1e-6 * max(1, abs(terms[n])) for n in range(10))
            st.caption("Closed form matches the recurrence for the first 10 terms ✔" if ok else "Closed form check failed.")
        elif abs(disc) <= 1e-12:
            R = r1.real
            B = (a1 - a0 * R) / R if R else 0
            T.card("lemon", "✨", "One repeated root", f"r = {R:.4g}")
            T.formula(f"aₙ = ({a0:.4g} + {B:.4g}·n)·({R:.4g})ⁿ")
        else:
            T.card("lilac", "✨", "Complex conjugate roots", f"r = {r1:.3g}, {r2:.3g} → oscillating solution")
        T.dataframe(pd.DataFrame({"n": range(len(terms)), "aₙ": [round(t, 4) for t in terms]}).T)
        st.caption("Try c₁=1, c₂=1, a₀=0, a₁=1 for Fibonacci · c₁=1, c₂=2 for Jacobsthal-type growth.")
