import math

def deleted_edge_greedy(uPrefixLinearGraph):
    clusters = []
    val = 0
    j = 0
    
    while uPrefixLinearGraph.getU(j) < len(uPrefixLinearGraph)-1:
        fi = 0
        min_i = j
        min_fi = math.inf
        for i in range(uPrefixLinearGraph.getU(j)+1-j):
            fi = uPrefixLinearGraph.getU(j+i) -j + fi - 2*i
            if fi < min_fi:
                min_fi = fi
                min_i = i
        clusters.append((j,j+min_i))
        j+=min_i+1
        val += min_fi

    clusters.append((j, len(uPrefixLinearGraph)-1))
    
    return val, clusters
    
