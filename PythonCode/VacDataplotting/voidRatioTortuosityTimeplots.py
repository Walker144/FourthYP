import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd

#filename = "I:\Apr16\Test1\TestCombineddata.csv" # mixed
#filename = "I:\Apr01\Test3\TestCombineddata.csv" # elliptical
#filename = "I:\Mar27\Test3\TestCombineddata.csv" #Circular
filename = "I:\Mar27\Test1\TestCombineddata.csv" #Circular Dense

#filename = "I:\Mar31\Test1\TestCombineddata.csv" #Circular New


def smooth_data(data, window_size):
    return np.array(pandas.Series(data).rolling(window=window_size, min_periods=1).mean())



datafile = pd.read_csv(filename)

fig, (ax1,ax2,ax3) = plt.subplots(3,1)

ax1.plot(datafile["time"],datafile["VoidRatio12"],label = "PPT1 - PPT2")
ax1.plot(datafile["time"],datafile["VoidRatio23"],label = "PPT2 - PPT3")
ax1.plot(datafile["time"],datafile["VoidRatio13"],label = "PPT1 - PPT3")


ax2.plot(datafile["time"],datafile["VoidRatio12"]/ (1 + datafile["VoidRatio12"]),label = "PPT1 - PPT2")
ax2.plot(datafile["time"],datafile["VoidRatio23"]/ (1 + datafile["VoidRatio23"]),label = "PPT2 - PPT3")
ax2.plot(datafile["time"],datafile["VoidRatio13"]/ (1 + datafile["VoidRatio13"]),label = "PPT1 - PPT3")


ax3.plot(datafile["time"],datafile["Tortuosity12"],label = "PPT1 - PPT2")
ax3.plot(datafile["time"],datafile["Tortuosity23"],label = "PPT2 - PPT3")
ax3.plot(datafile["time"],datafile["Tortuosity13"],label = "PPT1 - PPT3")

ax1.set_xlim(0,max(datafile["time"]))
ax1.set_xlabel("Times (s)",size = "large")
ax1.set_ylabel("Void ratio",size = "large")
ax1.grid()
ax1.legend()

plt.subplots_adjust(hspace=0.3)

plt.show()



