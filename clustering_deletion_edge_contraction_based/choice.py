import random
import numpy as np
import math


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


def choice_weight_greedy(G):
    pass


def choice_entropy_greedy(G):
    pass


def choice(G, extractable_edges, method):
    return method(G, extractable_edges)
