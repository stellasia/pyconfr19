import networkx as nx
import community

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# ===========
# Load data
# ===========
G = nx.Graph()
edges = nx.read_edgelist('edges.csv', delimiter=",")
nodes = nx.read_adjlist("nodes.csv")
G.add_edges_from(edges.edges())
G.add_nodes_from(nodes)

# visualize graph
# ===========
layouts = {
    "circular": nx.circular_layout,
    "spectral": nx.spectral_layout,
    "spring": nx.spring_layout,
    "planar": nx.planar_layout,
    "random": nx.random_layout,
}

for name, func in layouts.items():
    pos = func(G)

    f = plt.figure()
    plt_nodes = nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=G.nodes,
        alpha=0.5,
    )
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=7)
    f.suptitle(f"Layout: {name}")
    f.savefig(f"graph_{name}.png")
    
# Kamada kawai
pos = nx.kamada_kawai_layout(G)

f = plt.figure()
plt_nodes = nx.draw_networkx_nodes(
    G,
    pos,
    nodelist=G.nodes,
    alpha=0.5,
)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=7)
f.savefig("graph_kk.png")


# ===========
# ANALYSIS
# ===========

# Page Rank
# ===========

res = nx.pagerank(G, alpha=0.9)

res_nodes = list(res.keys())
res_values = list(res.values())

f = plt.figure()
plt_nodes = nx.draw_networkx_nodes(G, pos,
        nodelist=res_nodes,
        node_color=res_values,
        alpha=0.5,
)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=7)
plt.colorbar(plt_nodes)
f.suptitle(f"Page Rank")
f.savefig("graph_pr.png")


# Louvain
# ===========
res = community.best_partition(G)

res_nodes = list(res.keys())
res_values = list(res.values())

f = plt.figure()
plt_nodes = nx.draw_networkx_nodes(G, pos,
        nodelist=res_nodes,
        node_color=res_values,
        cmap="tab20",
        alpha=0.5,
)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=7)
f.suptitle(f"Louvain")
f.savefig("graph_louvain.png")


# remove isolated nodes
G.remove_nodes_from(list(nx.isolates(G)))

res = community.best_partition(G)

res_nodes = list(res.keys())
res_values = list(res.values())

f = plt.figure()
plt_nodes = nx.draw_networkx_nodes(G, pos,
        nodelist=res_nodes,
        node_color=res_values,
        cmap="tab20",
        alpha=0.5,
)
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos, font_size=7)
f.suptitle(f"Louvain (no isolated nodes)")
f.savefig("graph_louvain_no_isolated.png")
