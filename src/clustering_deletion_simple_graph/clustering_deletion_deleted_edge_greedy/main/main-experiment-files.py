import networkx as nx
import time
from src.clustering_deletion_simple_graph.util.util_exp import read_graph
from src.clustering_deletion_simple_graph.clustering_deletion_deleted_edge_greedy.deleted_edge_greedy import deleted_edge_greedy, check_solution
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
        nx.set_edge_attributes(G_sol, 1, 'weight')
        nx.set_edge_attributes(G_sol, -1, 'f')
        nx.set_node_attributes(G_sol, "", "clique")

        for node in G_sol.nodes:
            G_sol.nodes[node]["clique"] = str(node)

        start_k = time.time()
        value = deleted_edge_greedy(G_sol)
        end_k = time.time() - start_k
        isCorrect = check_solution(G.copy(), G_sol, value)

        s += "dataset " + str(dataset) + "\n"
        s += "execution time " + str(end_k) + "\n"
        s += "value " + str(value) + "\n"
        s += "isCorrect " + str(isCorrect) + "\n"
        s += "*********************************"
    print(s)
