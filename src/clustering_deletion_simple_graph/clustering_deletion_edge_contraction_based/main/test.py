from clustering_deletion_edge_contraction import k_clustering_deletion_random_edge_contraction, choice_weight_greedy
import time
import networkx as nx


if __name__ == "__main__":
    G = nx.read_edgelist("data/bio/bio-celegans.edges",
                         create_using=nx.Graph(), nodetype=str)

    nx.set_edge_attributes(G, 1, 'weight')
    start_k = time.time()
    value, nodes = k_clustering_deletion_random_edge_contraction(
        G, 1, choice_method=choice_weight_greedy
    )
    end_k = time.time() - start_k
    # print("value ", value, " nodes ", nodes)
    print("value ", value)
    print("execution time ", end_k)
