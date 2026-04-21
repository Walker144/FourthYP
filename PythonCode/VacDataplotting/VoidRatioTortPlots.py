import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd
from newdataplotting import *


fig, (ax1,ax2) = plt.subplots(1,2)
fig.suptitle("Apr01 Test 3: Elliptical particles")


ax1.scatter(datafile["VoidRatio12"][::100] / datafile["VoidRatio12"][30000],datafile["Tortuosity12"][::100] / datafile["Tortuosity12"][30000],color = 'tab:blue',label = "PPT1 - PPT2")
ax1.scatter(datafile["VoidRatio23"][::100] / datafile["VoidRatio23"][30000],datafile["Tortuosity23"][::100] / datafile["Tortuosity23"][30000],color = 'tab:orange',label = "PPT2 - PPT3")
ax1.scatter(datafile["VoidRatio23"][::100] / datafile["VoidRatio13"][30000],datafile["Tortuosity13"][::100] / datafile["Tortuosity13"][30000],color = 'tab:green',label = "PPT1 - PPT3")

por12 = datafile["VoidRatio12"] / (1 + datafile["VoidRatio12"])
por23 = datafile["VoidRatio23"] / (1 + datafile["VoidRatio23"])
por13 = datafile["VoidRatio13"] / (1 + datafile["VoidRatio13"])



ax2.scatter(por12[::100] / por12[30000],datafile["Tortuosity12"][::100] / datafile["Tortuosity12"][30000],color = 'tab:blue',label = "PPT1 - PPT2")
ax2.scatter(por12[::100] / por12[30000],datafile["Tortuosity23"][::100] / datafile["Tortuosity23"][30000],color = 'tab:orange',label = "PPT2 - PPT3")
ax2.scatter(por12[::100] / por12[30000],datafile["Tortuosity13"][::100] / datafile["Tortuosity13"][30000],color = 'tab:green',label = "PPT1 - PPT3")


ax1.set_xlabel(r"Void ratio ($\frac{e}{e_0}$)")
ax1.set_ylabel(r"Tortuosity ($\frac{\tau}{\tau_0}$)")
ax2.set_xlabel(r"Porosity ($\frac{\phi}{\phi_0}$)")
ax2.set_ylabel(r"Tortuosity ($\frac{\tau}{\tau_0}$)")

ax1.grid()
ax2.grid()
ax1.legend()
ax2.legend()
ax1.set_box_aspect(1)
ax2.set_box_aspect(1)
plt.show()
