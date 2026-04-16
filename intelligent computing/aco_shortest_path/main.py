from time import perf_counter

from pathlib import Path

from src.aco import AntColonyOptimizer
from src.config import ACOConfig
from src.graph_utils import (
    create_graph_from_adjacency_matrix,
    dijkstra_shortest_path,
    load_graph,
)
from src.visualize import (
    plot_algorithm_comparison,
    plot_convergence,
    plot_graph_with_path,
    save_best_path,
)


def save_comparison_report(
    output_path: Path,
    aco_path: list[int],
    aco_distance: float,
    aco_time: float,
    dijkstra_path: list[int],
    dijkstra_distance: float,
    dijkstra_time: float,
) -> None:
    aco_path_str = " -> ".join(map(str, aco_path))
    dijkstra_path_str = " -> ".join(map(str, dijkstra_path))
    gap = aco_distance - dijkstra_distance
    accuracy = 0.0 if dijkstra_distance == 0 else (dijkstra_distance / aco_distance) * 100

    if abs(gap) < 1e-9:
        conclusion = "ACO tim duoc cung duong di toi uu nhu Dijkstra tren do thi mau."
    elif gap > 0:
        conclusion = (
            "ACO tim duoc nghiem gan toi uu, nhung van dai hon Dijkstra tren do thi mau."
        )
    else:
        conclusion = (
            "ACO cho ket qua nho hon Dijkstra, can kiem tra lai du lieu hoac cach danh gia."
        )

    lines = [
        "Comparison between ACO and Dijkstra",
        f"ACO path: {aco_path_str}",
        f"ACO distance: {aco_distance:.4f}",
        f"ACO runtime: {aco_time:.6f} seconds",
        "",
        f"Dijkstra path: {dijkstra_path_str}",
        f"Dijkstra distance: {dijkstra_distance:.4f}",
        f"Dijkstra runtime: {dijkstra_time:.6f} seconds",
        "",
        f"Distance gap (ACO - Dijkstra): {gap:.4f}",
        f"Relative quality of ACO: {accuracy:.2f}%",
        f"Conclusion: {conclusion}",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    project_root = Path(__file__).resolve().parent
    data_dir = project_root / "data"
    results_dir = project_root / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    config = ACOConfig()
    graph = load_graph(data_dir / "sample_matrix.csv")
    graph = create_graph_from_adjacency_matrix(graph)

    aco_start = perf_counter()
    optimizer = AntColonyOptimizer(graph=graph, config=config)
    best_path, best_distance, history = optimizer.run()
    aco_time = perf_counter() - aco_start

    dijkstra_start = perf_counter()
    dijkstra_path, dijkstra_distance = dijkstra_shortest_path(
        graph,
        source=config.source,
        destination=config.destination,
    )
    dijkstra_time = perf_counter() - dijkstra_start

    save_best_path(
        output_path=results_dir / "best_path.txt",
        best_path=best_path,
        best_distance=best_distance,
        source=config.source,
        destination=config.destination,
    )
    plot_convergence(history, results_dir / "convergence.png")
    plot_graph_with_path(graph, best_path, results_dir / "graph_result.png")
    plot_algorithm_comparison(
        aco_distance=best_distance,
        dijkstra_distance=dijkstra_distance,
        aco_time=aco_time,
        dijkstra_time=dijkstra_time,
        output_path=results_dir / "comparison_chart.png",
    )
    save_comparison_report(
        output_path=results_dir / "comparison_report.txt",
        aco_path=best_path,
        aco_distance=best_distance,
        aco_time=aco_time,
        dijkstra_path=dijkstra_path,
        dijkstra_distance=dijkstra_distance,
        dijkstra_time=dijkstra_time,
    )

    path_str = " -> ".join(map(str, best_path))
    print(f"Best path: {path_str}")
    print(f"Best distance: {best_distance:.4f}")
    print(f"Dijkstra distance: {dijkstra_distance:.4f}")
    print(f"Results saved to: {results_dir}")


if __name__ == "__main__":
    main()
