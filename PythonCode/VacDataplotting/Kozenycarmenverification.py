
import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd
from newdataplotting import *

k_calc12 = (datafile["VoidRatio12"] / (1 + datafile["VoidRatio12"]))**3 / (datafile["Tortuosity12"] **2)
k_calc23 = (datafile["VoidRatio23"] / (1 + datafile["VoidRatio23"]))**3 / (datafile["Tortuosity23"] **2)
k_calc13 = (datafile["VoidRatio13"] / (1 + datafile["VoidRatio13"]))**3 / (datafile["Tortuosity13"] **2)

plotindexes = [33000,150000]
k_calc12_0 = np.mean(k_calc12[plotindexes[0]:plotindexes[0]+ 1000])
k_calc23_0 = np.mean(k_calc23[plotindexes[0]:plotindexes[0]+ 1000])
k_calc13_0 = np.mean(k_calc13[plotindexes[0]:plotindexes[0]+ 1000])

k_meas12_0 = np.mean(k_meas12[plotindexes[0]:plotindexes[0]+ 1000])
k_meas23_0 = np.mean(k_meas23[plotindexes[0]:plotindexes[0]+ 1000])
k_meas13_0 = np.mean(k_meas13[plotindexes[0]:plotindexes[0]+ 1000])

print(k_calc12_0,k_meas12_0)


plt.scatter(smooth_data(k_calc12[plotindexes[0]:plotindexes[1]] / k_calc12_0,100)[::100], smooth_data(k_meas12[plotindexes[0]:plotindexes[1]] / k_meas12_0,100)[::100], label = "PPT1 - PPT2",s=10)
plt.scatter(smooth_data(k_calc23[plotindexes[0]:plotindexes[1]] / k_calc23_0,100)[::100], smooth_data(k_meas23[plotindexes[0]:plotindexes[1]] / k_meas23_0,100)[::100], label = "PPT2 - PPT3",s=10)
plt.scatter(smooth_data(k_calc13[plotindexes[0]:plotindexes[1]] / k_calc13_0,100)[::100], smooth_data(k_meas13[plotindexes[0]:plotindexes[1]] / k_meas13_0,100)[::100], label = "PPT1 - PPT3",s=10)
plt.xlim(0.8,3.5)
plt.ylim(0.8,3.5)
plt.gcf().set_size_inches(6, 6)
plt.gca().set_aspect('equal', adjustable='box')
plt.grid()
plt.legend()
plt.plot([0,5],[0,5],linestyle = '--', color = 'red')
plt.xlabel(r'Permeability calculated using Kozeny-Carman equation $\frac{k_{Carmen}}{k_{Carmen,ref}}$',fontsize = 'large')
plt.ylabel(r'Measured Permeability $\frac{k}{k_ref}$',fontsize = 'large')

plt.title("Mar27/Test1 Dense packed circular particles t = 350 - t= 900")


plt.show()