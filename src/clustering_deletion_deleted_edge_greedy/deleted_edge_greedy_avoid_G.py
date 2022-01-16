import math


class EdgeBean:
    def __init__(self, weight, e0, e1, Ne0_e1, Ne0e1, Ne1_e0, f) -> None:
        self.weight = weight
        self.e0 = e0
        self.e1 = e1
        self.Ne0_e1 = Ne0_e1
        self.Ne0e1 = Ne0e1
        self.Ne1_e0 = Ne1_e0
        self.old_f = f
        self.f = f

    def adjust_f(self):
        self.old_f = self.f

    def delete_v_out_Ne0_e1(self,v):
        if v in self.Ne0_e1:
            self.Ne0_e1.remove(v)
        else:
            print("ERRORE nodo non nel vicinato, ho cercato di eliminare il node v ", v)
            self.print_EdgeBean()

    def delete_v_out_Ne1_e0(self, v):
        if v in self.Ne1_e0:
            self.Ne1_e0.remove(v)
        else:
            print("ERRORE nodo non nel vicinato, ho cercato di eliminare il node v ", v)
            self.print_EdgeBean()


    def delete_v_in(self, v):
        if v in self.Ne0e1:
            self.Ne0e1.remove(v)
        else:
            print("ERRORE nodo non nel vicinato, ho cercato di eliminare il node v ", v)
            self.print_EdgeBean()
    
    def delete_v_out_Ne0_e1_f(self, G,v):
        if v in self.Ne0_e1:
            self.Ne0_e1.remove(v)
            self.f -= G[self.e0][v]["EdgeBean"].weight
        else:
            print("ERRORE nodo non nel vicinato, ho cercato di eliminare il node v ", v)
            self.print_EdgeBean()

    def delete_v_out_Ne1_e0_f(self,G,v):
        if v in self.Ne1_e0:
            self.Ne1_e0.remove(v)
            self.f -= G[self.e1][v]["EdgeBean"].weight
        else:
            print("ERRORE nodo non nel vicinato, ho cercato di eliminare il node v ", v)
            self.print_EdgeBean()

    def add_v_out_Ne0_e1(self, G, v):
        self.Ne0_e1.add(v)
        self.f += G[self.e0][v]["EdgeBean"].weight
        
    def add_v_out_Ne1_e0(self, G, v):
        self.Ne1_e0.add(v)
        self.f += G[self.e1][v]["EdgeBean"].weight




    def print_EdgeBean(self):
        print("weight ", self.weight)
        print("e0 {} e1 {}".format(self.e0, self.e1))
        print("Ne0_e1 ", self.Ne0_e1)
        print("Ne0e1 ", self.Ne0e1)
        print("Ne1_e0 ", self.Ne1_e0)
        print("olf_f {} f {}".format(self.old_f, self.f))

    def merge(self, edgeBean, G):
        # self.weight += edgeBean.weight
        self.Ne0e1 = self.Ne0e1.intersection(edgeBean.Ne0e1)

        if self.e1 == edgeBean.e1:
            self.Ne0_e1 = self.Ne0_e1.intersection(edgeBean.Ne0_e1)
            self.Ne1_e0 = self.Ne1_e0.union(edgeBean.Ne1_e0)
        elif self.e0 == edgeBean.e0:
            self.Ne1_e0 = self.Ne1_e0.intersection(edgeBean.Ne1_e0)
            self.Ne0_e1 = self.Ne0_e1.union(edgeBean.Ne0_e1)
        elif self.e0 == edgeBean.e1:
            self.Ne1_e0 = self.Ne1_e0.intersection(edgeBean.Ne0_e1)
            self.Ne0_e1 = self.Ne0_e1.union(edgeBean.Ne1_e0)
        elif self.e1 == edgeBean.e0:
            self.Ne0_e1 = self.Ne0_e1.intersection(edgeBean.Ne1_e0)
            self.Ne1_e0 = self.Ne1_e0.union(edgeBean.Ne0_e1)
        self.f = f_with_edgeBean(self, G)

        return True if self.old_f != self.f else False


