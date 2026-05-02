from pathlib import Path

import matplotlib.pyplot as plt

from .algorithms.avoa import AVOA
from .algorithms.pso import PSO
from .objective_functions import ackley, rastrigin, sphere
from .visualize import plot_comparison, plot_convergence


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"


def run_single_algorithm(
    optimizer_class,
    algo_name,
    func,
    func_name,
    lb,
    ub,
    dim,
    pop_size,
    max_iter,
    random_seed=None,
    verbose=True,
):
    optimizer = optimizer_class(
        obj_func=func,
        lb=lb,
        ub=ub,
        dim=dim,
        pop_size=pop_size,
        max_iter=max_iter,
        random_seed=random_seed,
        verbose=verbose,
    )

    best_solution, best_fitness, convergence_curve = optimizer.optimize()

    print(f"\n===== {algo_name} on {func_name.upper()} =====")
    print("Best Solution:")
    print(best_solution)
    print(f"Best Fitness: {best_fitness:.10f}")

    convergence_fig = plot_convergence(
        convergence_curve,
        title=f"{algo_name} on {func_name.capitalize()} Function",
        save_path=RESULTS_DIR / algo_name.lower() / f"{func_name}_convergence.png",
        show=False,
    )
    plt.close(convergence_fig)

    return best_solution, best_fitness, convergence_curve


def compare_avoa_pso_on_function(
    func,
    func_name,
    lb,
    ub,
    dim,
    pop_size,
    max_iter,
    random_seed=None,
    verbose=True,
):
    print(f"\n========== COMPARING ON {func_name.upper()} ==========")

    _, avoa_fit, avoa_curve = run_single_algorithm(
        AVOA,
        "AVOA",
        func,
        func_name,
        lb,
        ub,
        dim,
        pop_size,
        max_iter,
        random_seed=random_seed,
        verbose=verbose,
    )

    _, pso_fit, pso_curve = run_single_algorithm(
        PSO,
        "PSO",
        func,
        func_name,
        lb,
        ub,
        dim,
        pop_size,
        max_iter,
        random_seed=random_seed,
        verbose=verbose,
    )

    comparison_fig = plot_comparison(
        {
            "AVOA": avoa_curve,
            "PSO": pso_curve,
        },
        title=f"AVOA vs PSO on {func_name.capitalize()} Function",
        save_path=RESULTS_DIR / "comparison" / f"{func_name}_comparison.png",
        show=False,
    )
    plt.close(comparison_fig)

    print("\n===== COMPARISON SUMMARY =====")
    print(f"Function: {func_name}")
    print(f"AVOA Best Fitness: {avoa_fit:.10f}")
    print(f"PSO  Best Fitness: {pso_fit:.10f}")


def run_all_experiments(random_seed=42, verbose=True):
    lb = -10
    ub = 10
    dim = 30
    pop_size = 40
    max_iter = 150

    benchmarks = [
        ("sphere", sphere),
        ("rastrigin", rastrigin),
        ("ackley", ackley),
    ]

    for func_name, func in benchmarks:
        compare_avoa_pso_on_function(
            func,
            func_name,
            lb,
            ub,
            dim,
            pop_size,
            max_iter,
            random_seed=random_seed,
            verbose=verbose,
        )
