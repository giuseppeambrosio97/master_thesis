import networkx as nx
import time
from src.clustering_deletion_edge_contraction_based.util_exp import read_graph
from src.clustering_deletion_deleted_edge_greedy.clustering_deletion_deleted_edge_greedy import clustering_deleteting_choice_deleted_edge_greedy
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

    for dataset in datasets:
        G = read_graph(dataset)
        nx.set_edge_attributes(G, 1, 'weight')
        nx.set_edge_attributes(G, -1, 'f')
        nx.set_node_attributes(G, "", "labels")

        for node in G.nodes:
            G.nodes[node]["labels"] = str(node)

        start_k = time.time()
        value = clustering_deleteting_choice_deleted_edge_greedy(G)
        end_k = time.time() - start_k
        print("execution time ", end_k)
        print("value ", value)
