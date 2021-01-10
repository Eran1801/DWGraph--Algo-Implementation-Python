import math
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
            with open(file_name) as f:  # go to the path file and open it as a file
                graph_dict = json.load(f)  # create a dict that contains the data inside the json file
            g = DiGraph()  # create a instance of a DiGraph that we will insert all the data from the json file to him
            for node in graph_dict["Nodes"]:  # going throw all the nodes in the json file ( graph_dict )
                node_key = node["id"]
                node_pos_tuple = None
                if "pos" in node:
                    node_pos = node["pos"]
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
        if id1 == id2:
            return 0, [id1]
        src_node = self._graph.get_node(id1)
        dest_node = self._graph.get_node(id2)
        if src_node is None or dest_node is None:
            return float('inf'), []

        for edge_dest_key, edge_weight in src_node.get_all_edges_from_node().items():
            pq.put((edge_weight, src_node.get_key(), edge_dest_key))

        src_node.set_weight(0)
        src_node.set_info('BLACK')

        while not pq.empty():
            prioritized_edge = pq.get()  # (edge_weight, edge_src_key, edge_dest_key)
            edge_weight = prioritized_edge[0]
            node_src_key = prioritized_edge[1]
            node_dest_key = prioritized_edge[2]
            neighbor_node = self._graph.get_node(node_dest_key)  # get node with key = edge_key

            if edge_weight < neighbor_node.get_weight():
                neighbor_node.set_weight(edge_weight)
                neighbor_node.set_tag(node_src_key)

            if neighbor_node.get_info() != 'BLACK':
                for edge_dest_key, edge_weight in neighbor_node.get_all_edges_from_node().items():
                    pq.put((edge_weight + neighbor_node.get_weight(), neighbor_node.get_key(), edge_dest_key))
                neighbor_node.set_info('BLACK')  # mark that node as visited.

        next_parent = dest_node
        if next_parent.get_tag() == -1: return (float('inf'), [])
        path = list()
        while next_parent.get_tag() != -1:
            path.append(next_parent.get_key())
            next_parent = self._graph.get_node(next_parent.get_tag())
        path.append(next_parent.get_key())  # add the last node
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
        if self._graph is None:
            return []
        node = self._graph.get_node(id1)
        if node is None:
            return []

        connected_from_node = self.bfs_from(node)
        connected_to_node = self.bfs_to(node)

        strongly_connected_component = list(set(connected_from_node) & set(connected_to_node)) #makes a list from the intersection of connected_from_node and connected_to_node
        return strongly_connected_component


    def bfs_from(self, starting_node: NodeData) -> list:
        queue = [starting_node]
        connected_from = [starting_node.get_key()]
        visited = {}
        for node_key in self._graph.get_all_v():
            visited[node_key] = False

        visited[starting_node.get_key()] = True
        while len(queue): #while the queue is not empty
            node_from_queue = queue.pop()
            for edge_from_node_key in node_from_queue.get_all_edges_from_node():
                if not visited[edge_from_node_key]:
                    queue.insert(0, self._graph.get_node(edge_from_node_key))
                    connected_from.append(edge_from_node_key)
                    visited[edge_from_node_key] = True

        return connected_from

    def bfs_to(self, starting_node: NodeData) -> list:
        queue = [starting_node]
        connected_to = [starting_node.get_key()]
        visited = {}
        for node_key in self._graph.get_all_v():
            visited[node_key] = False

        visited[starting_node.get_key()] = True
        while len(queue):  # while the queue is not empty
            node_from_queue = queue.pop()
            for edge_to_node_key in node_from_queue.get_all_edges_to_node():
                if not visited[edge_to_node_key]:
                    queue.insert(0, self._graph.get_node(edge_to_node_key))
                    connected_to.append(edge_to_node_key)
                    visited[edge_to_node_key] = True

        return connected_to





    """
    Finds all the Strongly Connected Component(SCC) in the graph.
    @return: The list all SCC
    Notes:
    If the graph is None the function should return an empty list []
    """

    def connected_components(self) -> List[list]:
        check_for_components_in_nodes = []
        ans_list = []
        for node_key in self._graph.get_all_v():
            check_for_components_in_nodes.append(node_key)
        while len(check_for_components_in_nodes):
            node_key = check_for_components_in_nodes[0]
            scc = self.connected_component(node_key)
            ans_list.append(scc)
            for connected_node in scc:
                check_for_components_in_nodes.remove(connected_node) #remove the nodes that we found their sccs from check_for_components_in_nodes

        return ans_list


    """
    Plots the graph.
    If the nodes have a position, the nodes will be placed there.
    Otherwise, they will be placed in a random but elegant manner.
    @return: None
     """

    def plot_graph(self) -> None:
        arrow_width = 0.00005
        arrow_head_width = 8 * arrow_width
        arrow_head_length = 8 * arrow_width

        fig, ax = plt.subplots()

        min_pos_x, min_pos_y, max_pos_x, max_pos_y = float("inf"), float("inf"), 0, 0

        for node in self._graph.get_all_v().values():
            min_pos_x = node.get_pos()[0] if node.get_pos()[0] < min_pos_x else min_pos_x
            min_pos_y = node.get_pos()[1] if node.get_pos()[1] < min_pos_y else min_pos_y
            max_pos_x = node.get_pos()[0] if node.get_pos()[0] > max_pos_x else max_pos_x
            max_pos_y = node.get_pos()[1] if node.get_pos()[1] > max_pos_y else max_pos_y

            node_pos_tuple = (node.get_pos()[0], node.get_pos()[1])
            node_circle = plt.Circle(node_pos_tuple, 0.00015, color='red')
            ax.add_artist(node_circle)

            plt.text(node.get_pos()[0]-0.000135, node.get_pos()[1]+0.00025, str(node.get_key()), fontsize=9, color="green")

            src_node_pos = node.get_pos()

            for dest_node_key in node.get_all_edges_from_node():
                dest_node_pos = self._graph.get_node(dest_node_key).get_pos()
                plt.arrow(src_node_pos[0], src_node_pos[1], dest_node_pos[0] - src_node_pos[0], dest_node_pos[1] - src_node_pos[1], width=arrow_width, head_width=arrow_head_width, head_length=arrow_head_length, length_includes_head=True)


        #plt.plot(nodes_x, nodes_y, 'green', 'dashed', 3, 'o', 'blue', 12)

        # setting x and y axis range
        offset = 0.0005
        plt.ylim(min_pos_y - offset, max_pos_y + offset)
        plt.xlim(min_pos_x - offset, max_pos_x + offset)

        # naming the x axis
        plt.xlabel('x - axis')
        # naming the y axis
        plt.ylabel('y - axis')

        # giving a title to my graph
        plt.title('Graph')

        # function to show the plot
        plt.show()
