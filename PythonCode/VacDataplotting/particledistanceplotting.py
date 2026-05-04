import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd
import os


imagefolder = "I:\Apr16\Test1\ImageVectors"






def calculate_centre_distances(vectorfile,n):
        imagedf = pd.read_csv(vectorfile)
        Xcoords,Ycoords = imagedf["CentreX"],imagedf["CentreY"]

        total_distances_pow = 0
        numberofd = 0

        for i in range(len(Xcoords)):
                for j in range(i+1,len(Xcoords)):
                    total_distances_pow += (((Xcoords[i] - Xcoords[j])**2 + (Ycoords[i] - Ycoords[j]) **2 )**0.5)**n
                    numberofd += 1
        rmndistance = (total_distances_pow / numberofd) ** (1/n) 

        return rmndistance


rm2distancelist = []
rm1distancelist = []

for imname in os.listdir(imagefolder)[::8]:
    rm2distancelist.append(calculate_centre_distances(imagefolder + '\\' + imname,2))
    rm1distancelist.append(calculate_centre_distances(imagefolder + '\\' + imname,1))
    print(imname,rm2distancelist[-1],rm1distancelist[-1])


plt.plot(rm2distancelist)

plt.plot(rm1distancelist)
plt.show()

