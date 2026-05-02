import os

import matplotlib.pyplot as plt


def plot_convergence(curve, title="Convergence Curve", save_path=None, show=True):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(curve, linewidth=2)
    ax.set_title(title)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Best Fitness")
    ax.grid(True)
    fig.tight_layout()

    if save_path:
        folder = os.path.dirname(str(save_path))
        if folder:
            os.makedirs(folder, exist_ok=True)
        fig.savefig(save_path, dpi=300)
        print(f"Saved figure to: {os.path.abspath(str(save_path))}")

    if show:
        plt.show()
    return fig


def plot_comparison(curves_dict, title="Algorithm Comparison", save_path=None, show=True):
    fig, ax = plt.subplots(figsize=(9, 5))

    for label, curve in curves_dict.items():
        ax.plot(curve, linewidth=2, label=label)

    ax.set_title(title)
    ax.set_xlabel("Iteration")
    ax.set_ylabel("Best Fitness")
    ax.grid(True)
    ax.legend()
    fig.tight_layout()

    if save_path:
        folder = os.path.dirname(str(save_path))
        if folder:
            os.makedirs(folder, exist_ok=True)
        fig.savefig(save_path, dpi=300)
        print(f"Saved comparison figure to: {os.path.abspath(str(save_path))}")

    if show:
        plt.show()
    return fig
