import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd

#filename = "I:\Apr16\Test1\TestCombineddata.csv"
filename = "I:\Apr01\Test3\TestCombineddata.csv"


def smooth_data(data, window_size):
    return np.array(pandas.Series(data).rolling(window=window_size, min_periods=1).mean())



datafile = pd.read_csv(filename)

fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(3, 2, figsize=(10, 8))

ax1.plot(datafile['time'],datafile["PPT1 adjusted"])
ax1.plot(datafile['time'],datafile["PPT2 adjusted"])
ax1.plot(datafile['time'],datafile["PPT3 adjusted"])
ax1.set_xlabel("Time (s)")
ax1.set_ylabel(r'Pressure (kPa)')
ax1.grid()
ax1.legend()

h12 = smooth_data(datafile["PPT1 adjusted"] - datafile["PPT2 adjusted"],250) *1000 / (1000*9.806 * .1)
h23 = smooth_data(datafile["PPT2 adjusted"] - datafile["PPT3 adjusted"],250) *1000 / (1000*9.806 * .1)
h13 = smooth_data(datafile["PPT1 adjusted"] - datafile["PPT3 adjusted"],250)*1000/  (1000*9.806 * .2)

hcrit12 = (2.5-0.9806) / (1 + np.mean(datafile["VoidRatio12"][0:1000]))
hcrit23 = (2.5-0.9806)  / (1 + np.mean(datafile["VoidRatio23"][0:1000]))
hcrit13 = (2.5-0.9806) / (1 + np.mean(datafile["VoidRatio13"][0:1000]))

k_meas12 = datafile["flowrate"] / h12 * 1000
k_meas23 = datafile["flowrate"] / h23 * 1000
k_meas13 = datafile["flowrate"] / h13 * 1000


ax2.plot(datafile["time"],datafile["flowrate"])
ax2.grid()
ax2.set_xlabel("Time (s)")
ax2.set_ylabel(r'Flow rate ($m^3s^{-1}$)')


ax3.plot(datafile["time"],h12,label = "PPT1 - PPT2")
ax3.plot(datafile["time"],h23,label = "PPT2 - PPT3")
ax3.plot(datafile["time"],h13,label = "PPT1 - PPT3")

ax3.axhline(y=hcrit12, color="tab:blue", linestyle='--')
ax3.axhline(y=hcrit23, color="tab:orange", linestyle='--')
ax3.axhline(y=hcrit13, color="tab:green", linestyle='--')

ax3.grid()
ax3.legend()
ax3.set_xlabel("Time (s)")
ax3.set_ylabel(r'Hydrualic gradient (m)')

# Set upper y-limit to the max of the middle half (25th-75th percentile) of all 3 y-series
combined_k = np.concatenate([
    np.asarray(k_meas12, dtype=float),
    np.asarray(k_meas23, dtype=float),
    np.asarray(k_meas13, dtype=float)
])
ax4.set_ylim(top=np.nanpercentile(combined_k, 95)*1.5)

ax4.plot(datafile["time"],k_meas12,label = "PPT1 - PPT2")
ax4.plot(datafile["time"],k_meas23,label = "PPT2 - PPT3")
ax4.plot(datafile["time"],k_meas13,label = "PPT1 - PPT3")
ax4.grid()
ax4.legend()
ax4.set_xlabel("Time (s)")
ax4.set_ylabel(r'Permeability ($ms^{-1}$)')


ax5.plot(datafile["time"],datafile["VoidRatio12"],label = "PPT1 - PPT2")
ax5.plot(datafile["time"],datafile["VoidRatio23"],label = "PPT2 - PPT3")
ax5.plot(datafile["time"],datafile["VoidRatio13"],label = "PPT1 - PPT3")
ax5.grid()
ax5.legend()
ax5.set_xlabel("Time (s)")
ax5.set_ylabel(r'Void Ratio')


ax6.plot(datafile["time"],datafile["Tortuosity12"],label = "PPT1 - PPT2")
ax6.plot(datafile["time"],datafile["Tortuosity23"],label = "PPT2 - PPT3")
ax6.plot(datafile["time"],datafile["Tortuosity13"],label = "PPT1 - PPT3")
ax6.grid()
ax6.legend()
ax6.set_xlabel("Time (s)")
ax6.set_ylabel(r'Tortuosity')

plt.show()


