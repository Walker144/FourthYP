import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd
from newdataplotting import *


fig, (ax1,ax2,ax3) = plt.subplots(3,1)
fig.suptitle("Apr16 Test 1")

ax1.plot(datafile["time"],datafile["CoordinationNumber12"],label = "Coordination number")
ax2.plot(datafile["time"],datafile["CoordinationNumber23"],label = "Coordination number")
ax3.plot(datafile["time"],datafile["CoordinationNumber13"],label = "Coordination number")

ax1.plot(datafile["time"],datafile["MechanicalCoordination12"],label = "Mechanical coordination number")
ax2.plot(datafile["time"],datafile["MechanicalCoordination23"],label = "Mechanical coordination number")
ax3.plot(datafile["time"],datafile["MechanicalCoordination13"],label = "Mechanical coordination number")

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Coordination\nnumber")
ax1.grid()
ax1.legend()
ax1.set_title("PPT1 - PPT2")


ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Coordination\nnumber")
ax2.grid()
ax2.legend()
ax2.set_title("PPT2 - PPT3")

ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Coordination\nnumber")
ax3.grid()
ax3.legend()
ax3.set_title("PPT1 - PPT3")

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

fig, (ax1,ax2) = plt.subplots(1,2)
fig.suptitle("Apr01 Test 3: Elliptical particles")

ax1.scatter(datafile["CoordinationNumber12"][::100] / datafile["CoordinationNumber12"][10000],datafile["Tortuosity12"][::100] / datafile["Tortuosity12"][10000],color = 'tab:blue',label = "PPT1 - PPT2")
ax1.scatter(datafile["CoordinationNumber23"][::100] / datafile["CoordinationNumber23"][10000],datafile["Tortuosity23"][::100] / datafile["Tortuosity23"][10000],color = 'tab:orange',label = "PPT2 - PPT3")
ax1.scatter(datafile["CoordinationNumber23"][::100] / datafile["CoordinationNumber13"][10000],datafile["Tortuosity13"][::100] / datafile["Tortuosity13"][10000],color = 'tab:green',label = "PPT1 - PPT3")

ax2.scatter(datafile["MechanicalCoordination12"][::100] / datafile["MechanicalCoordination12"][10000],datafile["Tortuosity12"][::100] / datafile["Tortuosity12"][10000],color = 'tab:blue',label = "PPT1 - PPT2")
ax2.scatter(datafile["MechanicalCoordination23"][::100] / datafile["MechanicalCoordination23"][10000],datafile["Tortuosity23"][::100] / datafile["Tortuosity23"][10000],color = 'tab:orange',label = "PPT2 - PPT3")
ax2.scatter(datafile["MechanicalCoordination23"][::100] / datafile["MechanicalCoordination13"][10000],datafile["Tortuosity13"][::100] / datafile["Tortuosity13"][10000],color = 'tab:green',label = "PPT1 - PPT3")

ax1.plot([0.85,1.05],[0.85,1.05],linestyle = '--',color = 'red')
ax2.plot([0.85,1.05],[0.85,1.05],linestyle = '--',color = 'red')





ax1.set_xlabel(r"Coordination Number ($\frac{Z}{Z_0}$)",size = 'large')
ax1.set_ylabel(r'Tortuosity ($\frac{\tau}{\tau_0}$)',size = 'large')
ax2.set_xlabel(r"Mechanical Coordination Number ($\frac{Z_m}{Z_{m,0}}$)",size = 'large')
ax2.set_ylabel(r'Tortuosity ($\frac{\tau}{\tau_0}$)',size = 'large')

ax1.set_box_aspect(1)
ax2.set_box_aspect(1)



ax1.grid()
ax2.grid()
ax1.legend()
ax2.legend()

plt.show()

