import networkx as nx
import pandas as pd
import streamlit as st
from core import theme as T

PRESETS = {
    "Custom (edit below)": None,
    "Square with diagonal": ("A, B, C, D", "A-B, B-C, C-D, D-A, A-C"),
    "House": ("A, B, C, D, E", "A-B, B-C, C-D, D-A, A-E, B-E"),
    "Weighted roads": ("A, B, C, D, E, F", "A-B:4, A-C:2, B-C:1, B-D:5, C-D:8, C-E:10, D-E:2, D-F:6, E-F:3"),
    "K4 (complete)": ("1, 2, 3, 4", "1-2, 1-3, 1-4, 2-3, 2-4, 3-4"),
    "K3,3 (non-planar)": ("a, b, c, x, y, z", "a-x, a-y, a-z, b-x, b-y, b-z, c-x, c-y, c-z"),
    "Petersen graph": ("0, 1, 2, 3, 4, 5, 6, 7, 8, 9",
                       "0-1, 1-2, 2-3, 3-4, 4-0, 0-5, 1-6, 2-7, 3-8, 4-9, 5-7, 7-9, 9-6, 6-8, 8-5"),
}
NODE_COLS = ["#c4b5fd", "#7dd3fc", "#86efac", "#fdba74", "#f9a8d4", "#fde68a", "#5eead4", "#d8b4fe"]


def build(vs_txt, es_txt, directed):
    vs = [v.strip() for v in vs_txt.split(",") if v.strip()]
    G = nx.DiGraph() if directed else nx.Graph()
    G.add_nodes_from(vs)
    warn = []
    for e in es_txt.split(","):
        e = e.strip()
        if not e:
            continue
        w = 1
        if ":" in e:
            e, ws = e.rsplit(":", 1)
            try:
                w = float(ws)
                w = int(w) if w == int(w) else w
            except ValueError:
                warn.append(f"Bad weight in '{e}:{ws}'")
                continue
        parts = [p.strip() for p in e.split("-")]
        if len(parts) == 2 and parts[0] in vs and parts[1] in vs:
            G.add_edge(parts[0], parts[1], weight=w)
        else:
            warn.append(f"Edge '{e}' skipped (unknown vertex or bad format)")
    return vs, G, warn


def draw(G, pos, node_cols=None, hi_edges=(), labels=True, hi_nodes=()):
    fig, ax = T.new_fig(6.6, 4.6)
    ax.axis("off")
    hi = {tuple(e) for e in hi_edges} | {tuple(reversed(e)) for e in hi_edges}
    ecol = ["#f43f5e" if (u, v) in hi else "#a5b4fc" for u, v in G.edges]
    ew = [4 if (u, v) in hi else 2 for u, v in G.edges]
    kw = dict(arrows=True, arrowsize=18, node_size=900) if G.is_directed() else {}
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color=ecol, width=ew, **kw)
    cols = node_cols or ["#c4b5fd"] * len(G)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=cols, node_size=900, edgecolors="#7c5cff", linewidths=2)
    nx.draw_networkx_labels(G, pos, ax=ax, font_color="#2b2a3a", font_weight="bold", font_size=11)
    if labels and any(d.get("weight", 1) != 1 for *_, d in G.edges(data=True)):
        nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels={(u, v): d["weight"] for u, v, d in G.edges(data=True)},
                                     font_size=9, font_color="#be123c", bbox=dict(fc="white", ec="none", alpha=.8))
    return fig