class RangedHeap:
    def __init__(self, G) -> None:
        self.size = len(G.edges)
        self.fs = [{} for _ in range(len(G.nodes))]
        self.bool_fs = []
        # self.edges = {}

        for e in G.edges:
            e = self.get_e(e[0], e[1])
            Ne0_e1, Ne0e1, Ne1_e0 = split_neighborhood(G, e)
            val = len(Ne0_e1) + len(Ne1_e0)
            G[e[0]][e[1]]['f'] = val
            self.fs[val][e] = e
            G[e[0]][e[1]]['EdgeBean'] = EdgeBean(
                1, e[0], e[1], Ne0_e1, Ne0e1, Ne1_e0, val)
            # self.edges[e] = EdgeBean(1, e[0], e[1], Ne0_e1, Ne0e1, Ne1_e0, val)

        for id, id_map in enumerate(self.fs):
            if len(id_map) != 0:
                self.bool_fs.append(id)

    def getMin(self, G):
        if self.size >= 1:
            e = self.getMinTwins(G)
            # out = self.fs[self.bool_fs[0]].popitem()[1]
            self.size -= 1
            f_val = self.bool_fs[0]
            if len(self.fs[f_val]) == 0:
                del self.bool_fs[0]

            return G[e[0]][e[1]]['EdgeBean'], f_val
            # return self.edges.pop(e), f_val
        else:
            print("RangedHeap is empty")

    def getMinTwins(self, G):
        weight_max = -math.inf
        edge_to_pick = None
        for _, e in self.fs[self.bool_fs[0]].items():
            w = G[e[0]][e[1]]['EdgeBean'].weight
            if weight_max < w:
                weight_max = w
                edge_to_pick = e
        del self.fs[self.bool_fs[0]][edge_to_pick]
        return edge_to_pick

    def delete_e(self, e0, e1, f):
        e = self.get_e(e0, e1)
        del self.fs[f][e]
        self.size -= 1

        if len(self.fs[f]) == 0:
            self.binary_search_delete(f)

    def delete_e_old(self, e0, e1, old_f):
        e = self.get_e(e0, e1)
        del self.fs[old_f][e]
        self.size -= 1

        if len(self.fs[old_f]) == 0:
            self.binary_search_delete(old_f)

    def add(self, e0, e1, f):
        e = self.get_e(e0, e1)
        if len(self.fs[f]) == 0:
            self.binary_search_add(f)
        self.fs[f][e] = e
        self.size += 1

    def adjust(self, G, e0, e1):
        edgeBean = G[e0][e1]['EdgeBean']

        old_f = edgeBean.old_f
        self.delete_e_old(e0, e1, old_f)

        f = edgeBean.f
        self.add(e0, e1, f)

        edgeBean.adjust_f()

    def merge_and_add(self, G, edge1, edge2):
        edgeBean1 = G[edge1[0]][edge1[1]]['EdgeBean']
        edgeBean2 = G[edge2[0]][edge2[1]]['EdgeBean']

        self.delete_e(edge2[0], edge2[1], edgeBean2.f)

        if edgeBean1.merge(edgeBean2, G):
            self.adjust(G, edge1[0], edge1[1])

        # self.add(edge1[0], edge1[1], edgeBean1.f)

    # def delete_edges_e(self,e0,e1):
    #     e = self.get_e(e0, e1)
    #     del self.edges[e]

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

    # def getWeight_e(self, e):
    #     e = self.get_e(e[0], e[1])
    #     return self.edges[e].weight

    def get_e(self, e0, e1):
        return (e0, e1) if int(e0) < int(e1) else (e1, e0)

    # def print_edges(self):
    #     for key, value in self.edges.items():
    #         print("__________________")
    #         print("key", key)
    #         print("----> value ")
    #         value.print_EdgeBean()

    def print_fs(self):
        for id, id_map in enumerate(self.fs):
            values = ""
            for key, value in id_map.items():
                values += " " + str(value)
            s = "[" + str(id) + "]->" + values + "\n"
            print(s)

    def prinf_bool_fs(self):
        print(self.bool_fs)

    def print_rangedHeap(self):
        self.print_fs()
        self.prinf_bool_fs()

    def __len__(self):
        return self.size


def preprocess(G):
    rangedHeap = RangedHeap(G)
    value = 0
    while True:
        e = rangedHeap.getMin(G)
        if(G[e[0]][e[1]]['f'] > 0):
            break
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


def f(G, e):
    Ne0_e1, Ne1_e0 = xor(G, e)
    value = 0

    for node in Ne0_e1:  # removed
        value += G[e[0]][node]['weight']

    for node in Ne1_e0:  # removed
        value += G[e[1]][node]['weight']

    return value


def f_with_sets(G, e, Ne0_e1, Ne1_e0):
    value = 0

    for node in Ne0_e1:  # removed
        value += G[e[0]][node]['weight']

    for node in Ne1_e0:  # removed
        value += G[e[1]][node]['weight']

    return value


def f_with_edgeBean(edgeBean, G):
    value = 0

    for node in edgeBean.Ne0_e1:  # removed
        value += G[edgeBean.e0][node]['EdgeBean'].weight

    for node in edgeBean.Ne1_e0:  # removed
        value += G[edgeBean.e1][node]['EdgeBean'].weight

    return value


