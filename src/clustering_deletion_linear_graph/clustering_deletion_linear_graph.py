import math
from linear_graph.ULCompressedLinearGraph import ULCompressedLinearGraph


# def clustering_deletion_linear_graph(upperBoundCompressedLinearGraph):
#     pass


def gl(ul_LinearGraph, t, i):
    """
      Computa il numero di edge che hanno un estremo in S_{0,t-1} e un estremo
      in S_{t,i}. Tale funzione viene implementata sfruttando i lower bound del
      grafo lineare in input, l(.).

      INPUT:

      OUTPUT:
    """

    if t == 0:
        return 0

    sum = t*(i-t+1)
    for k in range(t, i+1):
        sum -= ul_LinearGraph.getL(k)

    return sum

# def gu(ul_LinearGraph, t, i):
#     """
#       Computa il numero di edge che hanno un estremo in S_{i,t-1} e un estremo
#       in S_{t,n-1}. Tale funzione viene implementata sfruttando gli upper bound del
#       grafo lineare in input, u(.)

#       INPUT:

#       OUTPUT:
#     """
#     pass


# p = [False for _ in range(7)]
# def DPR_clustering_deletion_linear_graph(ul_LinearGraph, i):
#   if i == 0 or i == -1:
#     return 0
#   elif p[i] != False:
#     return p[i]
#   else:
#     val = math.inf

#     t = i

#     while t >= ul_LinearGraph.getL(i):
#       val = min(val, DPR_clustering_deletion_linear_graph(
#           ul_LinearGraph, t-1)+gl(ul_LinearGraph, t, i))
#       t -= 1
#     p[i] = val

#     return p[i]


def DP_clustering_deletion_linear_graph(ul_LinearGraph):
    p = [0]
    n = len(ul_LinearGraph)

    for i in range(1, n):
        val = math.inf
        for t in range(i, ul_LinearGraph.getL(i)-1, -1):
            val = min(val, p[t-1]+gl(ul_LinearGraph, t, i))
        p.append(val)

    return p
