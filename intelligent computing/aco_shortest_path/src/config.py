from dataclasses import dataclass


@dataclass(slots=True)
class ACOConfig:
    num_ants: int = 20
    num_iterations: int = 100
    alpha: float = 1.0
    beta: float = 3.0
    evaporation_rate: float = 0.3
    q: float = 100.0
    initial_pheromone: float = 1.0
    max_steps_factor: int = 3
    source: int = 0
    destination: int = 5
    random_seed: int = 42
