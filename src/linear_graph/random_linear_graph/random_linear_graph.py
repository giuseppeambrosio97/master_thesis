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
  t = max(i+1, ui)
  d = np.zeros(n+1-t)
  norm = C(i, ui, n)
  for j, k in enumerate(range(t, n+1)):
    p = C(i+1, k, n)
    d[j] = (p/norm)
  return d


def C(i, j, n):
  return (int(sc.binom(2*n-i-j, n-i))*(j-i+1))//(n-i+1)


def random_linear_graph(n):
  """
  INPUT:
    n: integer
  OUTPUT:
    graph: a compressed version of the graph.
  """

  if n == 0:
    return []

  if n == 1:
    return [1]

  u = []
  d = getDistribution(0, 0, n, method=real_uniform_distribution)
  u.append(np.random.choice(range(1, n+1), size=1, p=d)[0])

  if n == 2:
    return u

  i = 1

  while u[-1] < n and i <= n-2:
    d = getDistribution(i, u[-1], n, method=real_uniform_distribution)
    d /= d.sum()
    ui = np.random.choice(range(max(u[-1], i+1), n+1), size=1, p=d)[0]
    u.append(ui)
    i += 1

  return u
