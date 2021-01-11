import json
import networkx as nx
import matplotlib.pyplot as plt
from src.GraphAlgo import GraphAlgo


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

    #nx.draw(nx_graph, with_labels=True)
    #plt.show()

    print("JSON file: " + file_path)

    print("Shortest Path (0,5) (DiGraph):\n" + str(dg_algo.shortest_path(0, 5)[1]))

    print("Shortest Path (0,5) (NetworkX Graph):\n" + str(nx.shortest_path(nx_graph, source=0, target=5, weight='weight')))

    print("Connected Components (DiGraph):")

    print(dg_algo.connected_components())

    #dg_algo.plot_graph()

    print("Connected Components (NetworkX Graph):")

    connected_components_graph = nx.strongly_connected_components(nx_graph)
    for elem in connected_components_graph:
        print(elem)

if __name__ == '__main__':
    check_functions("../data/G_10_80_0.json")
    #check_functions("../data/G_100_800_0.json")
    #check_functions("../data/G_1000_8000_0.json")
    #check_functions("../data/G_10000_80000_0.json")
    #check_functions("../data/G_20000_160000_0.json")
    #check_functions("../data/G_30000_240000_0.json")
