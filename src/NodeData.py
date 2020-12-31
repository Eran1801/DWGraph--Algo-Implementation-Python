import sys

import self as self

from api import edge_data
from api.edge_data import EdgeData


class NodeData:

    # When I crate a new node this will be is values in start
    def __init__(self, key: int):
        self._key = key
        self._edges_to_node = {}
        self._location = None
        self._weight: float = sys.float_info.dig  # like Double.MAXValue()
        self._info: str = ""
        self._tag: int = 0
        self._edges_from_node = {}

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

    def get_edge(self, node_key: int) -> edge_data:
        return self.edges_from_node.get(node_key)

    @property  # kind of a get function to the _edged_from_node , we can easily change it to not protected
    def edges_from_node(self):
        return self._edges_from_node

    def has_Ni(self, key: int) -> bool:
        return True if key in self._edges_from_node else False

    def connect_edge(self, node_dest: __init__, weight: float) -> None:
        edge = EdgeData(self.get_key, node_dest.get_key(), weight)
        value_to_dic = {node_dest.get_key, edge}
        self._edges_from_node.update(value_to_dic)
