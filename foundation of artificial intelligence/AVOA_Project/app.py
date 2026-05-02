from __future__ import annotations

from pathlib import Path
from time import perf_counter

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from src.algorithms.avoa import AVOA
from src.algorithms.pso import PSO
from src.objective_functions import ackley, rastrigin, sphere
from src.visualize import plot_comparison, plot_convergence


PROJECT_ROOT = Path(__file__).resolve().parent
BENCHMARKS = {
    "Sphere": sphere,
    "Rastrigin": rastrigin,
    "Ackley": ackley,
}


def run_optimizer(optimizer_class, func, lb, ub, dim, pop_size, max_iter, random_seed):
    optimizer = optimizer_class(
        obj_func=func,
        lb=lb,
        ub=ub,
        dim=dim,
        pop_size=pop_size,
        max_iter=max_iter,
        random_seed=random_seed,
        verbose=False,
    )
    start = perf_counter()
    best_solution, best_fitness, curve = optimizer.optimize()
    runtime = perf_counter() - start
    return optimizer, best_solution, best_fitness, curve, runtime


def build_contour_grid(func, dim, lb, ub, grid_points=120):
    x_values = np.linspace(lb, ub, grid_points)
    y_values = np.linspace(lb, ub, grid_points)
    grid_x, grid_y = np.meshgrid(x_values, y_values)
    contour_z = np.zeros_like(grid_x)

    for row_index in range(grid_x.shape[0]):
        for col_index in range(grid_x.shape[1]):
            point = np.zeros(dim)
            point[0] = grid_x[row_index, col_index]
            point[1] = grid_y[row_index, col_index]
            contour_z[row_index, col_index] = func(point)

    return grid_x, grid_y, contour_z


def plot_vulture_movement(
    func,
    dim,
    population_history,
    best_position_history,
    lb,
    ub,
    selected_iteration,
    tracked_vultures,
):
    fig, ax = plt.subplots(figsize=(8, 6))
    cmap = plt.cm.get_cmap("tab20", len(population_history[0]))
    upto_iteration = min(selected_iteration, len(population_history) - 1)
    vultures_to_plot = min(tracked_vultures, len(population_history[0]))
    grid_x, grid_y, contour_z = build_contour_grid(func, dim, lb, ub)

    contour_fill = ax.contourf(
        grid_x,
        grid_y,
        contour_z,
        levels=25,
        cmap="YlGnBu_r",
        alpha=0.75,
    )
    ax.contour(
        grid_x,
        grid_y,
        contour_z,
        levels=12,
        colors="white",
        linewidths=0.5,
        alpha=0.45,
    )
    fig.colorbar(contour_fill, ax=ax, label="Objective value")

    for vulture_index in range(vultures_to_plot):
        trajectory = np.array(
            [population_history[step][vulture_index, :2] for step in range(upto_iteration + 1)]
        )
        ax.plot(
            trajectory[:, 0],
            trajectory[:, 1],
            color=cmap(vulture_index),
            linewidth=1.2,
            alpha=0.7,
        )
        ax.scatter(
            trajectory[-1, 0],
            trajectory[-1, 1],
            color=cmap(vulture_index),
            s=35,
        )

    best_point = best_position_history[upto_iteration][:2]
    ax.scatter(
        best_point[0],
        best_point[1],
        marker="*",
        s=220,
        color="red",
        edgecolors="black",
        linewidths=0.8,
        label="Best solution so far",
    )

    ax.set_xlim(lb, ub)
    ax.set_ylim(lb, ub)
    ax.set_xlabel("Dimension 1")
    ax.set_ylabel("Dimension 2")
    ax.set_title(f"Vulture movement up to iteration {upto_iteration}")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return fig


