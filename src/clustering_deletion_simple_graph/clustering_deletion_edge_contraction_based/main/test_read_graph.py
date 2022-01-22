from src.clustering_deletion_simple_graph.util.util_exp import read_graph
import networkx as nx

if __name__ == "__main__":
    dataset = "data/bio/bio-CE-GT copy.edges"
    G = read_graph(dataset)
    print(len(list(G.nodes)))
    print(len(list(G.edges)))

    H = nx.read_edgelist(dataset, create_using=nx.Graph(), nodetype=str)

    print(len(list(H.nodes)))
    print(len(list(H.edges)))
