import random
import numpy as np
import math
from scipy.stats import distributions, entropy
import networkx as nx


def choice_uniform_random(G, extractable_edges):
    return random.choice(extractable_edges)


def choice_weight_random(G, extractable_edges):
    distribution = []
    norm = 0
    for edge in extractable_edges:
        norm += G[edge[0]][edge[1]]['weight']

    for edge in extractable_edges:
        distribution.append(G[edge[0]][edge[1]]['weight']/norm)

    id = np.random.choice(range(len(extractable_edges)),
                          size=1, p=distribution)
    return extractable_edges[id[0]]


def choice_weight_softmax_random(G, extractable_edges):
    distribution = []
    norm = 0
    for edge in extractable_edges:
        norm += math.exp(G[edge[0]][edge[1]]['weight'])

    for edge in extractable_edges:
        distribution.append(math.exp(G[edge[0]][edge[1]]['weight'])/norm)

    id = np.random.choice(range(len(extractable_edges)),
                          size=1, p=distribution)
    return extractable_edges[id[0]]


def choice_weight_greedy(G, extractable_edges):
    max_w = -math.inf
    max_edge = None

    for edge in extractable_edges:
        val = G[edge[0]][edge[1]]['weight']
        if val > max_w:
            max_w = val
            max_edge = edge

    return max_edge


def choice_entropy_greedy(G, extractable_edges):
    value_max = - math.inf
    e_max = None

    for e in extractable_edges:
        val = entropy_if_deleted_e(G.copy(), e)
        if val > value_max:
            value_max = val
            e_max = e
    return e_max


def entropy_if_deleted_e(G, e):
    vicini0 = set(G.neighbors(e[0]))
    vicini1 = set(G.neighbors(e[1]))

    A = vicini0 - vicini1  # vicini di e[0] e non di e[1]
    B = vicini0 & vicini1  # vicini di e[0] e di e[1]
    C = vicini1 - vicini0

    for node in B:
        G[e[0]][node]['weight'] += G[e[1]][node]['weight']

    for node in A:  # removed
        if node != e[1]:
            G.remove_edge(e[0], node)

    for node in C:  # removed
        if node != e[0]:
            G.remove_edge(e[1], node)

    mapping = {e[0]: e[0]+"-"+e[1]}
    nx.relabel_nodes(G, mapping, copy=False)
    G.remove_node(e[1])

    norm = 0
    for edge in G.edges:
        norm += G[edge[0]][edge[1]]['weight']

    distribution = []
    for edge in G.edges:
        distribution.append(G[edge[0]][edge[1]]['weight']/norm)

    return entropy(distribution, base=2)


def choice_deleted_edge_greedy(G, extractable_edges):
    value_min = math.inf
    e_min = None
    for e in extractable_edges:
        value = 0  # numero di edge da eliminare se contratto l'edge e

        vicini0 = set(G.neighbors(e[0]))
        vicini1 = set(G.neighbors(e[1]))
        A = vicini0 - vicini1
        C = vicini1 - vicini0

        for node in A:  # removed
            if node != e[1]:
                value += G[e[0]][node]['weight']

        for node in C:  # removed
            if node != e[0]:
                value += G[e[1]][node]['weight']

        if value < value_min:
            value_min = value
            e_min = e

    return e_min


def choice(G, extractable_edges, method):
    return method(G, extractable_edges)


def choice_deleted_edge_greedy_value(G, extractable_edges):
    value_min = math.inf
    e_min = None
    for e in extractable_edges:
        value = 0  # numero di edge da eliminare se contratto l'edge e

        vicini0 = set(G.neighbors(e[0]))
        vicini1 = set(G.neighbors(e[1]))
        A = vicini0 - vicini1
        C = vicini1 - vicini0

        for node in A:  # removed
            if node != e[1]:
                value += G[e[0]][node]['weight']

        for node in C:  # removed
            if node != e[0]:
                value += G[e[1]][node]['weight']

        if value < value_min:
            value_min = value
            e_min = e

    return e_min,value_min


def choice_max_Ne0_e1(G, extractable_edges):

    e_max = None
    value_max = -1
    for e in extractable_edges:
        vicini0 = set(G.neighbors(e[0]))
        vicini0.remove(e[1])
        vicini1 = set(G.neighbors(e[1]))
        vicini1.remove(e[0])

        Ne0_e1, Ne0e1, Ne1_e0 = vicini0 - vicini1, vicini0 & vicini1, vicini1 - vicini0

        value_AC = 0

        for node in Ne0_e1:  # removed
            value_AC += G[e[0]][node]['weight']

        for node in Ne1_e0:  # removed
            value_AC += G[e[1]][node]['weight']

        value_B = G[e[0]][e[1]]['weight']

        for node in Ne0e1:  # removed
            value_B += G[e[1]][node]['weight']
            value_B += G[e[0]][node]['weight']

        value_AC_plus_B = value_AC + value_B

        # print("edge {} value_B {} valueAC {}".format(e,value_B,value_AC))

        pvalue_B = value_B / value_AC_plus_B

        # pvalue_AC = 1 - pvalue_B
        # print("->>> pvalueB {} pvalueAC {}".format(pvalue_B, 1 - pvalue_B))
        if value_max < pvalue_B:
            value_max = pvalue_B
            e_max = e

    # print("***********************************************************take edge ", e_max)
    return e_max

