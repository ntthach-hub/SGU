from pathlib import Path

import networkx as nx
import numpy as np


def load_graph(file_path: str | Path) -> np.ndarray:
    file_path = Path(file_path)
    if file_path.suffix.lower() == ".csv":
        return np.loadtxt(file_path, delimiter=",")
    if file_path.suffix.lower() == ".txt":
        return load_edge_list(file_path)
    raise ValueError(f"Unsupported graph format: {file_path.suffix}")


def load_edge_list(file_path: str | Path) -> np.ndarray:
    edges = []
    max_node = -1

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            u_str, v_str, w_str = line.split()
            u, v, w = int(u_str), int(v_str), float(w_str)
            edges.append((u, v, w))
            max_node = max(max_node, u, v)

    matrix = np.zeros((max_node + 1, max_node + 1), dtype=float)
    for u, v, w in edges:
        matrix[u, v] = w
        matrix[v, u] = w
    return matrix


def create_graph_from_adjacency_matrix(matrix: np.ndarray) -> nx.Graph:
    graph = nx.Graph()
    num_nodes = matrix.shape[0]
    graph.add_nodes_from(range(num_nodes))

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            weight = float(matrix[i, j])
            if weight > 0:
                graph.add_edge(i, j, weight=weight)

    if not nx.is_connected(graph):
        raise ValueError("Input graph must be connected.")

    return graph


def path_length(graph: nx.Graph, path: list[int]) -> float:
    if len(path) < 2:
        return float("inf")

    return sum(graph[u][v]["weight"] for u, v in zip(path[:-1], path[1:]))


def dijkstra_shortest_path(
    graph: nx.Graph, source: int, destination: int
) -> tuple[list[int], float]:
    path = nx.shortest_path(graph, source=source, target=destination, weight="weight")
    distance = nx.shortest_path_length(
        graph,
        source=source,
        target=destination,
        weight="weight",
    )
    return list(path), float(distance)
