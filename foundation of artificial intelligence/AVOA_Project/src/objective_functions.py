import numpy as np


def sphere(x):
    """
    Hàm Sphere
    Global minimum tại x = [0, 0, ..., 0]
    f(x) = 0
    """
    return np.sum(x ** 2)


def rastrigin(x):
    """
    Hàm Rastrigin
    Global minimum tại x = [0, 0, ..., 0]
    f(x) = 0
    """
    n = len(x)
    return 10 * n + np.sum(x ** 2 - 10 * np.cos(2 * np.pi * x))


def rosenbrock(x):
    """
    Hàm Rosenbrock
    Global minimum tại x = [1, 1, ..., 1]
    f(x) = 0
    """
    return np.sum(100 * (x[1:] - x[:-1] ** 2) ** 2 + (x[:-1] - 1) ** 2)


def ackley(x):
    """
    Hàm Ackley
    Global minimum tại x = [0, 0, ..., 0]
    f(x) = 0
    """
    n = len(x)
    sum1 = np.sum(x ** 2)
    sum2 = np.sum(np.cos(2 * np.pi * x))

    term1 = -20 * np.exp(-0.2 * np.sqrt(sum1 / n))
    term2 = -np.exp(sum2 / n)

    return term1 + term2 + 20 + np.e