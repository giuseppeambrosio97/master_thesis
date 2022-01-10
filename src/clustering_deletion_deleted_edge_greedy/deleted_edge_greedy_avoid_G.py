import math


class EdgeBean:
    def __init__(self, weight,e0,e1, Ne0_e1, Ne0e1, Ne1_e0, f) -> None:
        self.weight = weight
        self.e0 = e0
        self.e1 = e1
        self.Ne0_e1 = Ne0_e1
        self.Ne0e1 = Ne0e1
        self.Ne1_e0 = Ne1_e0
        self.old_f = f
        self.f = f
    
    def delete_Ne0_e1_node(self, v):
        self.Ne0_e1.remove(v)

    def add_Ne0_e1_node(self,v):
        self.Ne0_e1.add(v)

    def delete_Ne1_e0_node(self, v):
        self.Ne1_e0.remove(v)

    def add_Ne1_e0_node(self, v):
        self.Ne1_e0.add(v)

    def delete_Ne0e1_node(self, v):
        self.Ne0e1.remove(v)

    def add_Ne0e1_node(self, v):
        self.Ne0e1.add(v)

    def adjust_f(self):
        self.old_f = self.f

    def delete_v(self, rangedHeap, v):
        """
            return True se l'edge è da sistemare nella rangedHeap
        """
        if v in self.Ne0_e1:
            self.Ne0_e1.remove(v)
            self.f -= rangedHeap.getWeight_e((self.e0, v))
            return True
        elif v in self.Ne1_e0:
            self.Ne1_e0.remove(v)
            self.f -= rangedHeap.getWeight_e((self.e1, v))
            return True
        elif v in self.Ne0e1:
            self.Ne0e1.remove(v)
            return False
        else:
            print("ERRORE nodo non nel vicinato, ho cercato di eliminare il node v ", v)
            self.print_EdgeBean()

    def delete_v_B(self,v):
        if v in self.Ne0_e1:
            self.Ne0_e1.remove(v)
            # return True
        elif v in self.Ne1_e0:
            self.Ne1_e0.remove(v)
            # self.f -= rangedHeap.getWeight_e((self.e1, v))
            # return True
        elif v in self.Ne0e1:
            self.Ne0e1.remove(v)
            # return False
        else:
            print("ERRORE nodo non nel vicinato, ho cercato di eliminare il node v ", v)
            self.print_EdgeBean()


    def print_EdgeBean(self):
        print("weight ", self.weight)
        # print("e0 {} e1 {}".format(self.e0,self.e1))
        print("Ne0_e1 ", self.Ne0_e1)
        print("Ne0e1 ", self.Ne0e1)
        print("Ne1_e0 ", self.Ne1_e0)
        print("olf_f {} f {}".format(self.old_f, self.f))
    
    def merge(self, edgeBean,rangedHeap):
        self.weight += edgeBean.weight
        self.Ne0_e1 = self.Ne0_e1.intersection(edgeBean.Ne0_e1)
        self.Ne0e1 = self.Ne0e1.intersection(edgeBean.Ne0e1)
        self.Ne1_e0 = self.Ne1_e0.intersection(edgeBean.Ne1_e0)
        self.f = f_with_edgeBean(self,rangedHeap)
        self.old_f = self.f
    
class RangedHeap:
    def __init__(self, G):
        self.size = len(G.edges)
        self.fs = [{} for _ in range(len(G.nodes))]
        self.bool_fs = []
        self.edges = {}

        for e in G.edges:
            e = self.get_e(e[0], e[1])
            Ne0_e1, Ne0e1, Ne1_e0 = split_neighborhood(G,e)
            val = f_with_sets(G,e,Ne0_e1,Ne1_e0)
            # G[e[0]][e[1]]['f'] = val
            self.fs[val][e] = e
            # G[e[0]][e[1]]['EdgeBean'] = EdgeBean(1, e[0],e[1],Ne0_e1, Ne0e1, Ne1_e0, val)
            self.edges[e] = EdgeBean(1, e[0], e[1], Ne0_e1, Ne0e1, Ne1_e0, val)

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
            
            return self.edges.pop(e), f_val
        else:
            print("RangedHeap is empty")

    def getMinTwins(self, G):
        weight_max = -math.inf
        edge_to_pick = None
        for _, e in self.fs[self.bool_fs[0]].items():
            w = G[e[0]][e[1]]['weight']
            if weight_max < w:
                weight_max = w
                edge_to_pick = e
        del self.fs[self.bool_fs[0]][edge_to_pick]
        return edge_to_pick

    def delete_e(self, e0, e1):
        e = self.get_e(e0, e1)
        f = self.edges[e].f
        del self.fs[f][e]
        self.size -= 1

        if len(self.fs[f]) == 0:
            self.binary_search_delete(f)

    def delete_e_old(self, e0, e1):
        e = self.get_e(e0, e1)
        old_f = self.edges[e].old_f
        del self.fs[old_f][e]
        self.size -= 1

        if len(self.fs[old_f]) == 0:
            self.binary_search_delete(old_f)


    def add(self, e0, e1):
        e = self.get_e(e0, e1)
        f = self.edges[e].f
        if len(self.fs[f]) == 0:
            self.binary_search_add(f)
        self.fs[f][e] = e
        self.size += 1

    def adjust(self, e0, e1):
        self.delete_e_old(e0, e1)
        self.add(e0, e1)
        e = self.get_e(e0,e1)
        self.edges[e].adjust_f()

    def merge_and_add(self, edge1,edge2, rangedHeap):
        edge1 = self.get_e(edge1[0], edge1[1])
        edge2 = self.get_e(edge2[0], edge2[1])

        self.delete_e(edge1[0], edge1[1])
        self.delete_e(edge2[0], edge2[1])

        edgeBean1 = self.edges[edge1]
        edgeBean2 = self.edges[edge2]

        edgeBean1.merge(edgeBean2, rangedHeap)

        self.add(edge1[0],edge1[1])

    def delete_edges_e(self,e0,e1):
        e = self.get_e(e0, e1)
        del self.edges[e]



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
    

    def getWeight_e(self,e):
        e = self.get_e(e[0],e[1])
        return self.edges[e].weight

    def add_weight(self, edge1, edge2):
        edge1 = self.get_e(edge1[0], edge1[1])
        edge2 = self.get_e(edge2[0], edge2[1])
        self.edges[edge1].weight += self.edges[edge2].weight

    def setWeight_e(self, e, weight):
        e = self.get_e(e[0], e[1])
        self.edges[e].w = weight

    def getf_e(self, e):
        e = self.get_e(e[0], e[1])
        return self.edges[e].f
    
    def setf_e(self, e, new_f):
        e = self.get_e(e[0], e[1])
        self.edges[e].f = new_f

    def subtract_to_f_e(self, e, weight):
        e = self.get_e(e[0], e[1])
        self.edges[e].f -= weight
        
    def get_EdgeBean_e(self, e):
        e = self.get_e(e[0], e[1])
        return self.edges[e]

    def get_e(self, e0, e1):
        return (e0, e1) if int(e0) < int(e1) else (e1, e0)

    def print_edges(self):
        for key, value in self.edges.items():
            print("__________________")
            print("key", key)
            print("----> value ")
            value.print_EdgeBean()

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
        self.print_edges()

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


