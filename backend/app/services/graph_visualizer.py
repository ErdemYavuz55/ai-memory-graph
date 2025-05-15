# backend/app/services/graph_visualizer.py

from pyvis.network import Network
import networkx as nx

def visualize_graph(graph: nx.DiGraph, output_path="graph.html"):
    net = Network(height="600px", width="100%", directed=True)
    net.barnes_hut()  # güzel bir düzenleme algoritması

    for node in graph.nodes():
        net.add_node(node, label=node)

    for source, target, data in graph.edges(data=True):
        label = data.get("label", "")
        net.add_edge(source, target, label=label)

    net.write_html(output_path)
    import webbrowser
    webbrowser.open(output_path)

