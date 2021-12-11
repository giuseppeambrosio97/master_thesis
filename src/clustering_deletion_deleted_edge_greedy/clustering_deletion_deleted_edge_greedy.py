class RangedHeap:
    def __init__(self, G) -> None:
        self.G = G
        self.size = len(self.G.edges)
        self.fs = [{} for _ in range(len(self.G.nodes))]
        self.bool_fs = []

        for e in self.G.edges:
            val = f(self.G, e)
            self.G[e[0]][e[1]]['f'] = val
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

    def delete_e(self, e0, e1):
        e = self.get_e(e0, e1)
        f = self.G[e[0]][e[1]]['f']
        del self.fs[f][e]
        self.size -= 1
        # self.fs[f].pop(str(e))

        if len(self.fs[f]) == 0:
            for i in range(len(self.bool_fs)):
                if f == self.bool_fs[i]:
                    break
            del self.bool_fs[i]

    def add(self, e0, e1, f):
        e = self.get_e(e0, e1)
        if len(self.fs[f]) == 0:
            if f < self.bool_fs[0]:
                self.bool_fs.insert(0, f)
            elif f > self.bool_fs[-1]:
                self.bool_fs.append(f)
            else:
                for i in range(1, len(self.bool_fs)):
                    if self.bool_fs[i-1] < f and f < self.bool_fs[i]:
                        break
                self.bool_fs.insert(i, f)
        self.fs[f][e] = e
        self.size += 1

    def adjust(self, e0, e1, f):
        e = self.get_e(e0, e1)
        old_f = self.G[e[0]][e[1]]['f']
        if old_f != f:
            self.delete_e(e[0], e[1])
            self.add(e[0], e[1], f)
            self.G[e[0]][e[1]]['f'] = f

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

    # def print_d(self):
    #   for key,val in self.d.items():
    #     print("key ", key, " val ", val)

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
        rangedHeap.delete_e(e[0], node)
        rangedHeap.delete_e(e[1], node)

    for node in Ne0_e1:  # removed
        # if node != e[1]:
        rangedHeap.delete_e(e[0], node)
        G.remove_edge(e[0], node)

    for node in Ne1_e0:  # removed
        # if node != e[0]:
        rangedHeap.delete_e(e[1], node)
        ### E' necessario se poi cancello il node e[1]?!
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

    G.nodes[e[0]]["labels"] += "-" + G.nodes[e[1]]["labels"]
    G.remove_node(e[1])

    for node in Ne0e1:
      rangedHeap.add(e[0], node, f(G, (e[0], node)))

    toAdjust = G.edges(list(Ne0_e1)+list(Ne0e1)+list(Ne1_e0))
    for edge in toAdjust:
      if edge[0] != e[0] and edge[1] != e[0]:
        rangedHeap.adjust(edge[0], edge[1], f(G, edge))



def clustering_deleteting_choice_deleted_edge_greedy(G):
    rangedHeap = RangedHeap(G)
    # rangedHeap.print_fs()
    # print("_-------------------------------_")
    conta = 0
    value = 0
    while len(rangedHeap) != 0:
        e = rangedHeap.getMin()
        # print("edge contratto ", e)
        # print("edge contratto super nodi ",
            #   G.nodes[e[0]]["labels"], G.nodes[e[1]]["labels"])
        value += G[e[0]][e[1]]['f']
        conta +=1

        print("value ", value)
        print("conta ", conta)
        edge_contraction(G, e, rangedHeap)
        # print("size  ", len(rangedHeap))
        # rangedHeap.print_fs()
        # print("_-------------------------------_")

        # print("GGGGGGGGGGGG")
        # for node in G.nodes:
        #   print("super nodi ", G.nodes[node]["labels"])
        #   print("-----> ", node)

    return value