def f_with_edgeBean(edgeBean,rangedHeap):
    value = 0

    for node in edgeBean.Ne0_e1:  # removed
        value += rangedHeap.getWeight_e((edgeBean.e0,node))

    for node in edgeBean.Ne1_e0:  # removed
        value += rangedHeap.getWeight_e((edgeBean.e1, node))

    return value


def edge_contraction(G, e_edgeBean, rangedHeap):
    e = (e_edgeBean.e0,e_edgeBean.e1)
    Ne0_e1, Ne0e1, Ne1_e0 = e_edgeBean.Ne0_e1, e_edgeBean.Ne0e1, e_edgeBean.Ne1_e0

    deleted_edge = set()

    for node in Ne0_e1:  # removed
        rangedHeap.delete_e(e[0], node)
        G.remove_edge(e[0], node)
        deleted_edge.add((e[0],node))

    for node in Ne1_e0:  # removed
        rangedHeap.delete_e(e[1], node)
        deleted_edge.add((e[1], node))

    for node in Ne0e1:
        rangedHeap.merge_and_add((e[0], node), (e[1], node),rangedHeap)
        deleted_edge.add((e[1], node))

    G.nodes[e[0]]["labels"] += "-" + G.nodes[e[1]]["labels"]
    G.remove_node(e[1])

    toAdjust = set()

    toAdjust_Ne0e1 = G.edges(list(Ne0e1))

    for edge in toAdjust_Ne0e1:
        if edge[0] != e[0] and edge[1] != e[0]:
            edgeBean = rangedHeap.get_EdgeBean_e(edge) ### REMOVE e[1] dagl'insiemi
            edgeBean.delete_v_B(e[1])


    toAdjust_Ne0_e1 = G.edges(list(Ne0_e1))

    for edge in toAdjust_Ne0_e1: ## eliminare dai vicini e[0] e nel caso sta in A,C allora occorre modificare f altrimenti niente
        edgeBean = rangedHeap.get_EdgeBean_e(edge)
        if edgeBean.delete_v(rangedHeap, e[0]):
            toAdjust.add(edge)

    toAdjust_Ne1_e0 = G.edges(list(Ne1_e0))

    for edge in toAdjust_Ne1_e0: ## eliminare dai vicini e[0] e nel caso sta in A,C allora occorre modificare f altrimenti niente
        edgeBean = rangedHeap.get_EdgeBean_e(edge)  # REMOVE e[1] dagl'insiemi
        if edgeBean.delete_v(rangedHeap, e[1]):
            toAdjust.add(edge)
    
    for edge in toAdjust:
        rangedHeap.adjust(edge[0], edge[1])

    # print("to delete " , deleted_edge)

    for edge in deleted_edge:
        rangedHeap.delete_edges_e(edge[0],edge[1])


    
    # rangedHeap.print_edges()


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
    while len(rangedHeap) != 0:
        edgeBean, val = rangedHeap.getMin(G)
        # print("TO CONTRACT {} {}".format(edgeBean.e0,edgeBean.e1))
        sol_val+=val
        edge_contraction(G, edgeBean, rangedHeap)
        # print(rangedHeap.edges.keys())
        # edgeBean.print_EdgeBean()
        # print("*******************************************")

        # print(rangedHeap.edges.keys())
    return sol_val
