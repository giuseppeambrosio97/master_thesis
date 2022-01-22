import networkx as nx
import time
from src.clustering_deletion_edge_contraction_based.util_exp import read_graph
from src.clustering_deletion_deleted_edge_greedy.deleted_edge_greedy_avoid_G import deleted_edge_greedy_avoid,check_solution
if __name__ == "__main__":

    datasets = [
        "data/exp/inputs/HC_small/HC_3_20_0.3.txt",
        # "data/exp/inputs/HC_small/HC_3_10_0.2.txt",
        # "data/exp/inputs/HC_small/HC_3_15_0.2.txt",
        # "data/exp/inputs/HC_small/HC_3_20_0.2.txt",
        # "data/exp/inputs/HC_small/HC_3_15_0.3.txt",
        # "data/exp/inputs/HC_small/HC_3_15_0.1.txt",
        # "data/exp/inputs/HC_small/HC_3_10_0.3.txt",
        # "data/exp/inputs/HC_small/HC_6_20_0.3.txt",
    ] 

    s = ""
    for dataset in datasets:
        G = read_graph(dataset)

        G_sol = G.copy()
        # nx.set_edge_attributes(G, 1, 'weight')
        # nx.set_edge_attributes(G, -1, 'f')
        nx.set_node_attributes(G_sol, None, "clique")
        nx.set_edge_attributes(G_sol, None, "EdgeBean")

        for node in G_sol.nodes:
            G_sol.nodes[node]["clique"] = set([node])

        print("n = {}, m = {}".format(len(G.nodes), len(G.edges)))

        start_k = time.time()
        value = deleted_edge_greedy_avoid(G_sol)
        end_k = time.time() - start_k
        isCorrect = check_solution(G.copy(), G_sol, value)
        s += "dataset " + str(dataset) + "\n"
        s += "n = {}, m = {}".format(len(G.nodes),len(G.edges)) + "\n"
        s += "execution time " + str(end_k) + "\n"
        s += "value " + str(value) + "\n"
        s += "isCorrect " + str(isCorrect) + "\n"
        s += "*********************************"    
    print(s)
