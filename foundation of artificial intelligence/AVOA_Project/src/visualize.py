import os
import matplotlib.pyplot as plt


def plot_convergence(curve, title="Convergence Curve", save_path=None):
    plt.figure(figsize=(8, 5))
    plt.plot(curve, linewidth=2)
    plt.title(title)
    plt.xlabel("Iteration")
    plt.ylabel("Best Fitness")
    plt.grid(True)
    plt.tight_layout()

    if save_path:
        folder = os.path.dirname(save_path)
        if folder:
            os.makedirs(folder, exist_ok=True)
        plt.savefig(save_path, dpi=300)
        print(f"Saved figure to: {os.path.abspath(save_path)}")

    plt.show()