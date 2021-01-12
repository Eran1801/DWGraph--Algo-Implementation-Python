import random
import sys


class NodeData:

    # When I crate a new node this will be is values in start
    def __init__(self, key: int, pos: tuple = None):
        self._key = key
        self._edges_to_node = {}
        self._location = None
        self._weight: float = float("inf")  #represents weight in Algo
        self._info: str = 'WHITE' #represents visited in Algo ("WHITE": not visited, "BLACK": visited)
        self._tag: int = -1 #represents parent in Algo
        self._edges_from_node = {}
        random_number_x = random.uniform(35.185, 35.215)
        random_number_y = random.uniform(32.098, 32.11)
        self._pos: tuple = pos if pos is not None else(random_number_x, random_number_y)
        self._id: int = -1  # represents id in algo (used in connected_components)
        self._low: int = -1  # represents low in algo (used in connected_components)

    def reset_values(self) -> None:
        self._weight: float = float("inf")  # represents weight in Algo
        self._info: str = 'WHITE'  # represents visited in Algo ("WHITE": not visited, "BLACK": visited)
        self._tag: int = -1  # represents parent in Algo
        self._id: int = -1  # represents id in algo (used in connected_components)
        self._low: int = -1  # represents low in algo (used in connected_components)

    def get_all_edges_to_node(self):
        return self._edges_to_node  # return a dict that holds all the edges that connected to this call node { key(id_src),weight}

    def get_all_edges_from_node(self):
        return self._edges_from_node  # return a dict that holds all the edges that connected from this call node

    def get_key(self) -> int:
        return self._key

    def get_weight(self) -> float:
        return self._weight

    def set_weight(self, weight: float) -> None:
        self._weight = weight

    def get_info(self) -> str:
        return self._info

    def set_info(self, info: str) -> None:
        self._info = info

    def get_tag(self) -> int:
        return self._tag

    def set_tag(self, tag: int) -> None:
        self._tag = tag

    def has_edge(self, dest: int) -> bool:
        return True if dest in self._edges_from_node else False

    def get_pos(self) -> tuple:
        return self._pos

    def edges_from_node(self):
        return self._edges_from_node

    def connect_from_edge(self, node_dest: int, weight: float) -> None:
        self._edges_from_node[node_dest] = weight

    def connect_to_edge(self, from_node: int, weight: float) -> None:
        self._edges_to_node[from_node] = weight

    def remove_edge_from(self, node_dest: int) -> None:
        del self._edges_from_node[node_dest]

    def remove_edge_to(self, node_dest: int) -> None:
        del self._edges_to_node[node_dest]

    def get_id(self) -> int:
        return self._id

    def get_low(self) -> int:
        return self._low

    def set_id(self, id: int) -> None:
        self._id = id

    def set_low(self, low: int) -> None:
        self._low = low

    def __repr__(self):
        return "" + str(self._key) + ": |edges out| " + str(len(self._edges_from_node)) + " |edges in| " + str(len(self._edges_to_node)) + ""
