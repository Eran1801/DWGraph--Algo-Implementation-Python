from eran_sketch import edge_data, node_data


class DWGraphDs:

    def __init__(self):
        self._nodes_dict = {}  # holds the nodes in the graph
        self._num_of_edges = 0
        self._mode_count = 0

    def get_node(self, key: int) -> node_data:  # the ' -> node_data ' is to tell which kind of element will return
        return self._nodes_dict.get(key)  # if the node doesn't exist return None. that it's equal to null

    def get_edge(self, src: int, dest: int) -> edge_data:
        if self._nodes_dict.get(src) is None:  # if the node with the key of src don't exist in nodes_dict return null
            return None
        node_source = node_data.NodeData(self.get_node(src))  # This is how you set a type of var
        return node_source.get_edge(dest)

    def add_node(self, node: node_data) -> None:
        key_node = node_data.NodeData(node).get_key()  # holds the key of the node in the argument
        if key_node not in self._nodes_dict:
            add_value = {key_node, node}
            self._nodes_dict.update(add_value)
            self._mode_count+=1
        else:
            pass  # else - do nothing

    def connect(self, src: int, dest: int, weight: float) -> None:

        if src != dest or weight < 0 :
            # if the key not in the graph we need to add the node with the key of the src
            # to the neighbor_dict of node dest
            if src not in self._nodes_dict:
                node_source = node_data.NodeData(self.get_node(src))
                node_dest = node_data.NodeData(self.get_node(dest))
                if node_source.has_Ni(dest) : self._num_of_edges+=1 #
                   node_source.connect_edge(node_dest,weight)
                   self._mode_count+=1


