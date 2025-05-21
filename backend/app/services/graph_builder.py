# backend/app/services/graph_builder.py

import networkx as nx
from typing import List, Dict

def build_graph_from_triplets(triplets: List[Dict]) -> nx.DiGraph:
    G = nx.DiGraph()

    for triplet in triplets:
        subject = triplet["subject"]
        predicate = triplet["predicate"]
        obj = triplet["object"]

        G.add_node(subject)
        G.add_node(obj)
        G.add_edge(subject, obj, label=predicate)

    return G

def export_graph_as_edges(graph: nx.DiGraph) -> List[Dict]:
    edges = []
    for u, v, data in graph.edges(data=True):
        edges.append({
            "from": u,
            "to": v,
            "relation": data.get("label", "")
        })
    return edges
