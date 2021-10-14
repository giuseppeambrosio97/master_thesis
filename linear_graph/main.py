def main(item):
    pass


import math as mt

def solve(item):
    maxidispari = -mt.inf
    minpari = mt.inf
    for i,val in enumerate(item):
        if val % 2 != 0:
            maxidispari=max(maxidispari,val)
        elif val % 2 == 0: 
            minpari = min(minpari,val)

    maxidispari2 = -mt.inf
    minpari2 = mt.inf

    for i,val in enumerate(item):
        if val != maxidispari and val != minpari:
            if val % 2 != 0:
                maxidispari2=max(maxidispari2,val)
            elif val % 2 == 0: 
                minpari2 = min(minpari2,val)



    return maxidispari2,minpari2


item = [1,2,3,4,5]

print(solve(item))
