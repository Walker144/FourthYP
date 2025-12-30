import pandas
import numpy as np
import matplotlib.pyplot as plt


data1 = pandas.read_excel('OneDrive_1_22-10-2025\matlabcode\pptcalibration2dataexport.xlsx')
data2 = pandas.read_excel('OneDrive_1_22-10-2025\matlabcode\pptcalibration2actuallydataexport.xlsx')
data3 = pandas.read_excel('OneDrive_1_22-10-2025\matlabcode\pptcalibration4dataexport.xlsx')

times1 = data1['timestamps']
times2 = data2['timestamps']
times3 = data3['timestamps']



PPT1 = data1['Var3']
PPT2 = data2['Var2']
PPT3 = data3['Var4']

PPT1 = PPT1.tolist()
PPT2 = PPT2.tolist()
PPT3 = PPT3.tolist()

def smooth_data(data, window_size):
    return pandas.Series(data).rolling(window=window_size, min_periods=1).mean().tolist()

import plottingfunctions
fs = int(1 / (times1[100] - times1[99]))
cutoff = 1  # cutoff frequency in Hz

PPT1 = plottingfunctions.butterfilter(PPT1,fs,cutoff)
PPT2 = plottingfunctions.butterfilter(PPT2,fs,cutoff)
PPT3 = plottingfunctions.butterfilter(PPT3,fs,cutoff)
stabletime1 = [[14,22],[24,30],[34,40],[43,48],[51,57],[60,68],[70,78],[80,91],[99,102],[110,113],[122,129],[136,140],[142,150],[157,160],[162,167]]
stabletime2 = [[0,4],[6,13],[15,22],[24,32],[35,42],[44,52],[55,70],[72,82],[86,91],[96,102],[104,109],[114,118],[124,127],[133,140],[145,146]]
stabletime3 = [[0,7],[11,36],[38,58],[60,67],[68,76],[78,90],[94,99],[103,115],[129,135],[142,148],[155,160],[167,170],[180,185],[192,197],[200,204]]

#set which stable times, timestamps, and PPT data to use 
stabletime = stabletime3
times = times3
PPT = PPT3

# Create subplots side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

ax1.plot(times, PPT, label='PPT2')

vaverages = []
times = times.tolist()
for timeset in stabletime:
    startindex = times.index(timeset[0])
    endindex = times.index(timeset[1])
    vaverages.append(np.average(PPT[startindex:endindex]))
    ax1.plot(timeset, [vaverages[-1], vaverages[-1]],
             marker='p', linestyle='-', color='red',
             markerfacecolor='red', markeredgecolor='red')

ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Voltage (V)')


print(vaverages)
vaverages = np.array(vaverages)
pressures = np.array([1,2,4,6,8,10,15,20,15,10,8,6,4,2,1])

slope, intercept = np.polyfit(vaverages, pressures, 1)

x_line = np.linspace(min(vaverages), max(vaverages), 200)
y_line = slope * x_line + intercept

ax2.scatter(vaverages, pressures, color='blue', label='data points')
ax2.plot(x_line, y_line, color='red', label=f'fit: y={slope:.7f}x + {intercept:.7f}')

ax2.set_ylabel('Pore Pressure (KPa)')
ax2.set_xlabel('Voltage (V)')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
