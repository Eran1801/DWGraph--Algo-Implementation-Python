from GraphInterface import GraphInterface
from NodeData import NodeData



class DiGraph(GraphInterface):

    def __init__(self):
        self._num_of_nodes = 0
        self._num_of_edges = 0
        self._nodes = {}  # Holds the nodes in the graph
        self._mc = 0

    """
    Returns the number of vertices in this graph
     @return: The number of vertices in this graph
     """

    def v_size(self) -> int:
        return self._num_of_nodes

    """
    Returns the number of edges in this graph
    @return: The number of edges in this graph
     """

    def e_size(self) -> int:
        return self._num_of_edges

    """
    return a dictionary of all the nodes in the Graph, each node is represented using a pair
    (node_id, node_data)
     """

    def get_all_v(self) -> dict:
        return self._nodes

    """
    return a dictionary of all the nodes connected to (into) node_id ,
    each node is represented using a pair (other_node_id, weight)
    """

    def all_in_edges_of_node(self, id1: int) -> dict:

        # a var from kind of node_data call the function that returns all the edges that connect to him
        return self._nodes[id1].get_all_edges_to_node()

    """
    return a dictionary of all the nodes connected from node_id , each node is represented using a pair
    (other_node_id, weight)
    """

    def all_out_edges_of_node(self, id1: int) -> dict:

        # a var from kind of node_data call the function that returns all the edges that connect from him
        return self._nodes[id1].get_all_edges_from_node()

    def get_mc(self) -> int:
        return self._mc

    """
    Adds an edge to the graph.
    @param id1: The start node of the edge
    @param id2: The end node of the edge
    @param weight: The weight of the edge
    @return: True if the edge was added successfully, False o.w.

    Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
    """

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:

        if id1 not in self._nodes or id2 not in self._nodes or self._nodes[id1].has_edge(id2):
            return False
        self._nodes[id1].connect_from_edge(id2, weight)
        self._nodes[id2].connect_to_edge(id1, weight)
        self._mc += 1
        self._num_of_edges += 1
        return True

    """
    Adds a node to the graph.
    @param node_id: The node ID
    @param pos: The position of the node
    @return: True if the node was added successfully, False o.w.

    Note: if the node id already exists the node will not be added
    """

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id in self._nodes:
            return False
        self._nodes[node_id] = NodeData(node_id, pos)  # pos in default = None
        self._mc += 1
        self._num_of_nodes += 1
        return True

    def get_node(self, node_id: int) -> NodeData:
        return self._nodes.get(node_id)

    """
    Removes a node from the graph.
    @param node_id: The node ID
    @return: True if the node was removed successfully, False o.w.

    Note: if the node id does not exists the function will do nothing
    """

    def remove_node(self, node_id: int) -> bool:

        if node_id in self._nodes:

            # removes all the edges that connected to node_id
            # Note : key_of_edge_to_delete is the src key of the edge that will be deleted
            for key_of_edge_to_delete in self._nodes[node_id].get_all_edges_to_node():
                self._nodes[key_of_edge_to_delete].remove_edge_from(node_id)
                self._mc += 1

            # removes all the edges that connected from node_id
            # Note : key_of_edge_to_delete is the src key of the edge that will be deleted
            for key_of_edge_to_delete in self._nodes[node_id].get_all_edges_from_node():
                self._nodes[key_of_edge_to_delete].remove_edge_to(node_id)
                self._mc += 1

            del self._nodes[node_id]  # delete the value of the key node_id
            self._mc += 1
            self._num_of_nodes -= 1
            return True
        return False  # if node doesn't exist in the graph return false

    """
    Removes an edge from the graph.
    @param node_id1: The start node of the edge
    @param node_id2: The end node of the edge
    @return: True if the edge was removed successfully, False o.w.

    Note: If such an edge does not exists the function will do nothing
    """

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 not in self._nodes or node_id2 not in self._nodes:
            return False
        if not self._nodes[node_id1].has_edge(node_id2):
            return False
        self._nodes[node_id1].remove_edge_from(node_id2)
        self._nodes[node_id2].remove_edge_to(node_id1)
        self._mc += 1
        self._num_of_edges -= 1
        return True

    def __repr__(self):
        return "Graph: |V|=" + str(self._num_of_nodes) + " , |E|=" + str(self._num_of_edges)
