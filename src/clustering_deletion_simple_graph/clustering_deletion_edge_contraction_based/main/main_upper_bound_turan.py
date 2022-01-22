from src.clustering_deletion_edge_contraction_based.upper_bound_turan import upper_bound_turan
import networkx as nx

if __name__ == "__main__":
    G = nx.read_edgelist("data/cur_data_exp/0.edges",
                         create_using=nx.Graph(), nodetype=str)
    n = len(G.nodes)
    m = len(G.edges)
    print(n, m)
    print(upper_bound_turan(n, m))
