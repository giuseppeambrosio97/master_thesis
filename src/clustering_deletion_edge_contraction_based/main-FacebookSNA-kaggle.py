from clustering_deletion_edge_contraction import *
import time
import matplotlib.pyplot as p

if __name__ == "__main__":
    fb = nx.read_edgelist('/home/peppe/Scrivania/master_thesis/clustering_deletion_edge_contraction_based/data/FacebookSNA-kaggle/facebook-combined.txt',
                          create_using=nx.Graph(), nodetype=str)

    # print(len(list(fb.nodes)))
    # print(len(list(fb.edges)))
    nx.set_edge_attributes(fb, 1, 'weight')
    # value, nodes = clustering_deletion_random_edge_contraction(G)
    start_k = time.time()
    value, nodes = k_clustering_deletion_random_edge_contraction(
        fb, len(list(fb.edges)))
    end_k = time.time() - start_k
    # print("value ", value, " nodes ", nodes)
    print("value ", value)
    print("execution time ", end_k)
