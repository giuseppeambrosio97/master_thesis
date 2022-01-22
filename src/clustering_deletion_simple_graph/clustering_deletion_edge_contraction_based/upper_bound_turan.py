import math
import scipy.special as sc


def upper_bound_turan(n, m):
    ni = n
    mi = m
    val = 0

    while(ni > 0 and mi > 0):
        ri = r(n, m)
        print("ri ", ri)
        edge_to_del = edge_to_delete(ri, ni)
        print("edge to del ", edge_to_del)
        val += (ni-ri)*ri
        ni -= ri
        mi -= edge_to_del

    return val


def r(n, m):
    nn = n*n
    return 1 + math.floor(nn/(nn-2*m))


def edge_to_delete(r, ni):
    return (ni-r)*r + int(sc.binom(r, 2))
