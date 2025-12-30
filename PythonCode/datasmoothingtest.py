import pandas
import numpy as np
import plottingfunctions


def smooth_data(data, window_size):
    return pandas.Series(data).rolling(window=window_size, min_periods=1).mean().tolist()

data = pandas.read_excel('OneDrive_1_22-10-2025\matlabcode\week7test1dataexport.xlsx')

times = data['timestamps']
PPT1 = data['Var4']
PPT2 = data['Var3']
PPT3 = data['Var5']

PPT1 = (PPT1 -0.0069594)/0.0016471
PPT2 = (PPT2 - 0.0081294) / 0.0016308
PPT3 = (PPT3 - 0.0053957) / 0.0016309

PPT1smoothed = smooth_data(PPT1, 100)
PPT2smoothed = smooth_data(PPT2, 100)
PPT3smoothed = smooth_data(PPT3, 100)

fs = int(1 / (times[100] - times[99]))
cutoff = 1  # cutoff frequency in Hz

PPT1butterworth = plottingfunctions.butterfilter(PPT1, fs, cutoff)
PPT2butterworth = plottingfunctions.butterfilter(PPT2, fs, cutoff)
PPT3butterworth = plottingfunctions.butterfilter(PPT3, fs, cutoff)



import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 11

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# Raw data plot
ax1.plot(times, PPT1, label="PPT1")
ax1.plot(times, PPT2, label="PPT2")
ax1.plot(times, PPT3, label="PPT3")
ax1.set_xlabel('Time (s)', fontsize=16)
ax1.set_ylabel('Pressure (kPa)', fontsize=16)
ax1.set_title('Data before processing', fontsize=18)
ax1.set_xlim(left=0)
ax1.legend()


# Butterworth filtered data plot
ax2.plot(times, PPT1butterworth, label=f'PPT1')
ax2.plot(times, PPT2butterworth, label=f'PPT2')
ax2.plot(times, PPT3butterworth, label=f'PPT3')
ax2.set_xlabel('Time (s)', fontsize=16)
ax2.set_ylabel('Pressure (kPa)', fontsize=16)
ax2.set_title('Data after filtering', fontsize=18)
ax2.set_xlim(left=0)
ax2.legend()


plt.tight_layout()
plt.show()
