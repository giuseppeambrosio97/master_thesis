import networkx as nx

from clustering_deletion_deleted_edge_greedy.deleted_edge_greedy import preprocess
from src.clustering_deletion_weight_greedy.clustering_deletion_edge_greedy import RangedHeap
if __name__ == "__main__":
    edge_list = [('1', '2'), ('2', '3'), ('1', '3'), ('1', '9'), ('1', '7'), ('1', '8'), ('7', '8'),
                 ('7', '9'), ('8', '9'), ('3', '4'), ('3', '5'), ('3', '6'), ('4', '6'), ('4', '5'), ('5', '6')]
    G = nx.Graph(edge_list)
    nx.set_edge_attributes(G, 1, 'weight')
    nx.set_node_attributes(G, "", "labels")

    for node in G.nodes:
        G.nodes[node]["labels"] = str(node)

    preprocess(G)
    r = RangedHeap(G)
    r.prinf_bool_fs()
    r.print_fs()
    print(r.getRand())

    print("_________________________________************************************____________________________________________")
    r.prinf_bool_fs()
    r.print_fs()
    print(r.getRand())

    print("_________________________________************************************____________________________________________")
    r.prinf_bool_fs()
    r.print_fs()
    print(r.getRand())
    
    print("_________________________________************************************____________________________________________")
    r.prinf_bool_fs()
    r.print_fs()
