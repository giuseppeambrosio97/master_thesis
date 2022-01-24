from src.linear_graph.UPrefixCompressedLinearGraph import UPrefixCompressedLinearGraph
from src.clustering_deletion_linear_graph.deleted_edge_greedy import deleted_edge_greedy


if __name__ == "__main__":
    upperBound = [2, 2, 3, 5, 6]
    ul_LinearGraph = UPrefixCompressedLinearGraph(7, upperBound)

    value, clusters = deleted_edge_greedy(ul_LinearGraph)
    print("value ", value)
    print("clusters ", clusters)
