import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd
from newdataplotting import *


fig, (ax2) = plt.subplots(1,1)
fig.suptitle("Mar27 Test 1: Dense packed circular particles")


'''ax1.scatter(datafile["VoidRatio12"][::100] / datafile["VoidRatio12"][0000],datafile["Tortuosity12"][::100] / datafile["Tortuosity12"][0000],color = 'tab:blue',label = "PPT1 - PPT2")
ax1.scatter(datafile["VoidRatio23"][::100] / datafile["VoidRatio23"][0000],datafile["Tortuosity23"][::100] / datafile["Tortuosity23"][0000],color = 'tab:orange',label = "PPT2 - PPT3")
ax1.scatter(datafile["VoidRatio23"][::100] / datafile["VoidRatio13"][0000],datafile["Tortuosity13"][::100] / datafile["Tortuosity13"][0000],color = 'tab:green',label = "PPT1 - PPT3")
'''

datatimes = np.array([0,1460])*100

por12 = datafile["VoidRatio12"] / (1 + datafile["VoidRatio12"])
por23 = datafile["VoidRatio23"] / (1 + datafile["VoidRatio23"])
por13 = datafile["VoidRatio13"] / (1 + datafile["VoidRatio13"])



ax2.scatter(por12[datatimes[0]:datatimes[1]:100] / por12[0000],datafile["Tortuosity12"][datatimes[0]:datatimes[1]:100] / datafile["Tortuosity12"][0000],color = 'tab:blue',label = "PPT1 - PPT2")
ax2.scatter(por12[datatimes[0]:datatimes[1]:100] / por12[0000],datafile["Tortuosity23"][datatimes[0]:datatimes[1]:100] / datafile["Tortuosity23"][0000],color = 'tab:orange',label = "PPT2 - PPT3")
ax2.scatter(por12[datatimes[0]:datatimes[1]:100] / por12[0000],datafile["Tortuosity13"][datatimes[0]:datatimes[1]:100] / datafile["Tortuosity13"][0000],color = 'tab:green',label = "PPT1 - PPT3")


'''ax1.set_xlabel(r"Void ratio ($\frac{e}{e_0}$)")
ax1.set_ylabel(r"Tortuosity ($\frac{\tau}{\tau_0}$)")'''
ax2.set_xlabel(r"Porosity ($\frac{\phi}{\phi_{ref}}$)",size = 'large')
ax2.set_ylabel(r"Tortuosity ($\frac{\tau}{\tau_{ref}}$)",size = 'large')

#ax1.grid()
ax2.grid()
#ax1.legend()
ax2.legend()
#ax1.set_box_aspect(1)
ax2.set_box_aspect(1)
fig.set_size_inches(8, 8)
plt.tight_layout()
plt.show()





'''fig, (ax2) = plt.subplots(1,1)
fig.suptitle("Mar27 Test 1: Dense packed circular particles")

ax2.scatter(por12[::100],datafile["Tortuosity12"][::100] ,color = 'tab:blue',label = "PPT1 - PPT2")
ax2.scatter(por12[::100] ,datafile["Tortuosity23"][::100],color = 'tab:orange',label = "PPT2 - PPT3")
ax2.scatter(por12[::100] ,datafile["Tortuosity13"][::100],color = 'tab:green',label = "PPT1 - PPT3")

porvalues = np.linspace(min(min(por12[::100]),min(por23[::100]),min(por13[::100])),max(max(por12[::100]),max(por23[::100]),max(por13[::100])),100)

tortline = .83 * porvalues ** -.65

ax2.plot(porvalues,tortline,linestyle = '--',color = 'red', label = 'Monte Carlo Model')



ax2.set_xlabel(r"Porosity ($\phi$)",size = 'large')
ax2.set_ylabel(r"Tortuosity ($\tau$)",size = 'large')

#ax1.grid()
ax2.grid()
#ax1.legend()
ax2.legend()
#ax1.set_box_aspect(1)
ax2.set_box_aspect(1)
plt.show()
'''