from .algorithms.avoa import AVOA
from .algorithms.pso import PSO
from .objective_functions import sphere, rastrigin, ackley
from .visualize import plot_convergence, plot_comparison


def run_single_algorithm(optimizer_class, algo_name, func, func_name, lb, ub, dim, pop_size, max_iter):
    optimizer = optimizer_class(
        obj_func=func,
        lb=lb,
        ub=ub,
        dim=dim,
        pop_size=pop_size,
        max_iter=max_iter
    )

    best_solution, best_fitness, convergence_curve = optimizer.optimize()

    print(f"\n===== {algo_name} on {func_name.upper()} =====")
    print("Best Solution:")
    print(best_solution)
    print(f"Best Fitness: {best_fitness:.10f}")

    plot_convergence(
        convergence_curve,
        title=f"{algo_name} on {func_name.capitalize()} Function",
        save_path=f"foundation of artificial intelligence/AVOA_Project/results/{algo_name.lower()}/{func_name}_convergence.png"
    )

    return best_solution, best_fitness, convergence_curve


def compare_avoa_pso_on_function(func, func_name, lb, ub, dim, pop_size, max_iter):
    print(f"\n========== COMPARING ON {func_name.upper()} ==========")

    _, avoa_fit, avoa_curve = run_single_algorithm(
        AVOA, "AVOA", func, func_name, lb, ub, dim, pop_size, max_iter
    )

    _, pso_fit, pso_curve = run_single_algorithm(
        PSO, "PSO", func, func_name, lb, ub, dim, pop_size, max_iter
    )

    plot_comparison(
        {
            "AVOA": avoa_curve,
            "PSO": pso_curve
        },
        title=f"AVOA vs PSO on {func_name.capitalize()} Function",
        save_path=f"foundation of artificial intelligence/AVOA_Project/results/comparison/{func_name}_comparison.png"
    )

    print("\n===== COMPARISON SUMMARY =====")
    print(f"Function: {func_name}")
    print(f"AVOA Best Fitness: {avoa_fit:.10f}")
    print(f"PSO  Best Fitness: {pso_fit:.10f}")


def run_all_experiments():
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
        compare_avoa_pso_on_function(func, func_name, lb, ub, dim, pop_size, max_iter)