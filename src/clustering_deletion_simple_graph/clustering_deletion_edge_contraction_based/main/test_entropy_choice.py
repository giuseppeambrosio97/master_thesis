import networkx as nx
from src.clustering_deletion_simple_graph.clustering_deletion_edge_contraction_based.choice import choice_entropy_greedy, entropy_if_deleted_e

if __name__ == "__main__":
    edge_list = [('1', '2'), ('2', '3'), ('1', '3'), ('1', '9'), ('1', '7'), ('1', '8'), ('7', '8'),
                 ('7', '9'), ('8', '9'), ('3', '4'), ('3', '5'), ('3', '6'), ('4', '6'), ('4', '5'), ('5', '6')]
    G = nx.Graph(edge_list)
    nx.set_edge_attributes(G, 1, 'weight')

    print(choice_entropy_greedy(G, list(G.edges)))

    # e = ('3', '6')

    # print(entropy_if_deleted_e(G.copy(), e))