def render():
    T.header("🕸️ Graph Theory", "Build a graph, then run BFS, DFS, shortest paths, MST, colouring and more")
    pick = st.selectbox("🎁 Load a preset graph", list(PRESETS))
    default_v, default_e = PRESETS[pick] or ("A, B, C, D, E", "A-B, B-C, C-D, D-E, A-C, B-D")
    c1, c2 = st.columns(2)
    vs_txt = c1.text_input("Vertices (comma-separated)", default_v, key=f"v_{pick}")
    es_txt = c2.text_input("Edges  (u-v, optional weight  u-v:5)", default_e, key=f"e_{pick}")
    directed = st.checkbox("Directed graph", False)

    try:
        vs, G, warns = build(vs_txt, es_txt, directed)
    except Exception as ex:
        st.error(f"⚠️ {ex}")
        return
    for w in warns:
        st.warning(w)
    if not vs:
        st.info("Add at least one vertex.")
        return
    pos = nx.spring_layout(G, seed=7) if len(G) > 2 else nx.circular_layout(G)
    U = G.to_undirected()
    tabs = st.tabs(["📊 Overview", "🚶 BFS / DFS", "🛣️ Shortest Path", "🌲 Spanning Tree", "🎨 Colouring & More"])

    with tabs[0]:
        l, r = st.columns([3, 2])
        with l:
            T.show(draw(G, pos))
        with r:
            m = st.columns(2)
            m[0].metric("Vertices |V|", G.number_of_nodes())
            m[1].metric("Edges |E|", G.number_of_edges())
            conn = nx.is_weakly_connected(G) if directed else nx.is_connected(G)
            m = st.columns(2)
            m[0].metric("Connected?", "Yes ✅" if conn else "No ❌")
            m[1].metric("Components", nx.number_connected_components(U))
            if not directed:
                st.metric("Eulerian circuit?", "Yes ✅" if conn and nx.is_eulerian(G) else "No ❌")
        st.markdown("##### 🔢 Adjacency matrix")
        T.dataframe(nx.to_pandas_adjacency(G, nodelist=vs, dtype=int))
        st.markdown("##### 📐 Degrees")
        if directed:
            dd = pd.DataFrame({"Vertex": vs, "In": [G.in_degree(v) for v in vs], "Out": [G.out_degree(v) for v in vs]})
        else:
            dd = pd.DataFrame({"Vertex": vs, "Degree": [G.degree(v) for v in vs]})
        T.dataframe(dd, hide_index=True)
        if not directed:
            T.callout(f"Handshaking lemma: Σdeg = {sum(d for _, d in G.degree())} = 2×|E| = {2 * G.number_of_edges()} ✅")
            odd = [v for v, d in G.degree() if d % 2]
            st.caption(f"Odd-degree vertices: {odd or 'none'} → "
                       + ("Euler circuit possible." if not odd else "Euler path possible." if len(odd) == 2 else "no Euler path."))

    with tabs[1]:
        start = st.selectbox("Start vertex", vs)
        bfs = [start] + [v for _, v in nx.bfs_edges(G, start)]
        dfs = [start] + [v for _, v in nx.dfs_edges(G, start)]
        order = st.radio("Traversal", ["BFS", "DFS"], horizontal=True)
        seq = bfs if order == "BFS" else dfs
        tree = list(nx.bfs_edges(G, start)) if order == "BFS" else list(nx.dfs_edges(G, start))
        k = st.slider("Reveal visited vertices", 1, len(seq), len(seq)) if len(seq) > 1 else 1
        cols = ["#86efac" if v in seq[:k] else "#e5e7eb" for v in G.nodes]
        cols = ["#7c5cff" if v == start else c for v, c in zip(G.nodes, cols)]
        l, r = st.columns([3, 2])
        with l:
            T.show(draw(G, pos, cols, tree[:k - 1]))
        with r:
            T.card("mint", "🚶", f"{order} order", " → ".join(seq[:k]))
            st.caption("BFS uses a queue (level by level); DFS uses a stack (as deep as possible first).")

    with tabs[2]:
        c1, c2 = st.columns(2)
        s = c1.selectbox("From", vs, key="sp_s")
        t = c2.selectbox("To", vs, index=len(vs) - 1, key="sp_t")
        try:
            path = nx.dijkstra_path(G, s, t, weight="weight")
            dist = nx.dijkstra_path_length(G, s, t, weight="weight")
            l, r = st.columns([3, 2])
            with l:
                T.show(draw(G, pos, ["#fdba74" if v in path else "#e5e7eb" for v in G.nodes], list(zip(path, path[1:]))))
            with r:
                T.card("peach", "🛣️", f"Distance = {dist}", " → ".join(path))
                st.caption("Dijkstra's algorithm. Edge weights default to 1 — add `:w` to edges for a weighted graph.")
        except nx.NetworkXNoPath:
            st.error("No path exists between these vertices.")

    with tabs[3]:
        if nx.is_connected(U) and len(U) > 1:
            mst = nx.minimum_spanning_tree(U, weight="weight")
            tot = sum(d["weight"] for *_, d in mst.edges(data=True))
            l, r = st.columns([3, 2])
            with l:
                T.show(draw(U, pos, None, list(mst.edges)))
            with r:
                T.card("lilac", "🌲", f"MST weight = {tot}", f"{mst.number_of_edges()} edges (= |V| − 1)")
                T.dataframe(pd.DataFrame([{"edge": f"{u}–{v}", "weight": d["weight"]} for u, v, d in mst.edges(data=True)]),
                             hide_index=True)
        else:
            st.info("A spanning tree needs a connected graph with 2+ vertices.")

    with tabs[4]:
        col = nx.greedy_color(U, strategy="largest_first")
        chi = max(col.values()) + 1 if col else 0
        l, r = st.columns([3, 2])
        with l:
            T.show(draw(U, pos, [NODE_COLS[col[v] % len(NODE_COLS)] for v in U.nodes]))
        with r:
            T.card("rose", "🎨", f"Greedy colouring uses {chi} colours", "Adjacent vertices never share a colour")
            st.metric("Bipartite?", "Yes ✅" if nx.is_bipartite(U) else "No ❌")
            planar, _ = nx.check_planarity(U)
            st.metric("Planar?", "Yes ✅" if planar else "No ❌")
            st.metric("Complete graph?", "Yes ✅" if U.number_of_edges() == len(U) * (len(U) - 1) // 2 else "No ❌")
            T.callout("Bipartite ⇔ 2-colourable ⇔ no odd cycle. Greedy colouring gives an upper bound on χ(G).")
