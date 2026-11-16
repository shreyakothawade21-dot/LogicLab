# ============================================================
#  LogicLab — Interactive Discrete Mathematics Learning Lab
#  Built with Python + Streamlit  |  Run:  streamlit run app.py
# ============================================================
import streamlit as st

st.set_page_config(page_title="LogicLab – Discrete Mathematics", page_icon="🧠", layout="wide",
                   initial_sidebar_state="expanded")

from core import theme as T  # noqa: E402
from modules import (cheatsheet_page, counting_page, dashboard_page, graph_page, logic_page,  # noqa: E402
                     modular_page, quiz_page, recurrence_page, sets_page)

T.inject_css()

PAGES = {
    "🏠 Dashboard": None,
    "🔢 Logic & Truth Tables": logic_page.render,
    "🔣 Counting Lab": counting_page.render,
    "🧮 Set Counting": sets_page.render,
    "⚙️ Modular Arithmetic": modular_page.render,
    "🕸️ Graph Theory": graph_page.render,
    "🔁 Recurrence Relations": recurrence_page.render,
    "📝 Practice Quiz": quiz_page.render,
    "📚 Cheat Sheet": cheatsheet_page.render,
}

ss = st.session_state
ss.setdefault("visited", set())
ss.setdefault("best", 0)
ss.setdefault("nav", "🏠 Dashboard")

with st.sidebar:
    st.markdown('<div class="brand">🧠 LogicLab</div><div class="brand-sub">Discrete Mathematics · VIT</div>',
                unsafe_allow_html=True)
    page = st.radio("Navigate", list(PAGES), key="nav", label_visibility="collapsed")
    st.divider()
    st.progress(len(ss.visited - {"🏠 Dashboard"}) / 8, text="Modules explored")
    st.caption("Made with 💜 using Streamlit\n\nAY 2026-27")

ss.visited.add(page)
if page == "🏠 Dashboard":
    dashboard_page.render(ss.visited, ss.best)
else:
    PAGES[page]()
