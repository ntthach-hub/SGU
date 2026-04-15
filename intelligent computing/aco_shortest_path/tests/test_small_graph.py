import unittest

import networkx as nx

from src.aco import AntColonyOptimizer
from src.config import ACOConfig


class TestACOSmallGraph(unittest.TestCase):
    def test_finds_shortest_path_on_small_graph(self) -> None:
        graph = nx.Graph()
        graph.add_weighted_edges_from(
            [
                (0, 1, 2),
                (0, 2, 5),
                (1, 2, 1),
                (1, 3, 2),
                (2, 3, 4),
            ]
        )

        config = ACOConfig(
            num_ants=15,
            num_iterations=60,
            alpha=1.0,
            beta=3.0,
            evaporation_rate=0.2,
            q=100.0,
            source=0,
            destination=3,
            random_seed=7,
        )

        optimizer = AntColonyOptimizer(graph=graph, config=config)
        best_path, best_distance, history = optimizer.run()

        self.assertEqual(best_path, [0, 1, 3])
        self.assertAlmostEqual(best_distance, 4.0, places=6)
        self.assertEqual(len(history), config.num_iterations)


if __name__ == "__main__":
    unittest.main()
