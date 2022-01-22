import networkx as nx
import time
from src.clustering_deletion_simple_graph.clustering_deletion_deleted_edge_greedy.deleted_edge_greedy import deleted_edge_greedy, check_solution
if __name__ == "__main__":
    edge_list = [('1', '2'), ('2', '3'), ('1', '3'), ('1', '9'), ('1', '7'), ('1', '8'), ('7', '8'),
                 ('7', '9'), ('8', '9'), ('3', '4'), ('3', '5'), ('3', '6'), ('4', '6'), ('4', '5'), ('5', '6')]
    G = nx.Graph(edge_list)
    G_sol = G.copy()
    nx.set_edge_attributes(G_sol, 1, 'weight')
    nx.set_edge_attributes(G_sol, -1, 'f')
    nx.set_node_attributes(G_sol, "", "clique")
    nx.set_edge_attributes(G_sol, None, "EdgeBean")

    for node in G_sol.nodes:
        G_sol.nodes[node]["clique"] = str(node)

    start_k = time.time()
    value = deleted_edge_greedy(G_sol)
    end_k = time.time() - start_k
    isCorrect = check_solution(G.copy(), G_sol, value)
    print("isCorrect ", isCorrect)
    print("execution time ", end_k)
    print("value ", value)
