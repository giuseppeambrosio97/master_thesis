
import math
from src.clustering_deletion_edge_contraction_based.clustering_deletion_edge_contraction import edge_contraction

DP = {}


def DP_cd_edge_contraction(G):
    if len(G.edges) == 0:
        return 0
    else:
        val_min = math.inf
        for e in G.edges:
            H = G.copy()
            val = edge_contraction(H, e)
            val += DP_cd_edge_contraction(H)
            if(val < val_min):
                val_min = val
        return val_min


