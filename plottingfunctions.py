import numpy as np
def createtimeaverage(listtosmooth,n):
    newlist = []
    for i in range(len(listtosmooth)):
        if i < n:
            newlist.append(np.average(listtosmooth))