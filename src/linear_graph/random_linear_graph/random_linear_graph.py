import numpy as np
import scipy.special as sc


def generalization_catalan_numeber(i, ui):
  pass


def catalan_number(n):
  ans = 1.0
  for k in range(2, n+1):
     ans = ans * (n+k)/k
  return int(ans)


def uniform_distribution(i, ui, n):
  norm = n-max(ui, i)
  p = 1/norm
  distribution = [p for _ in range(norm)]
  return distribution


def getDistribution(i, ui, n, method):
  return method(i, ui, n)


def real_uniform_distribution(i, ui, n):
  """
    :param i: the index of the previous node for which we want to generate u
    :param ui: the u of the previous node (i-1)
    :param n: the number of the nodes

    :return d: the distribution over the value that u (of the current node i) can assume
                the value that u can assume are in the range of {t,t+1,...,n-1}
  """
  # if i >= ui:
  #   print("i must be less than u(i)")
  # if i <= 0:
  #   print("i must be greater or equal to 1")
  # if i >= n:
  #   print("i must be less than n")

  t = max(i+1, ui)
  d = np.zeros(n+1-t)
  norm = C(i, ui, n)
  for j, k in enumerate(range(t, n+1)):
    p = C(i+1, k, n)
    d[j] = (p/norm)
  return d


def C(i, j, n):
  """
    Given the number of nodes C(i,j,n) count the number of linear graph that have u(i) = j
  """
  return (int(sc.binom(2*n-i-j, n-i))*(j-i+1))//(n-i+1)


def random_linear_graph(n):
  """
    :param n: integer
    :return u: a compressed version of the graph.
  """

  if n <= 0:
    return "n must be greater or equal to 1"

  if n == 1:
    return []

  u = []
  d = getDistribution(0, 0, n, method=real_uniform_distribution)
  u.append(np.random.choice(range(1, n+1), size=1, p=d)[0])
  u[0] -= 1

  if n == 2:
    return u

  i = 1

  # while u[-1] < n and i <= n-2:
  #   d = getDistribution(i, u[-1], n, method=real_uniform_distribution)
  #   d /= d.sum()
  #   ui = np.random.choice(range(max(u[-1], i+1), n+1), size=1, p=d)[0]
  #   u.append(ui)
  #   i += 1

  while getui(u,-1) < n and i <= n-2:
    d = getDistribution(i, getui(u, -1), n, method=real_uniform_distribution)
    d /= d.sum()
    ui = np.random.choice(range(max(getui(u, -1), i+1), n+1), size=1, p=d)[0]
    u.append(ui-1)
    i += 1

  return u

def getui(u,i):
  return u[i]+1
