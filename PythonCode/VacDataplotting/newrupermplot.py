import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd
from newdataplotting import *


timerange=  [250,1250]


#if we took the current soil structure and said that there was no flow, and it did not reconsolidate
sigmav1ref = ((2.5-1) / (1 + datafile["VoidRatio12"]) + (2.5-1) / (1 + datafile["VoidRatio23"]) ) * 0.1 * 1000 * 9.806 / 1000
sigmav2ref = ((2.5-1) / (1 + datafile["VoidRatio23"]) ) * 0.1 * 1000 * 9.806 / 1000

simgav1 = sigmav1ref - datafile["PPT1 adjusted"] + datafile["PPT3 adjusted"]
simgav2 = sigmav2ref - datafile["PPT2 adjusted"] + datafile["PPT3 adjusted"]


fig,(ax1,ax2,ax3,ax4) = plt.subplots(4,1)

ru1 = 1 - simgav1 / sigmav1ref
ru2 = 1 - simgav2 / sigmav2ref


krel12 = k_meas12 / np.average(k_meas12[timerange[0]*100:timerange[0]*100+1000])
krel23 = k_meas23 / np.average(k_meas23[timerange[0]*100:timerange[0]*100+1000])


ax1.plot(datafile["time"],simgav1,label = 'PPT1')
ax1.plot(datafile["time"],simgav2,label = 'PPT1')

ax1.plot(datafile["time"],sigmav1ref,label = 'PPT1 Hydrostatic',color = 'tab:blue',linestyle = '--')
ax1.plot(datafile["time"],sigmav2ref,label = 'PPT2 Hydrostatic',color = 'tab:orange',linestyle = '--')




ax2.plot(datafile["time"],ru1,label = 'PPT1')
ax2.plot(datafile["time"],ru2,label = 'PPT2')

ax3.plot(datafile["time"],k_meas12,label = 'PPT1 - PPT2')
ax3.plot(datafile["time"],k_meas23,label = 'PPT2 - PPT3')

ax4.plot(datafile["time"],krel12,label = 'PPT1 - PPT2')
ax4.plot(datafile["time"],krel23,label = 'PPT2 - PPT3')




ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Vertical Effective Stress (Kpa)")
ax1.grid()
ax1.legend()

ax2.set_ylabel("$R_u$")
ax2.set_xlabel("Time (s)")
ax2.grid()
ax2.legend()



combined_k = np.concatenate([
    np.asarray(k_meas12, dtype=float),
    np.asarray(k_meas23, dtype=float),
    np.asarray(k_meas13, dtype=float)
])
ax3.set_ylim(0,np.nanpercentile(combined_k, 95)*1.5)


ax3.set_ylabel("Permeability ($ms^{-1}$)")
ax3.set_xlabel("Time (s)")
ax3.grid()
ax3.legend()

ax4.set_ylabel("Relative Permeability ")
ax4.set_xlabel("Time (s)")
ax4.grid()
ax4.legend()
ax4.set_ylim(0,np.nanpercentile(combined_k, 95) / float(np.average(k_meas23[timerange[0]*100:timerange[0]*100+1000])))

plt.show()


plt.scatter(ru1[timerange[0]*100:timerange[1]*100:100],krel12[timerange[0]*100:timerange[1]*100:100],label="$R_u$ at PPT1, Permeability for PPT1 - PPT2")
plt.scatter(ru2[timerange[0]*100:timerange[1]*100:100],krel23[timerange[0]*100:timerange[1]*100:100],label="$R_u$ at PPT2, Permeability for PPT2 - PPT3")
plt.xlabel("$R_u$")
plt.ylabel("Relative Permeability")

plt.grid()
plt.legend()
plt.show()