def main() -> None:
    st.set_page_config(page_title="AVOA Benchmark App", layout="wide")
    st.title("African Vultures Optimization Algorithm")
    st.caption("Giao dien Streamlit de chay AVOA tren ham benchmark va so sanh voi PSO.")

    st.sidebar.header("Cau hinh")
    benchmark_name = st.sidebar.selectbox("Ham benchmark", list(BENCHMARKS))
    dim = st.sidebar.slider("So chieu", min_value=2, max_value=100, value=30, step=1)
    pop_size = st.sidebar.slider("Kich thuoc quan the", min_value=5, max_value=200, value=40, step=5)
    max_iter = st.sidebar.slider("So vong lap", min_value=10, max_value=500, value=150, step=10)
    lower_bound = st.sidebar.number_input("Can duoi", value=-10.0, step=1.0)
    upper_bound = st.sidebar.number_input("Can tren", value=10.0, step=1.0)
    random_seed = st.sidebar.number_input("Random seed", min_value=0, max_value=100000, value=42, step=1)
    compare_with_pso = st.sidebar.checkbox("So sanh voi PSO", value=True)

    if lower_bound >= upper_bound:
        st.error("Can duoi phai nho hon can tren.")
        return

    function = BENCHMARKS[benchmark_name]
    st.info("Ca ba ham benchmark nay deu co nghiem toi uu ly thuyet bang 0 tai vector 0.")

    if not st.button("Chay toi uu", type="primary", use_container_width=True):
        return

    with st.spinner("Dang chay thuat toan..."):
        avoa_optimizer, avoa_solution, avoa_fitness, avoa_curve, avoa_runtime = run_optimizer(
            AVOA,
            function,
            lower_bound,
            upper_bound,
            dim,
            pop_size,
            max_iter,
            int(random_seed),
        )

        pso_result = None
        if compare_with_pso:
            pso_result = run_optimizer(
                PSO,
                function,
                lower_bound,
                upper_bound,
                dim,
                pop_size,
                max_iter,
                int(random_seed),
            )

    metrics = st.columns(4 if pso_result else 2)
    metrics[0].metric("AVOA best fitness", f"{avoa_fitness:.10f}")
    metrics[1].metric("AVOA runtime", f"{avoa_runtime:.6f}s")
    if pso_result:
        metrics[2].metric("PSO best fitness", f"{pso_result[2]:.10f}")
        metrics[3].metric("PSO runtime", f"{pso_result[4]:.6f}s")

    st.subheader("Best solution")
    st.code(str(avoa_solution.tolist()), language="python")

    convergence_fig = plot_convergence(
        avoa_curve,
        title=f"AVOA on {benchmark_name}",
        show=False,
    )
    st.pyplot(convergence_fig, use_container_width=True)
    plt.close(convergence_fig)

    st.subheader("Cach ken ken di chuyen")
    st.caption("Bieu do duoi day chieu cac ca the xuong 2 chieu dau tien de quan sat quy dao.")
    if dim > 2:
        st.info("Bai toan dang co nhieu hon 2 chieu, vi vay Streamlit dang hien thi 2 chieu dau tien.")

    selected_iteration = st.slider(
        "Xem den iteration",
        min_value=0,
        max_value=len(avoa_optimizer.population_history) - 1,
        value=min(10, len(avoa_optimizer.population_history) - 1),
        step=1,
    )
    tracked_vultures = st.slider(
        "So ken ken hien thi",
        min_value=1,
        max_value=pop_size,
        value=min(20, pop_size),
        step=1,
    )
    movement_fig = plot_vulture_movement(
        function,
        dim,
        avoa_optimizer.population_history,
        avoa_optimizer.best_position_history,
        lower_bound,
        upper_bound,
        selected_iteration,
        tracked_vultures,
    )
    st.pyplot(movement_fig, use_container_width=True)
    plt.close(movement_fig)

    if pso_result:
        comparison_fig = plot_comparison(
            {"AVOA": avoa_curve, "PSO": pso_result[3]},
            title=f"AVOA vs PSO on {benchmark_name}",
            show=False,
        )
        st.pyplot(comparison_fig, use_container_width=True)
        plt.close(comparison_fig)

        gap = avoa_fitness - pso_result[2]
        if gap < 0:
            st.success(f"AVOA tot hon PSO o lan chay nay, chenh lech {abs(gap):.10f}.")
        elif gap > 0:
            st.warning(f"PSO tot hon AVOA o lan chay nay, chenh lech {gap:.10f}.")
        else:
            st.info("AVOA va PSO cho cung fitness trong lan chay nay.")

    report_lines = [
        f"Benchmark: {benchmark_name}",
        f"Dimension: {dim}",
        f"Bounds: [{lower_bound}, {upper_bound}]",
        f"Population size: {pop_size}",
        f"Iterations: {max_iter}",
        f"Seed: {int(random_seed)}",
        f"AVOA best fitness: {avoa_fitness:.10f}",
        f"AVOA runtime: {avoa_runtime:.6f}s",
        f"AVOA best solution: {avoa_solution.tolist()}",
    ]
    if pso_result:
        report_lines.extend(
            [
                f"PSO best fitness: {pso_result[2]:.10f}",
                f"PSO runtime: {pso_result[4]:.6f}s",
            ]
        )
    report_text = "\n".join(report_lines)

    st.download_button(
        label="Tai bao cao text",
        data=report_text,
        file_name=f"{benchmark_name.lower()}_report.txt",
        mime="text/plain",
    )


if __name__ == "__main__":
    main()
