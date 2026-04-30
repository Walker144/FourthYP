import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd
from newdataplotting import *

plottitle = "Apr16/Test1 Mixed particles"

fig, (ax1,ax2,ax3) = plt.subplots(3,1)
fig.suptitle(plottitle)

datatimes = np.array([0,1000])*100



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
ax1.set_xlim(0,max(datafile["time"]))


ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Coordination\nnumber")
ax2.grid()
ax2.legend()
ax2.set_title("PPT2 - PPT3")
ax2.set_xlim(0,max(datafile["time"]))

ax3.set_xlabel("Time (s)")
ax3.set_ylabel("Coordination\nnumber")
ax3.grid()
ax3.legend()
ax3.set_title("PPT1 - PPT3")
ax3.set_xlim(0,max(datafile["time"]))


plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()


fig,(ax1,ax2,ax3,ax4) = plt.subplots(4,1)
fig.suptitle(plottitle)
ax1.plot(datafile["time"],datafile["CoordinationNumber12"],label = "PPT1 - PPT2")
ax1.plot(datafile["time"],datafile["CoordinationNumber23"],label = "PPT2 - PPT3")
ax1.plot(datafile["time"],datafile["CoordinationNumber13"],label = "PPT1 - PPT3")

ax2.plot(datafile["time"],datafile["MechanicalCoordination12"],label = "PPT1-PPT2")
ax2.plot(datafile["time"],datafile["MechanicalCoordination23"],label = "PPT2-PPT3")
ax2.plot(datafile["time"],datafile["MechanicalCoordination13"],label = "PPT1-PPT3")


ax3.plot(datafile["time"],datafile["Tortuosity12"],label = "PPT1-PPT2")
ax3.plot(datafile["time"],datafile["Tortuosity23"],label = "PPT2-PPT3")
ax3.plot(datafile["time"],datafile["Tortuosity13"],label = "PPT1-PPT3")


ax4.plot(datafile["time"],datafile["VoidRatio12"],label = "PPT1-PPT2")
ax4.plot(datafile["time"],datafile["VoidRatio23"],label = "PPT2-PPT3")
ax4.plot(datafile["time"],datafile["VoidRatio13"],label = "PPT1-PPT3")






ax1.set_xlabel("Time (s)", fontsize="large")
ax1.set_ylabel("Average coordination\nnumber", fontsize="large")
ax1.grid()
ax1.legend(fontsize="large")
ax1.set_xlim(0, max(datafile["time"]))


ax2.set_xlabel("Time (s)", fontsize="large")
ax2.set_ylabel("Mechanical coordination\n number", fontsize="large")
ax2.grid()
ax2.legend(fontsize="large")
ax2.set_xlim(0, max(datafile["time"]))

ax3.set_xlabel("Time (s)", fontsize="large")
ax3.set_ylabel("Tortuosity", fontsize="large")
ax3.grid()
ax3.legend(fontsize="large")
ax3.set_xlim(0, max(datafile["time"]))

ax4.set_xlabel("Time (s)", fontsize="large")
ax4.set_ylabel("Void Ratio", fontsize="large")
ax4.grid()
ax4.legend(fontsize="large")
ax4.set_xlim(0, max(datafile["time"]))


fig.set_size_inches(16, 10, forward=True)
plt.subplots_adjust(left=0.06, right=0.99, bottom=0.06, top=0.95, hspace=0.2)
plt.tight_layout(rect=[0.02, 0.02, 0.995, 0.98])
plt.show()

'''
fig, (ax1,ax2) = plt.subplots(1,2)
fig.suptitle(plottitle)




ax1.scatter(datafile["CoordinationNumber12"][datatimes[0]:datatimes[1]:100] / datafile["CoordinationNumber12"][0],datafile["Tortuosity12"][datatimes[0]:datatimes[1]:100] / datafile["Tortuosity12"][0],color = 'tab:blue',label = "PPT1 - PPT2")
ax1.scatter(datafile["CoordinationNumber23"][datatimes[0]:datatimes[1]:100] / datafile["CoordinationNumber23"][0],datafile["Tortuosity23"][datatimes[0]:datatimes[1]:100] / datafile["Tortuosity23"][0],color = 'tab:orange',label = "PPT2 - PPT3")
ax1.scatter(datafile["CoordinationNumber23"][datatimes[0]:datatimes[1]:100] / datafile["CoordinationNumber13"][0],datafile["Tortuosity13"][datatimes[0]:datatimes[1]:100] / datafile["Tortuosity13"][0],color = 'tab:green',label = "PPT1 - PPT3")

ax2.scatter(datafile["MechanicalCoordination12"][datatimes[0]:datatimes[1]:100] / datafile["MechanicalCoordination12"][0],datafile["Tortuosity12"][datatimes[0]:datatimes[1]:100] / datafile["Tortuosity12"][0],color = 'tab:blue',label = "PPT1 - PPT2")
ax2.scatter(datafile["MechanicalCoordination23"][datatimes[0]:datatimes[1]:100] / datafile["MechanicalCoordination23"][0],datafile["Tortuosity23"][datatimes[0]:datatimes[1]:100] / datafile["Tortuosity23"][0],color = 'tab:orange',label = "PPT2 - PPT3")
ax2.scatter(datafile["MechanicalCoordination23"][datatimes[0]:datatimes[1]:100] / datafile["MechanicalCoordination13"][0],datafile["Tortuosity13"][datatimes[0]:datatimes[1]:100] / datafile["Tortuosity13"][0],color = 'tab:green',label = "PPT1 - PPT3")

#ax1.plot([0.85,1.05],[0.85,1.05],linestyle = '--',color = 'red')
#ax2.plot([0.85,1.05],[0.85,1.05],linestyle = '--',color = 'red')





ax1.set_xlabel(r"Coordination Number ($\frac{Z}{Z_{ref}}$)",size = 'large')
ax1.set_ylabel(r'Tortuosity ($\frac{\tau}{\tau_{ref}}$)',size = 'large')
ax2.set_xlabel(r"Mechanical Coordination Number ($\frac{Z_m}{Z_{m,ref}}$)",size = 'large')
ax2.set_ylabel(r'Tortuosity ($\frac{\tau}{\tau_{ref}}$)',size = 'large')

ax1.grid()
ax2.grid()

fig.set_size_inches(12,6)



ax1.legend()
ax2.legend()

plt.show()

'''