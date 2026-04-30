import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd

'''filename = "I:\Apr16\Test1\TestCombineddata.csv" # mixed
firststeady = 300'''

filename = "I:\Apr01\Test3\TestCombineddata.csv" # elliptical
firststeady = 70

filename = "I:\Mar31\Test1\TestCombineddata.csv" #Circular
firststeady = 250
plottitle = r"Mar31/Test 1: Circular particles, $t_{ref} = 250s$"



'''filename = "I:\Mar27\Test1\TestCombineddata.csv" #Circular Dense
firststeady = 320'''

def smooth_data(data, window_size):
    return np.array(pandas.Series(data).rolling(window=window_size, min_periods=1).mean())




datafile = pd.read_csv(filename)

fig, (ax1,ax2,ax3,ax4) = plt.subplots(4, 1, figsize=(10, 8))



h12 = smooth_data(datafile["PPT1 adjusted"] - datafile["PPT2 adjusted"],250) *1000 / (1000*9.806 * .1)
h23 = smooth_data(datafile["PPT2 adjusted"] - datafile["PPT3 adjusted"],250) *1000 / (1000*9.806 * .1)
h13 = smooth_data(datafile["PPT1 adjusted"] - datafile["PPT3 adjusted"],250)*1000/  (1000*9.806 * .2)

hydraulicgradientcrit12 = (2.5-1) / (1  + datafile["VoidRatio12"])
hydraulicgradientcrit23 = (2.5-1) / (1  + datafile["VoidRatio23"])
hydraulicgradientcrit13 = (2.5-1) / (1  + datafile["VoidRatio13"])

hydraulicgradientcritadjusted12 = hydraulicgradientcrit12 + np.maximum(hydraulicgradientcrit23 - h23,0)


k_meas12 = datafile["flowrate"] / h12 * 1000
k_meas23 = datafile["flowrate"] / h23 * 1000
k_meas13 = datafile["flowrate"] / h13 * 1000


ax1.plot(datafile["time"],datafile["flowrate"])
ax1.grid()
ax1.set_xlabel("Time (s)")
ax1.set_ylabel(r'Flow rate ($m^3s^{-1}$)')
ax1.set_xlim(0,max(datafile["time"]))

ax2.plot(datafile["time"],h12,label = "PPT1 - PPT2")
ax2.plot(datafile["time"],h23,label = "PPT2 - PPT3")
ax2.plot(datafile["time"],h13,label = "PPT1 - PPT3")

'''ax2.plot(datafile["time"],hydraulicgradientcrit12, color="tab:blue", linestyle='--')
ax2.plot(datafile["time"],hydraulicgradientcrit23, color="tab:orange", linestyle='--')
ax2.plot(datafile["time"],hydraulicgradientcrit13, color="tab:green", linestyle='--')
ax2.plot(datafile["time"],hydraulicgradientcritadjusted12,color = "red")'''


ax2.grid()
ax2.legend()
ax2.set_xlabel("Time (s)")
ax2.set_ylabel(r'Hydrualic gradient')
ax2.set_xlim(0,max(datafile["time"]))


# Set upper y-limit to the max of the middle half (25th-75th percentile) of all 3 y-series
combined_k = np.concatenate([
    np.asarray(k_meas12, dtype=float),
    np.asarray(k_meas23, dtype=float),
    np.asarray(k_meas13, dtype=float)
])
ax3.set_ylim(top=np.nanpercentile(combined_k, 98)*1.5)

ax3.plot(datafile["time"],k_meas12,label = "PPT1 - PPT2")
ax3.plot(datafile["time"],k_meas23,label = "PPT2 - PPT3")
ax3.plot(datafile["time"],k_meas13,label = "PPT1 - PPT3")
ax3.grid()
ax3.legend()
ax3.set_xlabel("Time (s)")
ax3.set_ylabel('Permeability \n ($ms^{-1}$)')
ax3.set_xlim(0,max(datafile["time"]))


ax4.plot(datafile["time"],k_meas12 / np.mean(k_meas12[firststeady*100:firststeady*100+1000]),label = "PPT1 - PPT2")
ax4.plot(datafile["time"],k_meas23 / np.mean(k_meas23[firststeady*100:firststeady*100+1000]),label = "PPT2 - PPT3")
ax4.plot(datafile["time"],k_meas13 / np.mean(k_meas13[firststeady*100:firststeady*100+1000]),label = "PPT1 - PPT3")
ax4.grid()
ax4.legend()
ax4.set_xlabel("Time (s)")
ax4.set_ylabel("Relative\nPermeability ($\\frac{k}{k_{ref}}$)")
ax4.set_ylim(0,np.nanpercentile(combined_k, 95)*1.5 / min(np.mean(k_meas12[firststeady*100:firststeady*100+1000]),np.mean(k_meas23[firststeady*100:firststeady*100+1000]),np.mean(k_meas13[firststeady*100:firststeady*100+1000])))
ax4.set_xlim(0,max(datafile["time"]))
for ax in (ax1, ax2, ax3, ax4):
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend(loc="upper left")
       
for a in (ax1, ax2, ax3, ax4):
            a.xaxis.label.set_size(12)
            a.yaxis.label.set_size(12)
            a.tick_params(axis="both", labelsize=12)
            a.xaxis.labelpad = 10
            ax.figure.subplots_adjust(hspace=0.65)
plt.suptitle(plottitle)

plt.show()
