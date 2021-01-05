import random
from typing import List
import json
import queue as Q
import matplotlib.pyplot as plt

from GraphAlgoInterface import GraphAlgoInterface
from NodeData import NodeData
from GraphInterface import GraphInterface
from DiGraph import DiGraph


class GraphAlgo(GraphAlgoInterface):

    # When you create an instance of this Class the graph that you will working on is the DiGraph
    def __init__(self, graph: DiGraph = None):
        self._graph = graph
        self._id_counter = 0
        self._scc_counter = 0
        self._stack = []

    """
    return: the directed graph on which the algorithm works on.
    """

    def reset_algo_variables(self) -> None:
        self._id_counter = 0
        self._scc_counter = 0
        self._stack = []


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
                if "pos" in node:
                    node_pos = node["pos"]
                    node_pos_tuple = tuple(map(float, node_pos.split(",")))
                else:
                    random_number_x = random.uniform(35.185, 35.215)
                    random_number_y = random.uniform(32.098, 32.11)
                    node_pos_tuple = (random_number_x, random_number_y, 0.0)
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
            node_list.append({"id": node.get_key()})
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
        for node in self._graph.get_all_v().values():
            node.reset_values()
        pq = Q.PriorityQueue()
        if id1 == id2: return 0,[id1]
        src_node = self._graph.get_node(id1)
        dest_node = self._graph.get_node(id2)
        if src_node is None or dest_node is None:
            return float('inf'), []
        
        for edge_dest_key, edge_weight in src_node.get_all_edges_from_node().items():
            pq.put((edge_weight, src_node.get_key(), edge_dest_key))

        src_node.set_weight(0)
        src_node.set_info('BLACK')

        while not pq.empty():
            prioritized_edge = pq.get() # (edge_weight, edge_src_key, edge_dest_key)
            edge_weight = prioritized_edge[0]
            node_src_key = prioritized_edge[1]
            node_dest_key = prioritized_edge[2]
            neighbor_node = self._graph.get_node(node_dest_key) # get node with key = edge_key
            
            if edge_weight < neighbor_node.get_weight():
                neighbor_node.set_weight(edge_weight)
                neighbor_node.set_tag(node_src_key)

            if neighbor_node.get_info() != 'BLACK':
                for edge_dest_key, edge_weight in neighbor_node.get_all_edges_from_node().items():
                    pq.put((edge_weight + neighbor_node.get_weight(), neighbor_node.get_key(), edge_dest_key))
                neighbor_node.set_info('BLACK') # mark that node as visited.
        
        next_parent = dest_node
        if next_parent.get_tag() == -1: return (float('inf'),[])
        path = list()
        while next_parent.get_tag() != -1:
            path.append(next_parent.get_key())
            next_parent = self._graph.get_node(next_parent.get_tag())
        path.append(next_parent.get_key()) # add the last node
        path.reverse()
        return self._graph.get_node(path[-1]).get_weight(), path
            
    """
    Finds the Strongly Connected Component(SCC) that node id1 is a part of.
    @param id1: The node id
    @return: The list of nodes in the SCC

    Notes:
    If the graph is None or id1 is not in the graph, the function should return an empty list []
    """

    def connected_component(self, id1: int) -> list:
        sccs = self.connected_components()
        for list_element in sccs:
            for id_element in list_element:
                if id1 == id_element:
                    return list_element


    """
    Finds all the Strongly Connected Component(SCC) in the graph.
    @return: The list all SCC
    Notes:
    If the graph is None the function should return an empty list []
    """

    def connected_components(self) -> List[list]:
        self.reset_algo_variables()
        for node in self._graph.get_all_v().values():
            if node.get_id() == -1: #if not visited
                self.dfs(node)
        result_list = []
        for node_id in range(self._graph.v_size()):
            node_keys = []
            for node in self._graph.get_all_v().values():
                if node.get_low() == node_id:
                    node_keys.append(node.get_key())
            if len(node_keys):
                result_list.append(node_keys)
        return result_list

    def dfs(self, node: NodeData) -> None:
        node.set_id(self._id_counter)
        node.set_low(self._id_counter)
        self._stack.append(self._id_counter)
        self._id_counter += 1

        for edge_dest_key in node.get_all_edges_from_node():
            edge_dest_node = self._graph.get_node(edge_dest_key)
            if edge_dest_node.get_id() == -1:
                self.dfs(edge_dest_node)
            if edge_dest_key in self._stack:
                node.set_low(min(node.get_low(), edge_dest_node.get_low()))

        if node.get_id() == node.get_low():
            while len(self._stack):
                node_key_from_stack = self._stack.pop()
                node_from_stack = self._graph.get_node(node_key_from_stack)
                node_from_stack.set_low(node.get_id())
                if node_from_stack.get_id() == node.get_id():
                    break
            self._scc_counter += 1

    """
    Plots the graph.
    If the nodes have a position, the nodes will be placed there.
    Otherwise, they will be placed in a random but elegant manner.
    @return: None
     """

    def plot_graph(self) -> None:

        nodes_x = []
        nodes_y = []

        for node in self._graph.get_all_v().values():
            nodes_x.append(node.get_pos()[0])
            nodes_y.append(node.get_pos()[1])

        plt.plot(nodes_x, nodes_y, 'green', 'dashed', 3, 'o', 'blue', 12)

        # setting x and y axis range
        plt.ylim(32.098, 32.11)
        plt.xlim(35.185, 35.215)

        # naming the x axis
        plt.xlabel('x - axis')
        # naming the y axis
        plt.ylabel('y - axis')

        # giving a title to my graph
        plt.title('Graph')

        # function to show the plot
        plt.show()