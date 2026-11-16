import pandas as pd
import streamlit as st
from core import theme as T
from core import logic_engine as L

PRESETS = ["p and q", "p -> q", "not p or q", "(p -> q) and (q -> r)", "p xor q", "p or not p", "p and not p"]


def _tf(v):
    return "T" if v else "F"


def _style(df):
    def color(v):
        if v == "T":
            return "background-color:#dcfce7;color:#166534;font-weight:600;text-align:center"
        if v == "F":
            return "background-color:#ffe4ec;color:#9f1239;font-weight:600;text-align:center"
        return "text-align:center"
    return df.style.map(color)


def render():
    T.header("🔢 Logic & Truth Tables", "Type any expression — see every step, classify it, and discover normal forms")
    t1, t2, t3 = st.tabs(["📋 Truth Table Studio", "⚖️ Equivalence Checker", "🧪 Law Lab"])

    with t1:
        st.caption("Variables: single letters (p, q, r…) · Operators: `and` `or` `not` `xor` `->` `<->` · or symbols ∧ ∨ ¬ ⊕ → ↔")
        c1, c2 = st.columns([3, 2])
        preset = c2.selectbox("Quick examples", PRESETS, index=1)
        expr = c1.text_input("Expression", value=preset, key=f"tt_{preset}")
        show_steps = st.toggle("Show every sub-expression column (step-by-step)", value=True)
        try:
            ast = L.parse(expr)
            vs = sorted(L.variables(ast))
            if len(vs) > 5:
                st.error("Please use at most 5 distinct variables.")
                return
            envs = L.assignments(vs)
            rows = []
            subs = L.subexpressions(ast) if show_steps else []
            for e in envs:
                row = {v: _tf(e[v]) for v in vs}
                for s, node in subs:
                    row[s] = _tf(L.evaluate(node, e))
                row["RESULT"] = _tf(L.evaluate(ast, e))
                rows.append(row)
            df = pd.DataFrame(rows)
            df = df.loc[:, ~df.columns.duplicated()]  # result may repeat last sub-expression
            st.markdown(f"**Parsed as:** `{L.to_str(ast)}`")
            T.dataframe(_style(df), hide_index=True)

            vec = [L.evaluate(ast, e) for e in envs]
            kind = L.classify(vec)
            col = {"Tautology": "mint", "Contradiction": "rose", "Contingency": "lemon"}[kind]
            T.badge(f"{kind}", col)
            T.badge(f"{sum(vec)} of {len(vec)} rows are TRUE", "sky")
            meaning = {"Tautology": "always TRUE for every input.", "Contradiction": "always FALSE for every input.",
                       "Contingency": "sometimes TRUE and sometimes FALSE."}[kind]
            st.write(f"This expression is **{kind.lower()}** — {meaning}")

            with st.expander("🧬 Normal forms (derived from the table)"):
                dnf, cnf = L.normal_forms(ast, vs)
                st.markdown("**DNF** (OR of minterms):")
                T.formula(dnf)
                st.markdown("**CNF** (AND of maxterms):")
                T.formula(cnf)
                mins = [i for i, r in enumerate(vec) if r]
                st.caption(f"Row indices (top = 0) where TRUE: {mins}")
        except L.LogicError as ex:
            st.error(f"⚠️ {ex}")

    with t2:
        st.info("Two expressions are **logically equivalent** when their truth columns are identical for every assignment.")
        c1, c2 = st.columns(2)
        e1 = c1.text_input("Expression 1", "p -> q", key="eq1")
        e2 = c2.text_input("Expression 2", "not p or q", key="eq2")
        try:
            a1, a2 = L.parse(e1), L.parse(e2)
            vs = sorted(L.variables(a1) | L.variables(a2))
            v1, v2 = L.truth_vector(a1, vs), L.truth_vector(a2, vs)
            df = pd.DataFrame([{**{v: _tf(e[v]) for v in vs}, "Expr 1": _tf(x), "Expr 2": _tf(y),
                                "Match": "✔" if x == y else "✘"}
                               for e, x, y in zip(L.assignments(vs), v1, v2)])
            T.dataframe(df, hide_index=True)
            if v1 == v2:
                st.success(f"✅ Logically equivalent:  {L.to_str(a1)}  ≡  {L.to_str(a2)}")
            else:
                bad = [i for i, (x, y) in enumerate(zip(v1, v2)) if x != y]
                st.error(f"❌ Not equivalent — they differ in {len(bad)} row(s): {bad} (counting from 0).")
        except L.LogicError as ex:
            st.error(f"⚠️ {ex}")

    with t3:
        st.markdown("Pick a classic law — LogicLab **proves it by exhaustive truth-table check** live.")
        names = [n for n, _, _ in L.LAWS]
        pick = st.selectbox("Law", names)
        n, lhs, rhs = L.LAWS[names.index(pick)]
        a, b = L.parse(lhs), L.parse(rhs)
        vs = sorted(L.variables(a) | L.variables(b))
        ok = L.truth_vector(a, vs) == L.truth_vector(b, vs)
        c1, c2, c3 = st.columns([5, 1, 5])
        c1.markdown(f'<div class="formula">{L.to_str(a)}</div>', unsafe_allow_html=True)
        c2.markdown("<h2 style='text-align:center;color:#7c5cff'>≡</h2>", unsafe_allow_html=True)
        c3.markdown(f'<div class="formula">{L.to_str(b)}</div>', unsafe_allow_html=True)
        T.badge("Verified by all " + str(2 ** len(vs)) + " rows ✔" if ok else "Not valid ✘", "mint" if ok else "rose")
        with st.expander("📚 See all laws as a cheat-sheet"):
            T.dataframe(pd.DataFrame([{"Law": n, "Left": L.to_str(L.parse(l)), "Right": L.to_str(L.parse(r))}
                                       for n, l, r in L.LAWS]), hide_index=True)
