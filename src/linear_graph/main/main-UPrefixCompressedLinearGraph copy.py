from src.linear_graph.UPrefixCompressedLinearGraph import UPrefixCompressedLinearGraph

if __name__ == "__main__":
    upperBound = [2, 2, 3, 5, 6]
    ul_LinearGraph = UPrefixCompressedLinearGraph(7,upperBound)

    print(ul_LinearGraph.getU(6))
