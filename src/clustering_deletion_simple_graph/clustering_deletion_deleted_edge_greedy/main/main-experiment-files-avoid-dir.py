import networkx as nx
import time
import pandas as pd
from src.clustering_deletion_edge_contraction_based.util_exp import read_graph, read_dataset
from src.clustering_deletion_deleted_edge_greedy.deleted_edge_greedy_avoid_G import deleted_edge_greedy_avoid, check_solution
if __name__ == "__main__":

    car = "HC_large"

    datasetdir = "data/exp/{}/{}/".format("inputs", car)


    datasets = read_dataset(datasetdir)

    columns = ["Dataset name", "n", "m","Solution value", "Time", "isCorrect"]

    df = pd.DataFrame(
        columns=columns, index=range(len(datasets)))


    for i,dataset in enumerate(datasets):
        G = read_graph(dataset)

        G_sol = G.copy()

        start_k = time.time()
        value = deleted_edge_greedy_avoid(G_sol)
        end_k = time.time() - start_k
        isCorrect = check_solution(G.copy(), G_sol, value)

        df.at[i, "Dataset name"] = dataset
        df.at[i, "n"] = len(G.nodes)
        df.at[i, "m"] = len(G.edges)
        df.at[i, "Solution value"] = value
        df.at[i, "Time"] = end_k
        df.at[i, "isCorrect"] = isCorrect

    df.to_csv("data/exp/{}/{}.csv".format("outputs", car))
    print(df)

