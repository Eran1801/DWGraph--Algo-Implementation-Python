import json
import networkx as nx
from src.GraphAlgo import GraphAlgo
import time


def check_functions(file_path) -> bool:
    with open(file_path) as f:
        json_data = json.loads(f.read())

    nx_graph = nx.DiGraph()

    nx_graph.add_nodes_from(
        elem['id'] for elem in json_data['Nodes']
    )
    nx_graph.add_weighted_edges_from(
        (elem['src'], elem['dest'], elem['w']) for elem in json_data['Edges']
    )

    dg_algo = GraphAlgo()
    dg_algo.load_from_json(file_path)

    # nx.draw(nx_graph, with_labels=True)
    # plt.show()

    print("JSON file: " + file_path)


    start_time = time.time_ns()
    dg_algo.shortest_path(0, 5)
    end_time = time.time_ns()
    resultTime = end_time - start_time
    print("Running time Python shortest_path: " + str(resultTime / 1000000) + " ms")

    start_time = time.time_ns()
    print("Shortest Path (0,5) (NetworkX Graph):\n" + str(
        nx.shortest_path(nx_graph, source=0, target=5, weight='weight')))
    end_time = time.time_ns()
    resultTime = end_time - start_time
    print("Running time NetworkX shortest_path: " + str(resultTime / 1000000) + " ms")

    start_time = time.time_ns()
    print(dg_algo.connected_components())
    end_time = time.time_ns()
    resultTime = end_time - start_time
    print("Running time Python connected_components: " + str(resultTime / 1000000) + " ms")

    start_time = time.time_ns()
    connected_components_graph = nx.strongly_connected_components(nx_graph)
    end_time = time.time_ns()
    # for elem in connected_components_graph:
    #     print(elem)
    resultTime = end_time - start_time
    print("Running time NetworkX connected_components: " + str(resultTime / 1000000) + " ms")

    start_time = time.time_ns()
    dg_algo.connected_component(9)
    # for elem in connected_components_graph:
    #     print(elem)
    end_time = time.time_ns()
    resultTime = end_time - start_time
    print("Running time Python connected_component: " + str(resultTime / 1000000) + " ms")


if __name__ == '__main__':
    # check_functions("../data/G_10_80_0.json")
    # check_functions("../data/G_100_800_0.json")
    # check_functions("../data/G_1000_8000_0.json")
    # check_functions("../data/G_10000_80000_0.json")
    # check_functions("../data/G_20000_160000_0.json")
    check_functions("../data/G_30000_240000_0.json")
