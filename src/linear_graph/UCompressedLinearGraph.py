class UpperBoundCompressedLinearGraph:

  def __init__(self, upperBound):
    self.upperBound = upperBound

  def getU(self,i):
    if i < len(self.upperBound):
      return self.upperBound[i]
    elif i >= len(self.upperBound):
      return self.upperBound[-1]