def edge_contraction(G, e_edgeBean, rangedHeap):
    e = (e_edgeBean.e0, e_edgeBean.e1)
    Ne0_e1, Ne0e1, Ne1_e0 = e_edgeBean.Ne0_e1, e_edgeBean.Ne0e1, e_edgeBean.Ne1_e0

    for node in Ne0_e1:  # removed
        rangedHeap.delete_e(e[0], node, G[e[0]][node]["EdgeBean"].f)

    for node in Ne1_e0:  # removed
        rangedHeap.delete_e(e[1], node, G[e[1]][node]["EdgeBean"].f)
    
    for node in Ne0e1:
        G[e[0]][node]['EdgeBean'].weight += G[e[1]][node]['EdgeBean'].weight

    for node in Ne0e1:
        rangedHeap.merge_and_add(G, (e[0], node), (e[1], node))

    toAdjust_in_rangedHeap = set()

    # toAdjust_Ne0e1 = fil(G.edges(list(Ne0e1)), e[0], e[1])

    # for edge in toAdjust_Ne0e1:
    #     if edge[0] != e[0] and edge[1] != e[0]:  # REMOVE e[1] dagl'insiemi
    #         edgeBean = G[edge[0]][edge[1]]["EdgeBean"]
    #         edgeBean.delete_v_B(e[1])

    # toAdjust_Ne0_e1 = fil(G.edges(list(Ne0_e1)), e[0], e[1])

    # # eliminare dai vicini e[0] e nel caso sta in A,C allora occorre modificare f altrimenti niente
    # for edge in toAdjust_Ne0_e1:
    #     edgeBean = G[edge[0]][edge[1]]["EdgeBean"]
    #     if edgeBean.delete_v(G, e[0]):
    #         toAdjust.add(edge)

    # toAdjust_Ne1_e0 = fil(G.edges(list(Ne1_e0)), e[0], e[1])

    # # eliminare dai vicini e[0] e nel caso sta in A,C allora occorre modificare f altrimenti niente
    # for edge in toAdjust_Ne1_e0:
    #     edgeBean = G[edge[0]][edge[1]]["EdgeBean"]  # REMOVE e[1] dagl'insiemi
    #     # edgeBean.print_EdgeBean()
    #     if edgeBean.delete_v(G, e[1]):
    #         toAdjust.add(edge)
    

    toAdjust_Ne0e1 = fil(G.edges(list(Ne0e1)), e[0], e[1])
    # print("toAdjust_Ne0e1 ", toAdjust_Ne0e1)

    for edge in toAdjust_Ne0e1:
        if edge[0] != e[0] and edge[1] != e[0]:  # REMOVE e[1] dagl'insiemi
            if edge[0] in Ne0e1:
                b = edge[0]
                other = edge[1]
            else:
                b = edge[1]
                other = edge[0]

            edgeBean = G[edge[0]][edge[1]]["EdgeBean"]

            if other in Ne0_e1:                                         # B - A
                if edgeBean.e0 == b:
                    edgeBean.delete_v_out_Ne0_e1(e[1])
                    edgeBean.add_v_out_Ne0_e1(G,e[0])
                else:
                    edgeBean.delete_v_out_Ne1_e0(e[1])
                    edgeBean.add_v_out_Ne1_e0(G,e[0])
                toAdjust_in_rangedHeap.add(edge)
            elif other in Ne0e1:                                        # B - B
                edgeBean.delete_v_in(e[1])
            elif other in Ne1_e0:                                       # B - C
                edgeBean.f += G[e[1]][b]["EdgeBean"].weight
                toAdjust_in_rangedHeap.add(edge)
            else:                                                       # B - ext
                if edgeBean.e0 == b:
                    edgeBean.delete_v_out_Ne0_e1(e[1])
                else:   
                    edgeBean.delete_v_out_Ne1_e0(e[1])

    toAdjust_Ne0_e1 = fil(G.edges(list(Ne0_e1)), e[0], e[1])
    # print("toAdjust_Ne0_e1 ", toAdjust_Ne0_e1)

    # eliminare dai vicini e[0] e nel caso sta in A,C allora occorre modificare f altrimenti niente
    for edge in toAdjust_Ne0_e1:
        if edge[0] in Ne0_e1:
            a = edge[0]
            other = edge[1]
        else:
            a = edge[1]
            other = edge[1]
        
        edgeBean = G[edge[0]][edge[1]]["EdgeBean"]
        
        if other in Ne0_e1:                                         # A - A
            edgeBean.delete_v_in(e[0])
        elif other in Ne0e1:                                        # A - B
            edgeBean.delete_v_in(e[0])
        elif other in Ne1_e0:                                       # A - C
            if edgeBean.e0 == a:
                edgeBean.delete_v_out_Ne0_e1_f(G,e[0])
            else:
                edgeBean.delete_v_out_Ne1_e0_f(G, e[0])
            toAdjust_in_rangedHeap.add(edge)
        else:                                                       # A - ext
            if edgeBean.e0 == a:
                edgeBean.delete_v_out_Ne0_e1_f(G, e[0])
            else:
                edgeBean.delete_v_out_Ne1_e0_f(G, e[0])
            toAdjust_in_rangedHeap.add(edge)

    toAdjust_Ne1_e0 = fil(G.edges(list(Ne1_e0)), e[0], e[1])
    # print("toAdjust_Ne1_e0 ", toAdjust_Ne1_e0)

    # eliminare dai vicini e[0] e nel caso sta in A,C allora occorre modificare f altrimenti niente
    for edge in toAdjust_Ne1_e0:
        if edge[0] in Ne1_e0:
            c = edge[0]
            other = edge[1]
        else:
            c = edge[1]
            other = edge[0]

        edgeBean = G[edge[0]][edge[1]]["EdgeBean"]  # REMOVE e[1] dagl'insiemi

        if other in Ne0_e1:                                     # C - A
            if edgeBean.e0 == c:
                edgeBean.delete_v_out_Ne0_e1_f(G, e[1])
            else:
                edgeBean.delete_v_out_Ne1_e0_f(G, e[1])
            toAdjust_in_rangedHeap.add(edge)
        elif other in Ne0e1:                                    # C - B
            edgeBean.delete_v_in(e[1])
        elif other in Ne1_e0:                                   # C - C
            edgeBean.delete_v_in(e[1])
        else:                                                   # C - ext
            if edgeBean.e0 == c:
                edgeBean.delete_v_out_Ne0_e1_f(G, e[1])
            else:
                edgeBean.delete_v_out_Ne1_e0_f(G, e[1])
            toAdjust_in_rangedHeap.add(edge)
    




    for edge in toAdjust_in_rangedHeap:
        rangedHeap.adjust(G, edge[0], edge[1])

    for node in Ne0_e1:  # removed
        G.remove_edge(e[0], node)

    G.nodes[e[0]]["labels"] += "-" + G.nodes[e[1]]["labels"]
    G.remove_node(e[1])

    # print("to delete " , deleted_edge)


