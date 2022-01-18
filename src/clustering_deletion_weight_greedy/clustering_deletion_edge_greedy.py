import seaborn as sns
import math
import random
import numpy as np


class RangedHeap:
    def __init__(self, G):
        self.size = len(G.edges)
        self.fs = [{} for _ in range(len(G.nodes))]
        self.bool_fs = []

        for e in G.edges:
            val = G[e[0]][e[1]]['weight']
            e = self.get_e(e[0], e[1])
            self.fs[val][e] = e

        # self.bool_fs.append(1)
        for id, id_map in enumerate(self.fs):
            if len(id_map) != 0:
                self.bool_fs.append(id)

    def getMax(self):
        if self.size >= 1:
            out = self.getRandTwins()
            # out = self.fs[self.bool_fs[0]].popitem()[1]
            self.size -= 1
            if len(self.fs[self.bool_fs[-1]]) == 0:
                del self.bool_fs[-1]
            return out
        else:
            print("RangedHeap is empty")

    def getRand(self):
        prob_list = [id*len(self.fs[id]) for id in self.bool_fs]
        norm = np.sum(prob_list)
        for i in range(len(prob_list)):
            prob_list[i] /= norm

        weight_to_pick = np.random.choice(self.bool_fs, size=1, p=prob_list)[0]
        edge_to_pick = random.choice(list(self.fs[weight_to_pick].values()))
        del self.fs[weight_to_pick][edge_to_pick]
        self.size -= 1
        if len(self.fs[weight_to_pick]) == 0:
            self.binary_search_delete(weight_to_pick)
        return edge_to_pick

    def getRandTwins(self):
        edge_to_pick = random.choice(list(self.fs[self.bool_fs[-1]].values()))
        del self.fs[self.bool_fs[-1]][edge_to_pick]
        return edge_to_pick

    def delete_e(self, e0, e1, f):
        e = self.get_e(e0, e1)
        del self.fs[f][e]
        self.size -= 1

        if len(self.fs[f]) == 0:
            self.binary_search_delete(f)

    def add(self, e0, e1, f):
        e = self.get_e(e0, e1)
        if len(self.fs[f]) == 0:
            self.binary_search_add(f)
        self.fs[f][e] = e
        self.size += 1

    def adjust(self, e0, e1, old_f, new_f):
        e = self.get_e(e0, e1)
        self.delete_e(e[0], e[1], old_f)
        self.add(e[0], e[1], new_f)

    def binary_search_delete(self, x):
        l = 0
        r = len(self.bool_fs)-1

        while l <= r:
            c = (l + r) // 2
            if self.bool_fs[c] == x:
                break
            elif self.bool_fs[c] < x:
                l = c + 1
            else:
                r = c - 1
        del self.bool_fs[c]

    def binary_search_add(self, x):
        if len(self.bool_fs) > 0:
            if x < self.bool_fs[0]:
                self.bool_fs.insert(0, x)
            elif x > self.bool_fs[-1]:
                self.bool_fs.append(x)
            else:
                l = 0
                r = len(self.bool_fs)-1

                while l <= r:
                    c = (l + r) // 2
                    if self.bool_fs[c] < x:
                        if x < self.bool_fs[c+1]:
                            break
                        else:
                            l = c + 1
                    else:
                        r = c - 1
                self.bool_fs.insert(c+1, x)
        else:
            self.bool_fs.append(x)

    def get_e(self, e0, e1):
        return (e0, e1) if int(e0) < int(e1) else (e1, e0)

    def print_fs(self):
        for id, id_map in enumerate(self.fs):
            values = ""
            for key, value in id_map.items():
                values += " " + str(value)
            s = "[" + str(id) + "]->" + values + "\n"
            print(s)

    def prinf_bool_fs(self):
        print(self.bool_fs)

    def __len__(self):
        return self.size


def edge_contraction(G, e, rangedHeap):
    vicini0 = set(G.neighbors(e[0]))
    vicini0.remove(e[1])
    vicini1 = set(G.neighbors(e[1]))
    vicini1.remove(e[0])

    Ne0_e1 = vicini0 - vicini1  # vicini di e[0] e non di e[1]
    Ne0e1 = vicini0 & vicini1  # vicini di e[0] e di e[1]
    Ne1_e0 = vicini1 - vicini0  # vicini di e[1] e non di e[0]

    val = 0

    for node in Ne0_e1:  # removed
        rangedHeap.delete_e(e[0], node, G[e[0]][node]['weight'])
        val += G[e[0]][node]['weight']
        G.remove_edge(e[0], node)

    for node in Ne1_e0:  # removed
        rangedHeap.delete_e(e[1], node, G[e[1]][node]['weight'])
        val += G[e[1]][node]['weight']

    for node in Ne0e1:
        rangedHeap.delete_e(e[0], node, G[e[0]][node]['weight'])
        rangedHeap.delete_e(e[1], node, G[e[1]][node]['weight'])
        G[e[0]][node]['weight'] += G[e[1]][node]['weight']
        rangedHeap.add(e[0], node, G[e[0]][node]['weight'])

    G.nodes[e[0]]["clique"] += "-" + G.nodes[e[1]]["clique"]
    G.remove_node(e[1])

    return val


def clustering_deletion_choice_edge_greedy(G):
    rangedHeap = RangedHeap(G)

    value = 0
    while len(rangedHeap) != 0:
        e = rangedHeap.getMax()
        value += edge_contraction(G, e, rangedHeap)
    return value


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
    import pandas as pd

    df = pd.DataFrame(np.zeros((k, 2)), columns=["exec", "v_min"])

    for i in range(k):
        H = G.copy()
        val = clustering_deletion_choice_edge_greedy(H)
        df.at[i, 'exec'] = val
        if val < min_val:
            min_val = val
        df.at[i, 'v_min'] = min_val

    import seaborn as sns
    print(df)
    sns.lineplot(data=df)

    return min_val
