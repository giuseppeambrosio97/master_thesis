import math


class RangedHeap:
    def __init__(self, G):
        self.size = len(G.edges)
        self.fs = [set() for _ in range(len(G.nodes))]
        self.bool_fs = []

        for e in G.edges:
            val = f_simple_graph(G, e)
            G[e[0]][e[1]]['f'] = val
            e = self.get_e(e[0], e[1])
            self.fs[val].add(e)

        for id, id_map in enumerate(self.fs):
            if len(id_map) != 0:
                self.bool_fs.append(id)

    def getMin(self, G):
        if self.size >= 1:
            out = self.getMinTwins(G)
            # out = self.fs[self.bool_fs[0]].popitem()[1]
            self.size -= 1
            f_val = self.bool_fs[0]
            if len(self.fs[f_val]) == 0:
                del self.bool_fs[0]
            return out, f_val
        else:
            print("RangedHeap is empty")

    def getMinTwins(self, G):
        weight_max = -math.inf
        edge_to_pick = None
        for e in self.fs[self.bool_fs[0]]:
            w = G[e[0]][e[1]]['weight']
            if weight_max < w:
                weight_max = w
                edge_to_pick = e
        self.fs[self.bool_fs[0]].remove(edge_to_pick)
        return edge_to_pick

    def delete_e(self, e0, e1, f):
        e = self.get_e(e0, e1)
        self.fs[f].remove(e)
        self.size -= 1

        if len(self.fs[f]) == 0:
            self.binary_search_delete(f)

    def add(self, e0, e1, f):
        e = self.get_e(e0, e1)
        if len(self.fs[f]) == 0:
            self.binary_search_add(f)
        self.fs[f].add(e)
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
        if len(self.bool_fs) == 0:
            self.bool_fs.append(x)
        elif x < self.bool_fs[0]:
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

    def get_e(self, e0, e1):
        return (e0, e1) if int(e0) < int(e1) else (e1, e0)

    def print_fs(self):
        for id, id_map in enumerate(self.fs):
            values = ""
            for e in id_map:
                values += " " + str(e)
            s = "[" + str(id) + "]->" + values + "\n"
            print(s)

    def prinf_bool_fs(self):
        print(self.bool_fs)

    def __len__(self):
        return self.size


def preprocess(G):
    rangedHeap = RangedHeap(G)
    value = 0
    while True:
        e = rangedHeap.getMin(G)
        if(G[e[0]][e[1]]['f'] > 0):
            break

        value += 1
        edge_contraction(G, e, rangedHeap)
    return value


def xor(G, e):
    vicini0 = set(G.neighbors(e[0]))
    vicini0.remove(e[1])
    vicini1 = set(G.neighbors(e[1]))
    vicini1.remove(e[0])

    return vicini0 - vicini1, vicini1 - vicini0


def split_neighborhood(G, e):
    vicini0 = set(G.neighbors(e[0]))
    vicini0.remove(e[1])
    vicini1 = set(G.neighbors(e[1]))
    vicini1.remove(e[0])

    return vicini0 - vicini1, vicini0 & vicini1, vicini1 - vicini0


def f_simple_graph(G, e):
    A, C = xor(G, e)
    return len(A) + len(C)


def f_multi_graph(G, e):
    A, C = xor(G, e)
    value = 0

    for node in A:  # removed
        value += G[e[0]][node]['weight']

    for node in C:  # removed
        value += G[e[1]][node]['weight']

    return value


def f_multi_graph_v2(G, e):
    A, C = xor(G, e)
    return sum([G[e[0]][node]['weight'] for node in A]) + sum([G[e[1]][node]['weight'] for node in C])


def f_with_sets(G, e, Ne0_e1, Ne1_e0):
    value = 0

    for node in Ne0_e1:  # removed
        value += G[e[0]][node]['weight']

    for node in Ne1_e0:  # removed
        value += G[e[1]][node]['weight']

    return value


def edge_contraction(G, e, rangedHeap):
    Ne0_e1, Ne0e1, Ne1_e0 = split_neighborhood(G, e)

    for node in Ne0_e1:  # removed
        rangedHeap.delete_e(e[0], node, G[e[0]][node]['f'])
        G.remove_edge(e[0], node)

    for node in Ne1_e0:  # removed
        rangedHeap.delete_e(e[1], node, G[e[1]][node]['f'])

    for node in Ne0e1:
        G[e[0]][node]['weight'] += G[e[1]][node]['weight']
        rangedHeap.delete_e(e[0], node, G[e[0]][node]['f'])
        rangedHeap.delete_e(e[1], node, G[e[1]][node]['f'])

    G.nodes[e[0]]["clique"] += "-" + G.nodes[e[1]]["clique"]
    G.remove_node(e[1])

    for node in Ne0e1:
        new_f = f_multi_graph(G, (e[0], node))
        G[e[0]][node]['f'] = new_f
        rangedHeap.add(e[0], node, new_f)

    toAdjust = G.edges(list(Ne0_e1)+list(Ne0e1)+list(Ne1_e0))

    # toAdjust = G.edges(list(Ne0_e1)+list(Ne1_e0))
    for edge in toAdjust:
        if edge[0] != e[0] and edge[1] != e[0]:
            new_f = f_multi_graph(G, edge)
            old_f = G[edge[0]][edge[1]]['f']
            if new_f != old_f:
                G[edge[0]][edge[1]]['f'] = new_f
                rangedHeap.adjust(edge[0], edge[1], old_f, new_f)


def check_solution(G, G_sol, val):

    cliques = []
    n_nodes = 0
    for node in G_sol.nodes:
        clique = G_sol.nodes[node]["clique"].split("-")
        n_nodes += len(clique)
        cliques.append(clique)

    if n_nodes != len(G.nodes):
        return "Il numero dei nodi non coincide"

    def isClique(G, clique):
        for i in range(len(clique)):
            for j in range(i+1, len(clique)):
                if not G.has_edge(clique[i], clique[j]):
                    return False
                else:
                    G.remove_edge(clique[i], clique[j])
        return True

    for clique in cliques:
        if not isClique(G, clique):
            return "L'insieme di vertici {} non è una clique nel grafo di input".format(clique)
    if val == len(G.edges):
        return True
    else:
        return "val = {} ed è diverso dal numero di edge rimanenti {} se eliminate le clique ".format(val, len(G.edges))


def deleted_edge_greedy(G):
    rangedHeap = RangedHeap(G)

    sol_value = 0

    while len(rangedHeap) != 0:
        e, val = rangedHeap.getMin(G)
        sol_value += val
        edge_contraction(G, e, rangedHeap)

    return sol_value
