import networkx as nx
import time
import pandas as pd
from src.clustering_deletion_edge_contraction_based.util_exp import read_graph, read_dataset
from src.clustering_deletion_deleted_edge_greedy.deleted_edge_greedy_avoid_G import deleted_edge_greedy_avoid, check_solution
if __name__ == "__main__":

    car = "RAND"

    datasetdir = "data/exp/{}/{}/".format("inputs", car)


    datasets = read_dataset(datasetdir)

    df = pd.DataFrame(
        columns=["Solution value", "Time", "isCorrect"], index=range(len(datasets)))


    for i,dataset in enumerate(datasets):
        G = read_graph(dataset)

        G_sol = G.copy()
        nx.set_node_attributes(G_sol, None, "clique")
        nx.set_edge_attributes(G_sol, None, "EdgeBean")

        for node in G_sol.nodes:
            G_sol.nodes[node]["clique"] = set([node])

        start_k = time.time()
        try:
            value = deleted_edge_greedy_avoid(G_sol)
        except:
            print(dataset)
        end_k = time.time() - start_k
        isCorrect = check_solution(G.copy(), G_sol, value)
        df.at[i, "Solution value"] = value
        df.at[i, "Time"] = end_k
        df.at[i, "isCorrect"] = isCorrect

    df.to_csv("data/exp/{}/{}.csv".format("outputs", car))
    print(df)

