import sys


class NodeData:

    # When I crate a new node this will be is values in start
    def __init__(self, key: int, pos: tuple = None):
        self._key = key
        self._edges_to_node = {}
        self._location = None
        self._weight: float = sys.float_info.dig  # like Double.MAXValue()
        self._info: str = ""
        self._tag: int = 0
        self._edges_from_node = {}
        self._pos: tuple = pos

    def get_all_edges_to_node(self):
        return self._edges_to_node  # return a dict that holds all the edges that connected to this call node

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
        return self.tag

    def set_tag(self, tag: int) -> None:
        self._tag = tag

    def get_edge(self, node_key: int) -> float:
        return self.edges_from_node.get(node_key)

    def has_edge(self, dest: int) -> bool:
        return True if dest in self._edges_from_node else False

    def get_pos(self) -> tuple:
        return self._pos

    @property  # kind of a get function to the _edged_from_node , we can easily change it to not protected
    def edges_from_node(self):
        return self._edges_from_node

    def connect_from_edge(self, node_dest: int, weight: float) -> None:
        self._edges_from_node[node_dest] = weight

    def connect_to_edge(self, node_dest: int, weight: float) -> None:
        self._edges_to_node[node_dest] = weight

    def remove_edge_from(self, node_dest: int) -> None:
        del self._edges_from_node[node_dest]

    def remove_edge_to(self, node_dest: int) -> None:
        del self._edges_to_node[node_dest]

    def __repr__(self):
        return "" + str(self._key) + ": score " + str(self._tag) #TODO: figure out what is the score