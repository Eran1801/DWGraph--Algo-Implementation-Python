from unittest import TestCase

from src.DiGraph import DiGraph


# Creates a new 11 nodes graph with no connections
def create_small_graph() -> DiGraph:
    graph = DiGraph()
    for x in range(11):
        graph.add_node(x)
    return graph


class TestDiGraph(TestCase):

    def test_v_size(self):
        graph = create_small_graph()
        self.assertEqual(graph.v_size(), 11)

    def test_e_size(self):
        graph = create_small_graph()
        self.assertEqual(graph.e_size(), 0)
        graph.add_edge(0, 1, 1)
        graph.add_edge(0, 2, 3)
        graph.add_edge(1, 4, 1)
        graph.add_edge(2, 6, 1)
        graph.add_edge(1, 4, 3)
        self.assertEqual(graph.e_size(), 4)

    def test_get_mc(self):
        graph = create_small_graph()
        self.assertEqual(graph.get_mc(), 11)
        graph.add_edge(0, 1, 1)
        graph.add_edge(0, 2, 3)
        graph.add_edge(1, 4, 1)
        graph.add_edge(2, 6, 1)
        graph.add_edge(1, 4, 3)
        self.assertEqual(graph.get_mc(), 15)
        graph.remove_edge(2, 6)
        self.assertEqual(graph.get_mc(), 16)
        graph.remove_edge(2, 6)
        self.assertEqual(graph.get_mc(), 16)

    def test_add_node(self):
        graph = create_small_graph()
        self.assertEqual(graph.get_node(11), None)
        graph.add_node(11)
        self.assertEqual(graph.get_node(11).get_key(), 11)

    def test_get_node(self):
        graph = create_small_graph()
        self.assertEqual(graph.get_node(11), None)
        graph.add_node(11)
        self.assertEqual(graph.get_node(11).get_key(), 11)

    def test_remove_node(self):
        graph = create_small_graph()
        self.assertEqual(graph.get_node(4).get_key(), 4)
        graph.remove_node(4)
        self.assertIsNone(graph.get_node(4))

    def test_remove_edge(self):
        graph = create_small_graph()
        self.assertFalse(graph.remove_edge(0, 1))
        graph.add_edge(0, 1, 1.5)
        self.assertTrue(graph.remove_edge(0, 1))
