from pathlib import Path

from src.aco import AntColonyOptimizer
from src.config import ACOConfig
from src.graph_utils import create_graph_from_adjacency_matrix, load_graph
from src.visualize import plot_convergence, plot_graph_with_path, save_best_path


def main() -> None:
    project_root = Path(__file__).resolve().parent
    data_dir = project_root / "data"
    results_dir = project_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    config = ACOConfig()
    graph = load_graph(data_dir / "sample_matrix.csv")
    graph = create_graph_from_adjacency_matrix(graph)

    optimizer = AntColonyOptimizer(graph=graph, config=config)
    best_path, best_distance, history = optimizer.run()

    save_best_path(
        output_path=results_dir / "best_path.txt",
        best_path=best_path,
        best_distance=best_distance,
        source=config.source,
        destination=config.destination,
    )
    plot_convergence(history, results_dir / "convergence.png")
    plot_graph_with_path(graph, best_path, results_dir / "graph_result.png")

    path_str = " -> ".join(map(str, best_path))
    print(f"Best path: {path_str}")
    print(f"Best distance: {best_distance:.4f}")
    print(f"Results saved to: {results_dir}")


if __name__ == "__main__":
    main()
