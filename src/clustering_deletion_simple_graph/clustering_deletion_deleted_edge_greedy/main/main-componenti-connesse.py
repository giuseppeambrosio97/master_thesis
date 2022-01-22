import networkx as nx
from networkx.algorithms.components import connected
from src.clustering_deletion_simple_graph.util.util_exp import read_graph
import matplotlib.pyplot as plt

if __name__ == "__main__":
    dataset = "data/cur_data_exp/FB1 copy"
    G = read_graph(dataset)
    comps = connected.connected_components(G)

    for comp in comps:
        print(comp)

    # nx.draw(G, with_clique=True)
    # plt.show()
