import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd
from newdataplotting import *

timerange=  [250,800]


hydraulicgradientcrit12 = (2.5-1) / (1  + datafile["VoidRatio12"])
hydraulicgradientcrit23 = (2.5-1) / (1  + datafile["VoidRatio23"])
hydraulicgradientcrit13 = (2.5-1) / (1  + datafile["VoidRatio13"])

hydraulicgradientcrit12new = hydraulicgradientcrit12 + np.maximum(hydraulicgradientcrit23-h23, 0)

fig, (ax1,ax2,ax3,ax4) = plt.subplots(4,1)

ax1.plot(datafile["time"][timerange[0]*100:timerange[1]*100], h12[timerange[0]*100:timerange[1]*100],label = r"PPT1 - PPT2 $i_{meas}$")
ax1.plot(datafile["time"][timerange[0]*100:timerange[1]*100], h23[timerange[0]*100:timerange[1]*100],label = r"PPT2 - PPT3 $i_{meas}$")
ax1.plot(datafile["time"][timerange[0]*100:timerange[1]*100], h13[timerange[0]*100:timerange[1]*100],label = r"PPT1 - PPT3 $i_{meas}$")

ax1.plot(datafile["time"][timerange[0]*100:timerange[1]*100],hydraulicgradientcrit12new[timerange[0]*100:timerange[1]*100],label = r"PPT1 - PPT2 $i_{crit}$",color = "tab:blue", linestyle = "--")
ax1.plot(datafile["time"][timerange[0]*100:timerange[1]*100],hydraulicgradientcrit23[timerange[0]*100:timerange[1]*100],label = r"PPT2 - PPT3 $i_{crit}$",color = "tab:orange", linestyle = "--")
ax1.plot(datafile["time"][timerange[0]*100:timerange[1]*100],hydraulicgradientcrit13[timerange[0]*100:timerange[1]*100],label = r"PPT1 - PPT3 $i_{crit}$",color = "tab:green", linestyle = "--")

ax1.set_xlim(timerange[0],timerange[1])
ax1.set_xlabel("Time (s)")

ax1.set_ylabel("Hydraulic Gradient")
ax1.grid()
ax1.legend()

ax2.plot(datafile["time"][timerange[0]*100:timerange[1]*100],k_meas12[timerange[0]*100:timerange[1]*100], label = r'PPT1 - PPT2')
ax2.plot(datafile["time"][timerange[0]*100:timerange[1]*100],k_meas23[timerange[0]*100:timerange[1]*100], label = r'PPT2 - PPT3')
ax2.plot(datafile["time"][timerange[0]*100:timerange[1]*100],k_meas13[timerange[0]*100:timerange[1]*100], label = r'PPT1 - PPT3')

combined_k = np.concatenate([
    np.asarray(k_meas12, dtype=float),
    np.asarray(k_meas23, dtype=float),
    np.asarray(k_meas13, dtype=float)
])
ax2.set_ylim(0,np.nanpercentile(combined_k, 95)*1.5)
ax2.set_xlim(timerange[0],timerange[1])
ax2.grid()
ax2.set_xlabel("Time (s)")
ax2.set_ylabel("permeability ")

ax3.plot(datafile["time"][timerange[0]*100:timerange[1]*100:100],k_meas12[timerange[0]*100:timerange[1]*100:100] / np.mean(k_meas12[timerange[0]*100:timerange[0]*100 + 1000]))
ax3.plot(datafile["time"][timerange[0]*100:timerange[1]*100:100],k_meas23[timerange[0]*100:timerange[1]*100:100] / np.mean(k_meas23[timerange[0]*100:timerange[0]*100 + 1000]))
ax3.plot(datafile["time"][timerange[0]*100:timerange[1]*100:100],k_meas13[timerange[0]*100:timerange[1]*100:100] / np.mean(k_meas13[timerange[0]*100:timerange[0]*100 + 1000]))

ax3.set_xlim(timerange[0],timerange[1])
ax3.grid()
ax3.set_xlabel("Time (s)")
ax3.set_ylabel(r"$\frac{k}{k_{ref}}$ ")


ru12 = h12 / hydraulicgradientcrit12
ru23 = h23 / hydraulicgradientcrit23
ru13 = h13 / hydraulicgradientcrit13

ax4.plot(datafile["time"][timerange[0]*100:timerange[1]*100:100],ru12[timerange[0]*100:timerange[1]*100:100])
ax4.plot(datafile["time"][timerange[0]*100:timerange[1]*100:100],ru23[timerange[0]*100:timerange[1]*100:100])
ax4.plot(datafile["time"][timerange[0]*100:timerange[1]*100:100],ru13[timerange[0]*100:timerange[1]*100:100])

ax4.set_xlim(timerange[0],timerange[1])
ax4.grid()
ax4.set_xlabel("Time (s)")
ax4.set_ylabel(r"$R_u$  $\frac{i_{meas}}{i_{crit}}$ ")


plt.show()

print(np.mean(k_meas12[timerange[0]*100:timerange[0]*100 + 1000]))
plt.scatter(ru12[timerange[0]*100:timerange[1]*100:100],k_meas12[timerange[0]*100:timerange[1]*100:100] / np.mean(k_meas12[timerange[0]*100:timerange[0]*100 + 1000]),label  = "PPT1 - PPT2")
plt.scatter(ru23[timerange[0]*100:timerange[1]*100:100],k_meas23[timerange[0]*100:timerange[1]*100:100] / np.mean(k_meas23[timerange[0]*100:timerange[0]*100 + 1000]),label  = "PPT2 - PPT3")
plt.scatter(ru13[timerange[0]*100:timerange[1]*100:100],k_meas13[timerange[0]*100:timerange[1]*100:100] / np.mean(k_meas13[timerange[0]*100:timerange[0]*100 + 1000]),label  = "PPT1 - PPT3")

plt.xlabel(r"$R_u$  ( $\frac{h}{h_{crit}}$)",size = "large")
plt.ylabel(r'$\frac{k}{k_{ref}}$',size = "large")
plt.grid()
plt.gcf().set_size_inches(6, 6)

plt.legend()
plt.show()
