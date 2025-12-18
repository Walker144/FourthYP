
import pandas
import numpy as np
data = pandas.read_excel('OneDrive_1_22-10-2025\matlabcode\Fridaytest2dataexport.xlsx')

times = data['timestamps']

flowvolume = data['FLOWcounterCalibrated']
PPT1 = data['Var4']
PPT2 = data['Var3']
PPT3 = data['Var5']



#Using data collected to convert PPT voltages to Pressure (KPa), and to convert the flow count into a flowrate

PPT1 = (PPT1 -0.0069594)/0.0016471
PPT2 = (PPT2 - 0.0081294) / 0.0016308
PPT3 = (PPT3 - 0.0053957) / 0.0016309









def smooth_data(data, window_size):
    return pandas.Series(data).rolling(window=window_size, min_periods=1).mean().tolist()


flowvolume = smooth_data(flowvolume,100)

PPT1 = smooth_data(PPT1, 40)
PPT2 = smooth_data(PPT2, 40)
PPT3 = smooth_data(PPT3, 40)
flowrate = np.gradient(flowvolume)

flowrate = smooth_data(flowrate,40)
flowrate = np.array(flowrate)
import matplotlib.pyplot as plt



fig, (ax1, ax2,ax3) = plt.subplots(3, 1, figsize=(10, 12))

# Plot PPT1, PPT2, PPT3 on the first graph
ax1.plot(times, PPT1, label='PPT1')
ax1.plot(times, PPT2, label='PPT2')
ax1.plot(times, PPT3, label='PPT3')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Pore Pressure (KPa)')
ax1.set_title('Pore Pressures vs Time')
ax1.legend(loc='upper left')
ax1.grid(True)

# Plot flow volume on the second graph
ax2.plot(times, flowrate, label='Flow Volume', color='orange')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Flow rate (g/s)')
ax2.set_title('Flow rate vs Time')
ax2.legend(loc='upper left')
ax2.grid(True)

pressurechange = []
permiability = []

for i in range(len(PPT2)):
    pressurechange.append(PPT3[i]-PPT2[i])
    permiability.append(flowrate[i]/pressurechange[-1])
permiability = smooth_data(permiability,100)

ax3.plot(times,permiability)

plt.tight_layout()
plt.show()