from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from time import perf_counter

import streamlit as st

from main import save_comparison_report
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
)


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_GRAPH_PATH = DATA_DIR / "sample_matrix.csv"


def build_config(
    num_ants: int,
    num_iterations: int,
    alpha: float,
    beta: float,
    evaporation_rate: float,
    q: float,
    initial_pheromone: float,
    max_steps_factor: int,
    source: int,
    destination: int,
    random_seed: int,
) -> ACOConfig:
    return ACOConfig(
        num_ants=num_ants,
        num_iterations=num_iterations,
        alpha=alpha,
        beta=beta,
        evaporation_rate=evaporation_rate,
        q=q,
        initial_pheromone=initial_pheromone,
        max_steps_factor=max_steps_factor,
        source=source,
        destination=destination,
        random_seed=random_seed,
    )


def load_graph_from_upload(uploaded_file) -> tuple:
    suffix = Path(uploaded_file.name).suffix.lower()
    temp_path = PROJECT_ROOT / f".streamlit_upload{suffix}"
    temp_path.write_bytes(uploaded_file.getvalue())
    try:
        matrix = load_graph(temp_path)
    finally:
        temp_path.unlink(missing_ok=True)
    return matrix, uploaded_file.name


def load_selected_graph(input_mode: str, uploaded_file) -> tuple:
    if input_mode == "Mau co san":
        return load_graph(DEFAULT_GRAPH_PATH), DEFAULT_GRAPH_PATH.name

    if uploaded_file is None:
        raise ValueError("Hay tai len file .csv hoac .txt de tiep tuc.")

    return load_graph_from_upload(uploaded_file)


def render_sidebar(num_nodes: int) -> ACOConfig:
    st.sidebar.header("Cau hinh ACO")
    num_ants = st.sidebar.slider("So kien", min_value=5, max_value=200, value=20, step=5)
    num_iterations = st.sidebar.slider(
        "So vong lap", min_value=10, max_value=500, value=100, step=10
    )
    alpha = st.sidebar.slider("Alpha", min_value=0.1, max_value=5.0, value=1.0, step=0.1)
    beta = st.sidebar.slider("Beta", min_value=0.1, max_value=8.0, value=3.0, step=0.1)
    evaporation_rate = st.sidebar.slider(
        "Ti le bay hoi pheromone",
        min_value=0.01,
        max_value=0.95,
        value=0.30,
        step=0.01,
    )
    q = st.sidebar.number_input("Q", min_value=1.0, max_value=10000.0, value=100.0, step=10.0)
    initial_pheromone = st.sidebar.number_input(
        "Pheromone ban dau",
        min_value=0.01,
        max_value=100.0,
        value=1.0,
        step=0.1,
    )
    max_steps_factor = st.sidebar.slider(
        "He so gioi han buoc", min_value=1, max_value=10, value=3, step=1
    )
    source = st.sidebar.number_input(
        "Dinh nguon", min_value=0, max_value=max(0, num_nodes - 1), value=0, step=1
    )
    default_destination = min(max(1, num_nodes - 1), max(0, num_nodes - 1))
    destination = st.sidebar.number_input(
        "Dinh dich",
        min_value=0,
        max_value=max(0, num_nodes - 1),
        value=default_destination,
        step=1,
    )
    random_seed = st.sidebar.number_input(
        "Random seed", min_value=0, max_value=100000, value=42, step=1
    )

    return build_config(
        num_ants=num_ants,
        num_iterations=num_iterations,
        alpha=alpha,
        beta=beta,
        evaporation_rate=evaporation_rate,
        q=q,
        initial_pheromone=initial_pheromone,
        max_steps_factor=max_steps_factor,
        source=int(source),
        destination=int(destination),
        random_seed=int(random_seed),
    )


def main() -> None:
    st.set_page_config(
        page_title="ACO Shortest Path",
        layout="wide",
    )
    st.title("Ant Colony Optimization for Shortest Path")
    st.caption("Giao dien Streamlit de chay ACO, so sanh voi Dijkstra va xem ket qua truc quan.")

    input_mode = st.radio(
        "Chon du lieu dau vao",
        options=["Mau co san", "Tai file len"],
        horizontal=True,
    )
    uploaded_file = None
    if input_mode == "Tai file len":
        uploaded_file = st.file_uploader(
            "Tai len file do thi (.csv ma tran ke hoac .txt danh sach canh)",
            type=["csv", "txt"],
        )

    try:
        matrix, data_label = load_selected_graph(input_mode, uploaded_file)
        graph = create_graph_from_adjacency_matrix(matrix)
    except Exception as exc:
        st.error(f"Khong the tai do thi: {exc}")
        return

    st.info(
        f"Da nap du lieu `{data_label}` voi {graph.number_of_nodes()} dinh va {graph.number_of_edges()} canh."
    )
    st.dataframe(matrix, use_container_width=True)

    config = render_sidebar(graph.number_of_nodes())
    if config.source == config.destination:
        st.warning("Dinh nguon va dinh dich dang trung nhau. Hay chon hai dinh khac nhau.")
        return

    run_clicked = st.button("Chay ACO", type="primary", use_container_width=True)
    if not run_clicked:
        return

    with st.spinner("Dang toi uu duong di..."):
        try:
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
        except Exception as exc:
            st.error(f"Khong the chay thuat toan: {exc}")
            return

    metric_columns = st.columns(4)
    metric_columns[0].metric("ACO distance", f"{best_distance:.4f}")
    metric_columns[1].metric("Dijkstra distance", f"{dijkstra_distance:.4f}")
    metric_columns[2].metric("ACO runtime", f"{aco_time:.6f}s")
    metric_columns[3].metric("Dijkstra runtime", f"{dijkstra_time:.6f}s")

    result_columns = st.columns(2)
    result_columns[0].markdown(f"**ACO path:** `{' -> '.join(map(str, best_path))}`")
    result_columns[1].markdown(f"**Dijkstra path:** `{' -> '.join(map(str, dijkstra_path))}`")

    with TemporaryDirectory() as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        convergence_path = temp_dir / "convergence.png"
        graph_path = temp_dir / "graph_result.png"
        comparison_path = temp_dir / "comparison_chart.png"
        report_path = temp_dir / "comparison_report.txt"

        plot_convergence(history, convergence_path)
        plot_graph_with_path(graph, best_path, graph_path)
        plot_algorithm_comparison(
            aco_distance=best_distance,
            dijkstra_distance=dijkstra_distance,
            aco_time=aco_time,
            dijkstra_time=dijkstra_time,
            output_path=comparison_path,
        )
        save_comparison_report(
            output_path=report_path,
            aco_path=best_path,
            aco_distance=best_distance,
            aco_time=aco_time,
            dijkstra_path=dijkstra_path,
            dijkstra_distance=dijkstra_distance,
            dijkstra_time=dijkstra_time,
        )

        chart_columns = st.columns(2)
        chart_columns[0].image(str(convergence_path), caption="ACO convergence", use_container_width=True)
        chart_columns[1].image(str(graph_path), caption="Do thi va duong di tot nhat", use_container_width=True)
        st.image(str(comparison_path), caption="So sanh ACO va Dijkstra", use_container_width=True)

        report_text = report_path.read_text(encoding="utf-8")
        st.subheader("Bao cao so sanh")
        st.code(report_text, language="text")
        st.download_button(
            label="Tai comparison_report.txt",
            data=report_text,
            file_name="comparison_report.txt",
            mime="text/plain",
        )


if __name__ == "__main__":
    main()
