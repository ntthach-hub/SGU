from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx


def save_best_path(
    output_path: str | Path,
    best_path: list[int],
    best_distance: float,
    source: int,
    destination: int,
) -> None:
    output_path = Path(output_path)
    path_str = " -> ".join(map(str, best_path))
    content = [
        "Ant Colony Optimization - Shortest Path Result",
        f"Source: {source}",
        f"Destination: {destination}",
        f"Best path: {path_str}",
        f"Best distance: {best_distance:.4f}",
    ]
    output_path.write_text("\n".join(content), encoding="utf-8")


def plot_convergence(history: list[float], output_path: str | Path) -> None:
    output_path = Path(output_path)
    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(history) + 1), history, color="#1f77b4", linewidth=2)
    plt.xlabel("Iteration")
    plt.ylabel("Best Distance")
    plt.title("ACO Convergence")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_graph_with_path(graph: nx.Graph, path: list[int], output_path: str | Path) -> None:
    output_path = Path(output_path)
    pos = nx.spring_layout(graph, seed=7)
    edge_labels = nx.get_edge_attributes(graph, "weight")
    highlighted_edges = list(zip(path[:-1], path[1:]))

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(graph, pos, node_color="#d9edf7", node_size=900, edgecolors="#1b4f72")
    nx.draw_networkx_labels(graph, pos, font_size=11, font_weight="bold")
    nx.draw_networkx_edges(graph, pos, width=1.8, edge_color="#7f8c8d")
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=9)

    if highlighted_edges:
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=highlighted_edges,
            width=4,
            edge_color="#e74c3c",
        )

    plt.title("Shortest Path Found by ACO")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    plt.close()


def plot_algorithm_comparison(
    aco_distance: float,
    dijkstra_distance: float,
    aco_time: float,
    dijkstra_time: float,
    output_path: str | Path,
) -> None:
    output_path = Path(output_path)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))

    algorithms = ["ACO", "Dijkstra"]
    distance_values = [aco_distance, dijkstra_distance]
    time_values = [aco_time, dijkstra_time]
    colors = ["#e67e22", "#2980b9"]

    axes[0].bar(algorithms, distance_values, color=colors, width=0.55)
    axes[0].set_title("Distance Comparison")
    axes[0].set_ylabel("Total Distance")
    axes[0].grid(axis="y", linestyle="--", alpha=0.4)

    axes[1].bar(algorithms, time_values, color=colors, width=0.55)
    axes[1].set_title("Runtime Comparison")
    axes[1].set_ylabel("Seconds")
    axes[1].grid(axis="y", linestyle="--", alpha=0.4)

    for ax, values in zip(axes, [distance_values, time_values]):
        for index, value in enumerate(values):
            ax.text(index, value, f"{value:.4f}", ha="center", va="bottom", fontsize=9)

    fig.suptitle("ACO vs Dijkstra")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)