def fil(l, e0, e1):
    s = set()
    s.add(e0)
    s.add(e1)

    l_ = []

    for edge in l:
        if edge[0] not in s and edge[1] not in s:
            l_.append(edge)
    return l_


def check_solution(G, G_sol, val):

    cliques = []
    n_nodes = 0
    for node in G_sol.nodes:
        clique = G_sol.nodes[node]["labels"].split("-")
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



def deleted_edge_greedy_avoid(G):
    rangedHeap = RangedHeap(G)
    # rangedHeap.edges[('1','7')].print_EdgeBean()

    # rangedHeap.edges[('1', '9')].print_EdgeBean()

    # rangedHeap.edges[('1', '7')].merge(
    #     rangedHeap.edges[('1', '9')], rangedHeap)

    # rangedHeap.print_edges()
    # rangedHeap.edges[('1', '7')].print_EdgeBean()

    # print("____________________________")

    sol_val = 0

    # for e in G.edges:
    #     G[e[0]][e[1]]['EdgeBean'].print_EdgeBean()
    #     print("-------------------------------------")

    # rangedHeap.print_fs()
    while len(rangedHeap) != 0:
        edgeBean, val = rangedHeap.getMin(G)
        # print("TO CONTRACT {} {}".format(edgeBean.e0, edgeBean.e1))
        sol_val += val
        edge_contraction(G, edgeBean, rangedHeap)
        # for e in G.edges:
        #     G[e[0]][e[1]]['EdgeBean'].print_EdgeBean()
        #     print("-------------------------------------")

        # print(G.nodes)

        # s = ""
        # for node in G.nodes:
        #     s += G.nodes[node]["labels"] + "|"
        # print(s)
        # print("SIZE ", len(rangedHeap))
        # print(rangedHeap.edges.keys())
        # edgeBean.print_EdgeBean()
        # print("*******************************************")

        # print(rangedHeap.edges.keys())
        # rangedHeap.print_fs()
        # print("sssss " ,rangedHeap.size)
    return sol_val
