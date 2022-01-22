import networkx as nx
import time
from src.clustering_deletion_simple_graph.clustering_deletion_weight_greedy.clustering_deletion_edge_greedy import clustering_deletion_choice_edge_greedy_with_preprocess
if __name__ == "__main__":
    edge_list = [('1', '2'), ('2', '3'), ('1', '3'), ('1', '9'), ('1', '7'), ('1', '8'), ('7', '8'),
                 ('7', '9'), ('8', '9'), ('3', '4'), ('3', '5'), ('3', '6'), ('4', '6'), ('4', '5'), ('5', '6')]
    G = nx.Graph(edge_list)

    for node in G.nodes:
        G.nodes[node]["clique"] = str(node)

    start_k = time.time()
    value = clustering_deletion_choice_edge_greedy_with_preprocess(G)
    end_k = time.time() - start_k
    print("execution time ", end_k)
    print("value ", value)
