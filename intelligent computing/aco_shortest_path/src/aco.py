import networkx as nx
import numpy as np

from src.ant import Ant
from src.config import ACOConfig


class AntColonyOptimizer:
    def __init__(self, graph: nx.Graph, config: ACOConfig) -> None:
        self.graph = graph
        self.config = config
        self.num_nodes = graph.number_of_nodes()
        self.rng = np.random.default_rng(config.random_seed)
        self.pheromone = np.zeros((self.num_nodes, self.num_nodes), dtype=float)
        self._initialize_pheromone()

    def _initialize_pheromone(self) -> None:
        for u, v in self.graph.edges():
            self.pheromone[u, v] = self.config.initial_pheromone
            self.pheromone[v, u] = self.config.initial_pheromone

    def run(self) -> tuple[list[int], float, list[float]]:
        best_path: list[int] = []
        best_distance = float("inf")
        convergence_history: list[float] = []

        max_steps = self.num_nodes * self.config.max_steps_factor

        for _ in range(self.config.num_iterations):
            all_paths: list[tuple[list[int], float]] = []

            for _ in range(self.config.num_ants):
                ant = Ant(
                    graph=self.graph,
                    source=self.config.source,
                    destination=self.config.destination,
                    alpha=self.config.alpha,
                    beta=self.config.beta,
                    rng=self.rng,
                )
                path, distance = ant.construct_solution(self.pheromone, max_steps=max_steps)
                if path:
                    all_paths.append((path, distance))
                    if distance < best_distance:
                        best_path = path.copy()
                        best_distance = distance

            self._update_pheromone(all_paths)
            convergence_history.append(best_distance)

        if not best_path:
            raise RuntimeError("ACO could not find a feasible path from source to destination.")

        return best_path, best_distance, convergence_history

    def _update_pheromone(self, paths: list[tuple[list[int], float]]) -> None:
        self.pheromone *= 1.0 - self.config.evaporation_rate

        for path, distance in paths:
            deposit = self.config.q / distance
            for u, v in zip(path[:-1], path[1:]):
                self.pheromone[u, v] += deposit
                self.pheromone[v, u] += deposit
