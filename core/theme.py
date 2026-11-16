"""Light, pastel look & feel + small UI helpers for LogicLab."""
import html
import matplotlib.pyplot as plt
import streamlit as st

PALETTE = {
    "violet": ("#ede9ff", "#7c5cff"),
    "sky":    ("#e0f2fe", "#0ea5e9"),
    "mint":   ("#dcfce7", "#16a34a"),
    "peach":  ("#ffedd5", "#f97316"),
    "rose":   ("#ffe4ec", "#e11d74"),
    "lemon":  ("#fef9c3", "#ca8a04"),
    "teal":   ("#ccfbf1", "#0d9488"),
    "lilac":  ("#f3e8ff", "#9333ea"),
}
MPL = ["#7c5cff", "#0ea5e9", "#16a34a", "#f97316", "#e11d74", "#ca8a04", "#0d9488", "#9333ea"]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', 'Segoe UI', system-ui, sans-serif; }
.block-container { padding-top: 1.6rem; max-width: 1180px; }

[data-testid="stSidebar"] { background: linear-gradient(180deg,#f3efff 0%,#eaf6ff 100%); border-right: 1px solid #e4defc; }
.brand { font-size: 1.55rem; font-weight: 700; color:#5b3fd6; margin-bottom:-.2rem; }
.brand-sub { font-size:.8rem; color:#7a76a0; margin-bottom:.4rem; }

.hero {
  position:relative; overflow:hidden; border-radius: 22px; padding: 1.7rem 2rem; margin-bottom: 1.3rem;
  background: linear-gradient(120deg,#ede9ff 0%,#e0f2fe 55%,#dcfce7 100%);
  border: 1px solid #ddd6fe; box-shadow: 0 8px 24px rgba(124,92,255,.10);
}
.hero h1 { margin:0; font-size:1.9rem; color:#3b2a9c; font-weight:700; }
.hero p  { margin:.3rem 0 0; color:#55528a; font-size:.98rem; }

.lcard { border-radius:18px; padding:1.05rem 1.2rem; margin-bottom:.8rem; border:1px solid rgba(0,0,0,.05);
  box-shadow: 0 2px 10px rgba(60,40,140,.06); }
.lcard h3 { margin:0 0 .25rem; font-size:1.05rem; font-weight:600; }
.lcard p  { margin:0; font-size:.88rem; color:#4b4a63; }

.formula { background:#fff; border:1.5px dashed #c4b5fd; color:#4c1d95; font-family:'JetBrains Mono',monospace;
  font-size:.95rem; padding:.75rem 1rem; border-radius:12px; margin:.5rem 0; }
.step { background:#f5f3ff; border-left:4px solid #8b5cf6; padding:.55rem .9rem; border-radius:0 10px 10px 0;
  margin:.3rem 0; color:#3b2a8c; font-size:.93rem; }
.badge { display:inline-block; padding:4px 14px; border-radius:999px; font-weight:600; font-size:.85rem; margin:.15rem .2rem .15rem 0; }
.callout { background:#fffbea; border:1px solid #fde68a; border-radius:14px; padding:.7rem 1rem; color:#713f12; margin:.5rem 0; }
.stat { background:#fff; border:1px solid #ece8ff; border-radius:16px; padding:.8rem 1rem; text-align:center; box-shadow:0 3px 10px rgba(124,92,255,.06); }
.stat b { display:block; font-size:1.5rem; color:#5b3fd6; } .stat span { font-size:.8rem; color:#7a76a0; }
.pill-ok { color:#166534; background:#dcfce7; padding:2px 10px; border-radius:999px; font-size:.78rem; font-weight:600; }
.pill-todo { color:#6b7280; background:#f3f4f6; padding:2px 10px; border-radius:999px; font-size:.78rem; }

.stButton > button { border-radius: 12px; border: 1px solid #c4b5fd; background: linear-gradient(135deg,#8b5cf6,#6366f1); color:#fff; font-weight:600; padding:.45rem 1.1rem; }
.stButton > button:hover { filter: brightness(1.07); border-color:#8b5cf6; color:#fff; }
button[data-baseweb="tab"] { border-radius: 10px 10px 0 0; }
[data-testid="stMetric"] { background:#fff; border:1px solid #ece8ff; border-radius:14px; padding:.6rem .9rem; box-shadow:0 2px 8px rgba(124,92,255,.05); }

/* refinements: hide Streamlit chrome, tidy spacing, calm focus states */
footer, .stDeployButton, [data-testid="stDecoration"] { display:none !important; visibility:hidden; }
h3 { margin-top:1.1rem; color:#3b2a9c; }
h5 { color:#4c1d95; margin-top:.8rem; }
.hero { padding: 1.4rem 1.8rem; }
.stButton > button { box-shadow:none; transition:none; }
.stButton > button:focus:not(:active) { border-color:#7c5cff; color:#fff; }
[data-testid="stExpander"] { border:1px solid #e4defc; border-radius:14px; background:#fff; }
[data-testid="stDataFrame"] { border:1px solid #ece8ff; border-radius:12px; }
* { scroll-behavior:auto !important; }
@media (prefers-reduced-motion: reduce) { * { animation:none !important; transition:none !important; } }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


def header(title: str, subtitle: str = ""):
    st.markdown(
        f'<div class="hero"><h1>{title}</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True)


def card(color: str, icon: str, title: str, body: str):
    bg, fg = PALETTE.get(color, PALETTE["violet"])
    st.markdown(
        f'<div class="lcard" style="background:{bg}"><h3 style="color:{fg}">{icon} {title}</h3><p>{body}</p></div>',
        unsafe_allow_html=True)


def formula(text: str):
    st.markdown(f'<div class="formula">{html.escape(text)}</div>', unsafe_allow_html=True)


def step(text: str):
    st.markdown(f'<div class="step">➤ {text}</div>', unsafe_allow_html=True)


def badge(text: str, color: str = "violet"):
    bg, fg = PALETTE.get(color, PALETTE["violet"])
    st.markdown(f'<span class="badge" style="background:{bg};color:{fg}">{html.escape(text)}</span>', unsafe_allow_html=True)


def callout(text: str):
    st.markdown(f'<div class="callout">💡 {text}</div>', unsafe_allow_html=True)


def stat(value, label: str) -> str:
    return f'<div class="stat"><b>{value}</b><span>{label}</span></div>'


def new_fig(w=6.5, h=4.2):
    """Matplotlib figure that matches the light theme."""
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor("#fbfaff")
    ax.set_facecolor("#ffffff")
    for s in ax.spines.values():
        s.set_color("#ddd6fe")
    return fig, ax


def _stretch(fn, *a, **kw):
    """Full-width rendering that works on old (use_container_width) and new (width='stretch') Streamlit."""
    try:
        return fn(*a, width="stretch", **kw)
    except TypeError:
        return fn(*a, use_container_width=True, **kw)


def dataframe(data, **kw):
    return _stretch(st.dataframe, data, **kw)


def dataframe_in(container, data, **kw):
    return _stretch(container.dataframe, data, **kw)


def show(fig):
    _stretch(st.pyplot, fig)
    plt.close(fig)
