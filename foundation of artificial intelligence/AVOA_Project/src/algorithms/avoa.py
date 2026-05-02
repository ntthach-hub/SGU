import numpy as np


class AVOA:
    """
    Simplified African Vultures Optimization Algorithm (AVOA).

    This implementation is suitable for learning and benchmark demos.
    It is not a paper-exact reproduction of every AVOA strategy.
    """

    def __init__(
        self,
        obj_func,
        lb,
        ub,
        dim,
        pop_size=30,
        max_iter=100,
        random_seed=None,
        verbose=True,
    ):
        self.obj_func = obj_func
        self.lb = lb
        self.ub = ub
        self.dim = dim
        self.pop_size = pop_size
        self.max_iter = max_iter
        self.verbose = verbose
        self.rng = np.random.default_rng(random_seed)

        self.population = None
        self.fitness = None
        self.best_solution = None
        self.best_fitness = np.inf
        self.convergence_curve = []
        self.population_history = []
        self.best_position_history = []

    def initialize_population(self):
        self.population = self.rng.uniform(
            low=self.lb,
            high=self.ub,
            size=(self.pop_size, self.dim),
        )

    def evaluate_population(self):
        self.fitness = np.array([self.obj_func(individual) for individual in self.population])

    def update_best_solution(self):
        min_idx = np.argmin(self.fitness)
        current_best_fitness = self.fitness[min_idx]

        if current_best_fitness < self.best_fitness:
            self.best_fitness = current_best_fitness
            self.best_solution = self.population[min_idx].copy()

    def get_two_best_vultures(self):
        sorted_indices = np.argsort(self.fitness)
        best1 = self.population[sorted_indices[0]].copy()
        best2 = self.population[sorted_indices[1]].copy()
        return best1, best2

    def clip_position(self, position):
        return np.clip(position, self.lb, self.ub)

    def optimize(self):
        self.best_solution = None
        self.best_fitness = np.inf
        self.convergence_curve = []
        self.population_history = []
        self.best_position_history = []

        self.initialize_population()
        self.evaluate_population()
        self.update_best_solution()
        self.population_history.append(self.population.copy())
        self.best_position_history.append(self.best_solution.copy())

        for t in range(self.max_iter):
            best1, best2 = self.get_two_best_vultures()
            a = 2 - 2 * (t / self.max_iter)
            new_population = np.zeros_like(self.population)

            for i in range(self.pop_size):
                current = self.population[i].copy()
                leader = best1 if self.rng.random() < 0.5 else best2
                f_value = a * (2 * self.rng.random() - 1)
                rand_vec = self.rng.random(self.dim)

                if abs(f_value) >= 1:
                    random_vulture = self.population[self.rng.integers(self.pop_size)]
                    new_position = (
                        leader
                        - np.abs(rand_vec * leader - current) * f_value
                        + self.rng.random(self.dim) * (random_vulture - current)
                    )
                else:
                    new_position = leader - f_value * np.abs(leader - current)
                    new_position = new_position + 0.01 * self.rng.standard_normal(self.dim)

                new_population[i] = self.clip_position(new_position)

            self.population = new_population
            self.evaluate_population()
            self.update_best_solution()
            self.convergence_curve.append(self.best_fitness)
            self.population_history.append(self.population.copy())
            self.best_position_history.append(self.best_solution.copy())

            if self.verbose:
                print(
                    f"Iteration {t + 1}/{self.max_iter}, "
                    f"Best Fitness = {self.best_fitness:.6f}"
                )

        return self.best_solution, self.best_fitness, self.convergence_curve
