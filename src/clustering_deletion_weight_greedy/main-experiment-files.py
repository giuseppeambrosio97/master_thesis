from math import log
import networkx as nx
import time
from clustering_deletion_deleted_edge_greedy.deleted_edge_greedy import preprocess
from src.clustering_deletion_edge_contraction_based.util_exp import read_graph
from src.clustering_deletion_weight_greedy.clustering_deletion_edge_greedy import clustering_deletion_choice_edge_greedy, k_clustering_deletion_random_edge_contraction

if __name__ == "__main__":

    datasets = [
        "data/cur_data_exp/FB1",
        # "data/cur_data_exp/FB2",
        # "data/bio/bio-CE-GT",
        # "data/bio/bio-SC-CC",
        # "data/bio/bio-HS-HT.edges",
        # "data/bio/bio-grid-plant.edges",
        # "data/bio/bio-grid-worm.edges"
    ]

    s = ""
    for dataset in datasets:
        G = read_graph(dataset)
        nx.set_edge_attributes(G, 1, 'weight')
        nx.set_node_attributes(G, "", "labels")

        for node in G.nodes:
            G.nodes[node]["labels"] = str(node)

        n = len(G.nodes)
        start_k = time.time()
        preprocess(G)
        # value = k_clustering_deletion_random_edge_contraction(G, n*int(log(n)))
        value = clustering_deletion_choice_edge_greedy(G)
        end_k = time.time() - start_k
        s += "dataset " + str(dataset) + "\n"
        s += "execution time " + str(end_k) + "\n"
        s += "value " + str(value) + "\n"
        s += "*********************************"
    print(s)

    import matplotlib.pyplot as plt

    plt.show()
