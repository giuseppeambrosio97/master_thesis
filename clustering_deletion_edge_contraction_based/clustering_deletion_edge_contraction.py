import networkx as nx
from choice import *


def edge_contraction(G, e):
    vicini0 = set(G.neighbors(e[0]))
    vicini1 = set(G.neighbors(e[1]))

    value = 0

    A = vicini0 - vicini1
    B = vicini0 & vicini1
    C = vicini1 - vicini0

    for node in B:
        G[e[0]][node]['weight'] += G[e[1]][node]['weight']

    for node in A:
        if node != e[1]:
            value += G[e[0]][node]['weight']
            G.remove_edge(e[0], node)

    for node in C:
        if node != e[0]:
            value += G[e[1]][node]['weight']
            G.remove_edge(e[1], node)

    # for node in vicini0:
    #   if node in vicini1: #B
    #     G[e[0]][node]['weight'] += G[e[1]][node]['weight']
    #   elif node != e[1]:  #A
    #     value += G[e[0]][node]['weight']
    #     G.remove_edge(e[0],node)

    # for node in vicini1:
    #   if node not in vicini0: #C
    #     print("belloo ", node)
    #     value += G[e[1]][node]['weight']
    #     G.remove_edge(e[1],node)

    mapping = {e[0]: e[0]+e[1]}
    nx.relabel_nodes(G, mapping, copy=False)
    G.remove_node(e[1])

    return value


def clustering_deletion_random_edge_contraction(G):
    """
    INPUT:
        G: networkx graph

    OUTPUT:
        val: value of solution
        partion: partion of the set of vertices identified by the solution
    """
    extractable_edges = list(G.edges)
    value = 0

    while (extractable_edges):
        e = choice(G, extractable_edges, choice_weight_softmax_random)
        value += edge_contraction(G, e)
        extractable_edges = list(G.edges)

    return value, G.nodes


def k_clustering_deletion_random_edge_contraction(G, k):
    """
    INPUT:
        G: networkx graph
        k: number of times that clustering_deletion_random_edge_contraction must be executed
    OUTPUT:
        min_val: value of the solution with the minimum value among the k discovered
        min_partition: partition of the set of vertices identified by the solution with value min_value
    """

    min_val = math.inf
    min_partition = None

    for i in range(k):
        H = G.copy()
        val, partition = clustering_deletion_random_edge_contraction(H)
        if val < min_val:
            min_val = val
            min_partition = partition

    return min_val, min_partition
