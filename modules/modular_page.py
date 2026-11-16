import math
import matplotlib.patches as mp
import numpy as np
import pandas as pd
import streamlit as st
from core import theme as T


def egcd(a, b):
    """Extended Euclid: returns (g, x, y) with a*x + b*y = g, plus the table of steps."""
    rows, (r0, r1), (s0, s1), (t0, t1) = [], (a, b), (1, 0), (0, 1)
    while r1:
        q = r0 // r1
        rows.append({"q": q, "r": r1, "s": s1, "t": t1})
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
        t0, t1 = t1, t0 - q * t1
    return r0, s0, t0, rows


def is_prime(n):
    return n > 1 and all(n % i for i in range(2, math.isqrt(n) + 1))


def crt(pairs):
    x, M = 0, 1
    for a, m in pairs:
        g, p, _, _ = egcd(M, m)
        if g != 1:
            raise ValueError("Moduli must be pairwise coprime.")
        x = (x + (a - x) * p * M) % (M * m)
        M *= m
    return x % M, M


def render():
    T.header("⚙️ Modular Arithmetic", "GCD, Bézout, inverses, primes, Fermat, CRT and a modular clock")
    tabs = st.tabs(["🔢 GCD / LCM", "🔄 Inverse", "🕐 Mod Clock", "🔍 Primes & Sieve", "📐 Fermat & Fast Power", "🧩 CRT"])

    with tabs[0]:
        c1, c2 = st.columns(2)
        a, b = int(c1.number_input("a", value=48, step=1)), int(c2.number_input("b", value=18, step=1))
        g = math.gcd(a, b)
        l = abs(a * b) // g if g else 0
        m = st.columns(3)
        m[0].metric(f"{a} mod {b}", a % b if b else "undefined")
        m[1].metric("GCD", g)
        m[2].metric("LCM", l)
        if a > 0 and b > 0:
            with st.expander("📖 Euclidean algorithm", expanded=True):
                x, y = max(a, b), min(a, b)
                while y:
                    T.step(f"{x} = {y} × {x // y} + {x % y}")
                    x, y = y, x % y
                T.step(f"GCD = <b>{g}</b>")
            _, s, t, _ = egcd(a, b)
            T.callout(f"Bézout: {a}·({s}) + {b}·({t}) = {a * s + b * t} = gcd")

    with tabs[1]:
        st.markdown("Find **a⁻¹ mod m** — exists only when gcd(a, m) = 1.")
        c1, c2 = st.columns(2)
        a, m = int(c1.number_input("a", value=3, step=1, key="ia")), int(c2.number_input("m", min_value=2, value=7, step=1, key="im"))
        g, s, _, rows = egcd(a, m)
        if g != 1:
            st.error(f"No inverse: gcd({a},{m}) = {g} ≠ 1")
        else:
            inv = s % m
            T.card("lilac", "🔄", f"{a}⁻¹ mod {m} = {inv}", f"because {a} × {inv} = {a * inv} ≡ {a * inv % m} (mod {m})")
            with st.expander("📖 Extended Euclid table"):
                T.dataframe(pd.DataFrame(rows), hide_index=True)
            if m <= 40:
                st.markdown("**Multiplication table row** — find where the product hits 1:")
                T.dataframe(pd.DataFrame({"k": range(m), f"{a}·k mod {m}": [a * k % m for k in range(m)]}).T)

    with tabs[2]:
        c1, c2, c3 = st.columns(3)
        n = int(c1.slider("Modulus n", 2, 24, 12))
        a = int(c2.number_input("Number a", value=29, step=1))
        step_k = int(c3.slider("Highlight multiples of", 1, 12, 5))
        fig, ax = T.new_fig(4.6, 4.6)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.add_patch(mp.Circle((0, 0), 1, fc="#fff", ec="#8b5cf6", lw=2))
        hit = {(step_k * i) % n for i in range(n)}
        for k in range(n):
            ang = np.pi / 2 - 2 * np.pi * k / n
            x, y = 0.82 * np.cos(ang), 0.82 * np.sin(ang)
            col = "#7c5cff" if k == a % n else ("#fecdd3" if k in hit else "#ede9ff")
            ax.add_patch(mp.Circle((x, y), 0.1, fc=col, ec="#7c5cff"))
            ax.text(x, y, str(k), ha="center", va="center", fontsize=9, color="white" if k == a % n else "#3b2a8c")
        ax.text(0, 0, f"{a} mod {n}\n= {a % n}", ha="center", va="center", fontsize=15, fontweight="bold", color="#5b3fd6")
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        c1, c2 = st.columns([3, 2])
        with c1:
            T.show(fig)
        with c2:
            T.callout(f"{a} = {n}×{a // n} + {a % n}. On a {n}-hour clock it lands on <b>{a % n}</b>.")
            T.step(f"Pink = reachable by repeatedly adding {step_k} (mod {n}): {len(hit)} of {n} positions.")
            T.step("All positions reachable ⇔ gcd(step, n) = 1" + (" ✅" if math.gcd(step_k, n) == 1 else " ❌ (here it's not)"))

    with tabs[3]:
        c1, c2 = st.columns([1, 2])
        num = int(c1.number_input("Check a number", min_value=2, value=91, step=1))
        if is_prime(num):
            T.card("mint", "✅", f"{num} is PRIME", "Only divisors: 1 and itself.")
        else:
            f, x, d = [], num, 2
            while x > 1:
                while x % d == 0:
                    f.append(d)
                    x //= d
                d += 1
            T.card("rose", "❌", f"{num} is COMPOSITE", "Prime factorisation: " + " × ".join(map(str, f)))
        with c2:
            N = st.slider("Sieve of Eratosthenes up to", 30, 200, 100, step=10)
            sieve = [True] * (N + 1)
            sieve[0] = sieve[1] = False
            for i in range(2, math.isqrt(N) + 1):
                if sieve[i]:
                    for j in range(i * i, N + 1, i):
                        sieve[j] = False
            cols = 10
            rows = math.ceil((N + 1) / cols)
            fig, ax = T.new_fig(6, 0.42 * rows + 0.4)
            ax.axis("off")
            for v in range(1, N + 1):
                r, c = divmod(v - 1, cols)
                ax.add_patch(mp.FancyBboxPatch((c, -r), 0.9, 0.8, boxstyle="round,pad=0.02",
                                               fc="#c4b5fd" if sieve[v] else "#f3f4f6", ec="none"))
                ax.text(c + 0.45, -r + 0.4, str(v), ha="center", va="center", fontsize=8,
                        color="#3b2a8c" if sieve[v] else "#9ca3af")
            ax.set_xlim(0, cols)
            ax.set_ylim(-rows + 0.5, 1)
            T.show(fig)
            st.caption(f"{sum(sieve)} primes up to {N} (purple).")

    with tabs[4]:
        T.formula("p prime, gcd(a,p)=1  ⇒  a^(p−1) ≡ 1 (mod p)")
        c1, c2, c3 = st.columns(3)
        a = int(c1.number_input("base a", value=3, step=1, key="fa"))
        e = int(c2.number_input("exponent e", min_value=0, value=13, step=1, key="fe"))
        m = int(c3.number_input("modulus m", min_value=2, value=7, step=1, key="fm"))
        T.card("teal", "📐", f"{a}^{e} mod {m} = {pow(a, e, m)}", "Computed with square-and-multiply")
        bits, res, base, rows = bin(e)[2:][::-1], 1, a % m, []
        for i, bt in enumerate(bits):
            if bt == "1":
                res = res * base % m
            rows.append({"bit i": i, "bit": bt, f"{a}^(2^{i}) mod {m}": base, "running result": res})
            base = base * base % m
        with st.expander("📖 Square-and-multiply table"):
            T.dataframe(pd.DataFrame(rows), hide_index=True)
        if is_prime(m) and math.gcd(a, m) == 1:
            T.callout(f"Fermat check: {a}^{m - 1} mod {m} = {pow(a, m - 1, m)} ✅ (equals 1, as predicted)")
            T.step(f"Reduce the exponent: {e} mod {m - 1} = {e % (m - 1)} → {a}^{e % (m - 1)} ≡ {pow(a, e % (m - 1), m)}")
        else:
            st.info("Fermat's theorem needs a prime modulus and gcd(a, m) = 1 — pick those to see the shortcut.")

    with tabs[5]:
        st.markdown("Solve  **x ≡ aᵢ (mod mᵢ)**  with pairwise-coprime moduli (Chinese Remainder Theorem).")
        txt = st.text_input("Congruences as a,m pairs separated by ;", "2,3; 3,5; 2,7")
        try:
            pairs = [tuple(int(v) for v in p.split(",")) for p in txt.split(";") if p.strip()]
            x, M = crt(pairs)
            T.card("peach", "🧩", f"x ≡ {x} (mod {M})", "Unique solution modulo the product of the moduli")
            T.dataframe(pd.DataFrame([{"congruence": f"x ≡ {a} (mod {m})", f"{x} mod {m}": x % m,
                                        "✔": "✔" if x % m == a % m else "✘"} for a, m in pairs]),
                         hide_index=True)
        except Exception as ex:
            st.error(f"⚠️ {ex}")
