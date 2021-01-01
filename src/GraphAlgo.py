from typing import List
import json

from GraphAlgoInterface import GraphAlgoInterface
from NodeData import NodeData
from src import GraphInterface
from DiGraph import DiGraph


class GraphAlgo(GraphAlgoInterface):

    # When you create an instance of this Class the graph that you will working on is the DiGraph
    def __init__(self, graph: DiGraph):
        self._graph = graph

    """
    return: the directed graph on which the algorithm works on.
    """

    def get_graph(self) -> GraphInterface:
        return self._graph

    """
    Loads a graph from a json file.
    @param file_name: The path to the json file
    @returns True if the loading was successful, False o.w.
    """

    def load_from_json(self, file_name: str) -> bool:

        try:
            with open(file_name) as f: # go to the path file and open it as a file
                graph_dict = json.load(f)  # create a dict that contains the data inside the json file
            g = DiGraph()  # create a instance of a DiGraph that we will insert all the data from the json file to him
            for node in graph_dict["Nodes"]:  # going throw all the nodes in the json file ( graph_dict )
                node_key = node["id"]
                node_pos = node["pos"]
        # each pos value consists 3 float number that separated with a ',' the map take each number and put in a tuple
                node_pos_tuple = tuple(map(float, node_pos.split(",")))
                g.add_node(node_key, node_pos_tuple)
            for edge in graph_dict["Edges"]:  # Same thing for the Edges in the json file
                edge_src = int(edge["src"])
                edge_dest = int(edge["dest"])
                edge_weight = float(edge["w"])
                g.add_edge(edge_src, edge_dest, edge_weight)
            self._graph = g
            return True
        except Exception as e:
            print(e)
            return False
    """
    Saves the graph in JSON format to a file
    @param file_name: The path to the out file
    @return: True if the save was successful, False o.w.
    """

    def save_to_json(self, file_name: str) -> bool:

        graph_json = {}  # A dict that will holds the JSON file data of the self._graph
    # for the node and edge we crate a empty list that will hold the data of them and then will save to the JSON file
        node_list, edge_list = [], []
        for node in self._graph.get_all_v().values():  # The values() function return the value, in our case a NodeData
            node_list.append({"id": node.get_key(), "pos": node.get_pos()})
            for dest, weight in node.get_all_edges_from_node().items():  # items() return a ' key , value ' of the dict
                edge_list.append({"src": node.get_key(), "dest": dest, "w": weight})

        graph_json["Nodes"] = node_list  # In the place of the nodes insert the node_list that we create
        graph_json["Edges"] = edge_list  # Same for the edge_list
        try:
            with open(file_name, 'w') as f:
                json.dump(graph_json, f)
            return True
        except Exception as e:
            print(e)
            return False

    """
    Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
    @param id1: The start node id
    @param id2: The end node id
    @return: The distance of the path, a list of the nodes ids that the path goes through

          Example:
  #      >>> from GraphAlgo import GraphAlgo
  #       >>> g_algo = GraphAlgo()
  #        >>> g_algo.addNode(0)
  #        >>> g_algo.addNode(1)
  #        >>> g_algo.addNode(2)
  #        >>> g_algo.addEdge(0,1,1)
  #        >>> g_algo.addEdge(1,2,4)
  #        >>> g_algo.shortestPath(0,1)
  #        (1, [0, 1])
  #        >>> g_algo.shortestPath(0,2)
  #        (5, [0, 1, 2])

          Notes:
          If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
          More info:
          https://en.wikipedia.org/wiki/Dijkstra's_algorithm
          """

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        pass

    """
    Finds the Strongly Connected Component(SCC) that node id1 is a part of.
    @param id1: The node id
    @return: The list of nodes in the SCC

    Notes:
    If the graph is None or id1 is not in the graph, the function should return an empty list []
    """

    def connected_component(self, id1: int) -> list:
        pass

    """
    Finds all the Strongly Connected Component(SCC) in the graph.
    @return: The list all SCC
    Notes:
    If the graph is None the function should return an empty list []
    """

    def connected_components(self) -> List[list]:
        pass

    """
    Plots the graph.
    If the nodes have a position, the nodes will be placed there.
    Otherwise, they will be placed in a random but elegant manner.
    @return: None
     """

    def plot_graph(self) -> None:
        pass
