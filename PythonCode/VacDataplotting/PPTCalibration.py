
import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd
import os

calibrationfile = r"C:\Users\andre\Documents\GitHub\FourthYP\OneDrive_1_22-10-2025\matlabcode\pptcalibration4.mat"
Pressures = [1,2,4,6,8,10,15,20,15,10,8,6,4,2,1]
steadytimes = [[0,9.5],[11,35.8],[37.4,58],[60,67],[68,76],[77.4,92.2],[93.3,100.5],[102,122.2],[125,135],[142,148],[154.4,160],[166.4,172],[180,185],[193,198],[200,204]]
PPTindex = 2



def smooth_data(data, window_size):
    return pandas.Series(data).rolling(window=window_size, min_periods=1).mean().tolist()



matdata = h5py.File(calibrationfile)
print(matdata.keys())

PPTdata = np.array(matdata["data"][PPTindex])
PPTtimes = np.array(matdata["timestamps"][0])

fs = int(1/(PPTtimes[100] - PPTtimes[99]))


PPTdatabutterworth = plottingfunctions.butterfilter(PPTdata,fs,2)


plt.plot(PPTtimes,PPTdatabutterworth,color = "tab:blue",label= "PPT data")
plt.grid()
plt.legend()
plt.ylabel("Voltage (V)")
plt.xlabel("Times (s)")

steadyvoltages = []

for timeset in steadytimes:
    steadyvoltages.append(np.mean(PPTdatabutterworth[int(timeset[0] * fs) : int(timeset[1] * fs)]))
    plt.plot(timeset,[np.mean(PPTdatabutterworth[int(timeset[0] * fs) : int(timeset[1] * fs)]),np.mean(PPTdatabutterworth[int(timeset[0] * fs) :int( timeset[1] * fs)])],color = 'tab:red',linestyle = '--',marker = 'o')


plt.title("Time-Voltage graph")

plt.show()


m,b = np.polyfit(steadyvoltages,Pressures,1)

print(m,b)


plt.plot(steadyvoltages,Pressures,linestyle = '',marker = 'o',label = 'Datapoints')

plt.plot([min(steadyvoltages),max(steadyvoltages)],[b + m * min(steadyvoltages),b+m * max(steadyvoltages)],linestyle = '--', marker = '',color = "tab:red",label = f'Regression line: P = {round(m,2)} $\cdot$ V + {round(b,3)}')
plt.title("Pressure - Voltage graph")

plt.ylabel("Pressure (Kpa)")
plt.xlabel("Voltage (V)")
plt.grid()
plt.legend()



plt.show()
