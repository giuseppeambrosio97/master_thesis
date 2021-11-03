from ULCompressedLinearGraph import *

if __name__ == "__main__":
    upperBound = [2, 2, 3, 5, 6, 6]
    lowerBound = [0, 0, 2, 3, 3, 4]
    ul_LinearGraph = ULCompressedLinearGraph(
        lowerBound, upperBound)

    print(ul_LinearGraph.getU(4))
