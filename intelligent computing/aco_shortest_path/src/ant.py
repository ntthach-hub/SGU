from dataclasses import dataclass, field

import networkx as nx
import numpy as np

from src.graph_utils import path_length


@dataclass
class Ant:
    graph: nx.Graph
    source: int
    destination: int
    alpha: float
    beta: float
    rng: np.random.Generator
    path: list[int] = field(default_factory=list)
    visited: set[int] = field(default_factory=set)

    def construct_solution(self, pheromone: np.ndarray, max_steps: int) -> tuple[list[int], float]:
        self.path = [self.source]
        self.visited = {self.source}
        current = self.source
        steps = 0

        while current != self.destination and steps < max_steps:
            next_node = self._select_next_node(current, pheromone)
            if next_node is None:
                break

            self.path.append(next_node)
            self.visited.add(next_node)
            current = next_node
            steps += 1

        if self.path[-1] != self.destination:
            return [], float("inf")

        return self.path, path_length(self.graph, self.path)

    def _select_next_node(self, current: int, pheromone: np.ndarray) -> int | None:
        neighbors = list(self.graph.neighbors(current))
        feasible = [node for node in neighbors if node not in self.visited]

        if not feasible:
            if self.destination in neighbors and self.destination != current:
                feasible = [self.destination]
            else:
                return None

        desirability = []
        for next_node in feasible:
            tau = pheromone[current, next_node] ** self.alpha
            eta = (1.0 / self.graph[current][next_node]["weight"]) ** self.beta
            desirability.append(tau * eta)

        probabilities = np.array(desirability, dtype=float)
        total = probabilities.sum()
        if total <= 0:
            return int(self.rng.choice(feasible))

        probabilities /= total
        return int(self.rng.choice(feasible, p=probabilities))
