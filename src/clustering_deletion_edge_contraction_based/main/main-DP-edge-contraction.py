from src.clustering_deletion_edge_contraction_based.clustering_deletion_edge_contraction import *
import time
from src.clustering_deletion_edge_contraction_based.DP_cd_edge_contraction import DP_cd_edge_contraction

if __name__ == "__main__":
    edge_list = [('1', '2'), ('2', '3'), ('1', '3'), ('1', '9'), ('1', '7'), ('1', '8'), ('7', '8'),
                 ('7', '9'), ('8', '9'), ('3', '4'), ('3', '5'), ('3', '6'), ('4', '6'), ('4', '5'), ('5', '6')]
    G = nx.Graph(edge_list)
    nx.set_edge_attributes(G, 1, 'weight')
    # value, nodes = clustering_deletion_random_edge_contraction(G)
    start_k = time.time()
    # value, nodes = DP_cd_edge_contraction(G)
    value = DP_cd_edge_contraction(G)

    end_k = time.time() - start_k
    # print("value ", value, " nodes ", nodes)
    print("value ", value)
    print("execution time ", end_k)
