from .avoa import AVOA
from .objective_functions import sphere, rastrigin, ackley
from .visualize import plot_convergence


def run_experiment(func, func_name, lb, ub, dim, pop_size, max_iter):
    print(f"\n===== RUNNING: {func_name.upper()} =====")

    optimizer = AVOA(
        obj_func=func,
        lb=lb,
        ub=ub,
        dim=dim,
        pop_size=pop_size,
        max_iter=max_iter
    )

    best_solution, best_fitness, convergence_curve = optimizer.optimize()

    print("\n===== FINAL RESULT =====")
    print("Function:", func_name)
    print("Best Solution:")
    print(best_solution)
    print(f"Best Fitness: {best_fitness:.10f}")

    plot_convergence(
        convergence_curve,
        title=f"AVOA on {func_name.capitalize()} Function",
        save_path=f"foundation of artificial intelligence/AVOA_Project/results/{func_name}_convergence.png"
    )


def main():
    lb = -10
    ub = 10
    dim = 30
    pop_size = 50
    max_iter = 300

    benchmarks = [
        ("sphere", sphere),
        ("rastrigin", rastrigin),
        ("ackley", ackley),
    ]

    for func_name, func in benchmarks:
        run_experiment(func, func_name, lb, ub, dim, pop_size, max_iter)


if __name__ == "__main__":
    main()