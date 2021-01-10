def connected_components(self) -> List[list]:
    self.reset_algo_variables()
    for node in self._graph.get_all_v().values():
        if node.get_id() == -1:  # if not visited
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