from avoa import AVOA
from objective_functions import sphere
from visualize import plot_convergence


def main():
    # =========================
    # Thiết lập tham số bài toán
    # =========================
    lb = -10
    ub = 10
    dim = 30
    pop_size = 50
    max_iter = 300

    # =========================
    # Khởi tạo thuật toán AVOA
    # =========================
    optimizer = AVOA(
        obj_func=sphere,
        lb=lb,
        ub=ub,
        dim=dim,
        pop_size=pop_size,
        max_iter=max_iter
    )

    # =========================
    # Chạy tối ưu
    # =========================
    best_solution, best_fitness, convergence_curve = optimizer.optimize()

    # =========================
    # In kết quả
    # =========================
    print("\n===== FINAL RESULT =====")
    print("Best Solution:")
    print(best_solution)
    print(f"Best Fitness: {best_fitness:.10f}")

    # =========================
    # Vẽ đồ thị hội tụ
    # =========================
    plot_convergence(
    convergence_curve,
    title="AVOA on Sphere Function",
    save_path="foundation of artificial intelligence/AVOA_Project/results/sphere_convergence.png"
    )
if __name__ == "__main__":
    main()