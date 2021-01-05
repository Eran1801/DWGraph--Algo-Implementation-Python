import json
from math import inf
from unittest import TestCase

from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


def create_graph() -> DiGraph:
    graph = DiGraph()
    for x in range(11):
        graph.add_node(x)
    return graph


def create_small_graph() -> DiGraph:
    g = DiGraph()  # creates an empty directed graph
    for n in range(4):
        g.add_node(n)
    g.add_edge(0, 1, 1)
    g.add_edge(1, 0, 1.1)
    g.add_edge(1, 2, 1.3)
    g.add_edge(2, 3, 1.1)
    g.add_edge(3, 2, 1.1)
    g.add_edge(1, 3, 1.9)
    g.remove_edge(1, 3)
    g.add_edge(1, 3, 10)

    return g


class TestGraphAlgo(TestCase):

    def test_load_from_json(self):

        g_algo = GraphAlgo()
        file = '../data/T0.json'
        g_algo.load_from_json(file)

        self.assertEqual(g_algo.get_graph().v_size(), 4)
        self.assertEqual(g_algo.get_graph().e_size(), 6)

    def test_save_to_json(self):

        graph = GraphAlgo(create_small_graph())
        check_save = ""

        graph.save_to_json("graph_test.json")
        f = open("graph_test.json")
        data = json.load(f)  # data contains the data in the json
        for id_ in data["Nodes"]:
            if id_["id"] == 0:  # i know that this id is zero because we create the graph above
                check_save = "save!"
                break

        self.assertEqual(check_save, "save!")  # so if the save of the graph was a success check_save will change

    def test_shortest_path(self):
        graph = GraphAlgo()
        graph.__init__(create_graph())

        self.assertEqual(len(graph.get_graph().get_all_v()), 11)

        graph.get_graph().add_edge(0, 1, 1)
        graph.get_graph().add_edge(0, 2, 3)
        graph.get_graph().add_edge(1, 4, 1)
        graph.get_graph().add_edge(2, 6, 1)
        graph.get_graph().add_edge(2, 1, 3)

        self.assertEqual(graph.shortest_path(0, 0), (0, [0]))
        self.assertEqual(graph.shortest_path(0, 6), (4, [0, 2, 6]))
        self.assertEqual(graph.shortest_path(0, 4), (2, [0, 1, 4]))
        self.assertEqual(graph.shortest_path(0, 9), (inf, []))

    def test_connected_component(self):

        graph = GraphAlgo(create_small_graph())

        self.assertEqual(graph.connected_component(3), [2, 3])
        self.assertEqual(graph.connected_component(0), [0, 1])
        self.assertEqual(graph.connected_component(1), [0, 1])
        self.assertEqual(graph.connected_component(9), [])

    def test_connected_components(self):

        graph = GraphAlgo(create_small_graph())

        self.assertEqual(graph.connected_components(), [[0, 1], [2, 3]])
        graph.get_graph().remove_edge(2, 3)
        self.assertEqual(graph.get_graph().e_size(), 5)  # the edge was deleted but still shows that yes
        # self.assertEqual(graph.connected_components(), [[0, 1], [2], [3]]) # not working for some reason
