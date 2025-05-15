# backend/test_graph_output.py

from app.services.graph_builder import build_graph_from_triplets
from app.services.graph_visualizer import visualize_graph

triplets = [
    {"subject": "Ali", "predicate": "recommend", "object": "FastAPI"},
    {"subject": "Erdem", "predicate": "build", "object": "memory system"},
    {"subject": "memory system", "predicate": "store", "object": "triplets"}
]

graph = build_graph_from_triplets(triplets)
visualize_graph(graph, output_path="triplet_graph.html")
