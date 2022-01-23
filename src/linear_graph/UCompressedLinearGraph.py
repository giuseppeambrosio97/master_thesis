class UCompressedLinearGraph:

  def __init__(self, upperBound):
    self.upperBound = upperBound

  def getU(self, i):
      if i < len(self.upperBound) and i >= 0:
          return self.upperBound[i]
      elif i == len(self.upperBound): # last node
          return "For the last node the upper bound is not defined"
      else:
          return "Index error"
