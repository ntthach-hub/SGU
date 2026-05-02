import numpy as np


class PSO:
    """Simple PSO baseline for benchmark comparison."""

    def __init__(
        self,
        obj_func,
        lb,
        ub,
        dim,
        pop_size=30,
        max_iter=100,
        w=0.7,
        c1=1.5,
        c2=1.5,
        random_seed=None,
        verbose=True,
    ):
        self.obj_func = obj_func
        self.lb = lb
        self.ub = ub
        self.dim = dim
        self.pop_size = pop_size
        self.max_iter = max_iter
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.verbose = verbose
        self.rng = np.random.default_rng(random_seed)

        self.positions = None
        self.velocities = None
        self.fitness = None
        self.pbest_positions = None
        self.pbest_fitness = None
        self.gbest_position = None
        self.gbest_fitness = np.inf
        self.convergence_curve = []

    def initialize(self):
        self.positions = self.rng.uniform(
            low=self.lb,
            high=self.ub,
            size=(self.pop_size, self.dim),
        )
        self.velocities = self.rng.uniform(
            low=-abs(self.ub - self.lb),
            high=abs(self.ub - self.lb),
            size=(self.pop_size, self.dim),
        ) * 0.1

        self.fitness = np.array([self.obj_func(x) for x in self.positions])
        self.pbest_positions = self.positions.copy()
        self.pbest_fitness = self.fitness.copy()

        best_idx = np.argmin(self.fitness)
        self.gbest_position = self.positions[best_idx].copy()
        self.gbest_fitness = self.fitness[best_idx]
        self.convergence_curve = []

    def clip_position(self, x):
        return np.clip(x, self.lb, self.ub)

    def optimize(self):
        self.initialize()

        for t in range(self.max_iter):
            for i in range(self.pop_size):
                r1 = self.rng.random(self.dim)
                r2 = self.rng.random(self.dim)

                self.velocities[i] = (
                    self.w * self.velocities[i]
                    + self.c1 * r1 * (self.pbest_positions[i] - self.positions[i])
                    + self.c2 * r2 * (self.gbest_position - self.positions[i])
                )

                self.positions[i] = self.positions[i] + self.velocities[i]
                self.positions[i] = self.clip_position(self.positions[i])

                current_fitness = self.obj_func(self.positions[i])

                if current_fitness < self.pbest_fitness[i]:
                    self.pbest_fitness[i] = current_fitness
                    self.pbest_positions[i] = self.positions[i].copy()

                if current_fitness < self.gbest_fitness:
                    self.gbest_fitness = current_fitness
                    self.gbest_position = self.positions[i].copy()

            self.convergence_curve.append(self.gbest_fitness)

            if self.verbose:
                print(
                    f"PSO Iteration {t + 1}/{self.max_iter}, "
                    f"Best Fitness = {self.gbest_fitness:.6f}"
                )

        return self.gbest_position, self.gbest_fitness, self.convergence_curve
