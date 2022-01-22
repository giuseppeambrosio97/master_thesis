from src.clustering_deletion_simple_graph.clustering_deletion_edge_contraction_based.choice import choice_deleted_edge_greedy_value
from src.clustering_deletion_simple_graph.clustering_deletion_edge_contraction_based.clustering_deletion_edge_contraction import edge_contraction


def preprocess(G):
    c = 0
    while True:
        e, value = choice_deleted_edge_greedy_value(G, list(G.edges))
        if(value > 0):
            return G, c
        edge_contraction(G, e)
        c += 1
