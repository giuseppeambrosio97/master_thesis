from src.linear_graph.UCompressedLinearGraph import UCompressedLinearGraph

if __name__ == "__main__":
    upperBound = [2, 2, 3, 5, 6, 6]
    ul_LinearGraph = UCompressedLinearGraph(upperBound)

    print(ul_LinearGraph.getU(3))
