class UPrefixCompressedLinearGraph:
    def __init__(self, n, prefixCode):
        self.n = n
        self.prefixCode = prefixCode

    def getU(self,i):
        if i >= 0 and i < len(self.prefixCode):
            return self.prefixCode[i]
        elif i >= len(self.prefixCode) and  i <  self.n-1:
            return self.n-1
        elif i == self.n-1: #last node
            return "For the last node the upper bound is not defined"
        else:
            return "Index error"
