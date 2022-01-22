import networkx as nx
import time
from src.clustering_deletion_simple_graph.clustering_deletion_deleted_edge_greedy.deleted_edge_greedy_avoid_G import preprocess
from src.clustering_deletion_simple_graph.clustering_deletion_edge_contraction_based.util_exp import read_graph
from src.clustering_deletion_simple_graph.clustering_deletion_weight_greedy.clustering_deletion_edge_greedy import clustering_deletion_choice_edge_greedy, k_clustering_deletion_random_edge_contraction
from src.clustering_deletion_simple_graph.clustering_deletion_deleted_edge_greedy.deleted_edge_greedy_avoid_G import deleted_edge_greedy_avoid, check_solution
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
        G_sol = G.copy()

        # n = len(G.nodes)
        start_k = time.time()
        # preprocess(G)
        # value = k_clustering_deletion_random_edge_contraction(G, n*int(log(n)))
        value = clustering_deletion_choice_edge_greedy(G_sol)
        end_k = time.time() - start_k
        isCorrect = check_solution(G.copy(), G_sol, value)
        s += "dataset " + str(dataset) + "\n"
        s += "execution time " + str(end_k) + "\n"
        s += "value " + str(value) + "\n"
        s += "isCorrect " + str(isCorrect) + "\n"
        s += "*********************************"
    print(s)

    # import matplotlib.pyplot as plt

    # plt.show()
