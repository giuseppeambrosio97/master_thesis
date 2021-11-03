class ULCompressedLinearGraph:
    lowerBound = []
    upperBound = []

    def __init__(self, lowerBound, upperBound):
        self.lowerBound = lowerBound
        self.upperBound = upperBound

    def getU(self, i):
        if(i < len(self.upperBound) and i >= 0):
            return self.upperBound[i]
        else:
            return "ERRORE indice"

    def getL(self, i):
        if(i <= len(self.upperBound) and i > 0):
            return self.lowerBound[i-1]
        else:
            return "ERRORE indice"

    def __len__(self):
        return len(self.upperBound)+1

    def existEdge(self, i, j):
        if self.getL(i) <= j and self.getU(i):
            return True
        else:
            return False
