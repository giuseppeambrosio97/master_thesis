class RangedHeap:
    def __init__(self, G):
        self.size = len(G.edges)
        self.fs = [{} for _ in range(len(G.nodes))]
        self.bool_fs = []

        for e in G.edges:
            val = f(G, e)
            G[e[0]][e[1]]['f'] = val
            e = self.get_e(e[0], e[1])
            self.fs[val][e] = e

        for id, id_map in enumerate(self.fs):
            if len(id_map) != 0:
                self.bool_fs.append(id)

    def getMin(self):
        if self.size >= 1:
            out = self.fs[self.bool_fs[0]].popitem()[1]
            self.size -= 1
            if len(self.fs[self.bool_fs[0]]) == 0:
                del self.bool_fs[0]
            return out
        else:
            print("RangedHeap is empty")

    def delete_e(self, e0, e1, f):
        e = self.get_e(e0, e1)
        # f = self.G[e[0]][e[1]]['f']
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


def f(G, e):
    vicini0 = set(G.neighbors(e[0]))
    vicini1 = set(G.neighbors(e[1]))

    A = vicini0 - vicini1  # vicini di e[0] e non di e[1]
    C = vicini1 - vicini0

    value = 0

    for node in A:  # removed
        if node != e[1]:
            value += G[e[0]][node]['weight']

    for node in C:  # removed
        if node != e[0]:
            value += G[e[1]][node]['weight']

    return value


def edge_contraction(G, e, rangedHeap):
    vicini0 = set(G.neighbors(e[0]))
    vicini1 = set(G.neighbors(e[1]))

    Ne0_e1 = vicini0 - vicini1  # vicini di e[0] e non di e[1]
    Ne0_e1.remove(e[1])

    Ne0e1 = vicini0 & vicini1  # vicini di e[0] e di e[1]

    Ne1_e0 = vicini1 - vicini0  # vicini di e[1] e non di e[0]
    Ne1_e0.remove(e[0])

    for node in Ne0e1:
        G[e[0]][node]['weight'] += G[e[1]][node]['weight']
        rangedHeap.delete_e(e[0], node, G[e[0]][node]['f'])
        rangedHeap.delete_e(e[1], node, G[e[1]][node]['f'])

    for node in Ne0_e1:  # removed
        rangedHeap.delete_e(e[0], node, G[e[0]][node]['f'])
        G.remove_edge(e[0], node)

    for node in Ne1_e0:  # removed
        rangedHeap.delete_e(e[1], node, G[e[1]][node]['f'])

    G.nodes[e[0]]["labels"] += "-" + G.nodes[e[1]]["labels"]
    G.remove_node(e[1])

    for node in Ne0e1:
        new_f = f(G, (e[0], node))
        G[e[0]][node]['f'] = new_f
        rangedHeap.add(e[0], node, new_f)

    toAdjust = G.edges(list(Ne0_e1)+list(Ne0e1)+list(Ne1_e0))
    for edge in toAdjust:
        if edge[0] != e[0] and edge[1] != e[0]:
            new_f = f(G, edge)
            old_f = G[edge[0]][edge[1]]['f']
            if new_f != old_f:
                G[edge[0]][edge[1]]['f'] = new_f
                rangedHeap.adjust(edge[0], edge[1], old_f, new_f)


def clustering_deleteting_choice_deleted_edge_greedy(G):
    rangedHeap = RangedHeap(G)
    value = 0
    while len(rangedHeap) != 0:
        e = rangedHeap.getMin()
        value += G[e[0]][e[1]]['f']
        edge_contraction(G, e, rangedHeap)
    return value
