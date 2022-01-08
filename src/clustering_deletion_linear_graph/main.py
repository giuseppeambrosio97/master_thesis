from src.linear_graph.ULCompressedLinearGraph import ULCompressedLinearGraph
from clustering_deletion_linear_graph.dynamic_programming import DP_clustering_deletion_linear_graph


if __name__ == "__main__":
    upperBound = [2, 2, 3, 5, 6, 6]
    lowerBound = [0, 0, 2, 3, 3, 4]
    ul_LinearGraph = ULCompressedLinearGraph(lowerBound, upperBound)

    print(DP_clustering_deletion_linear_graph(ul_LinearGraph))
