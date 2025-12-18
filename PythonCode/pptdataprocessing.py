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




PPT1 = smooth_data(PPT1, 100)
PPT2 = smooth_data(PPT2, 100)
PPT3 = smooth_data(PPT3, 100)





plt.figure(figsize=(10, 6))

plt.plot(times3, PPT3, label='PPT3')

#array of arrays with the times that it's stable
stabletime2 = [[0,4],[6,13],[15,22],[24,32],[35,42],[44,52],[55,70],[72,82],[86,91],[96,102],[104,109],[114,118],[124,127],[133,140],[145,146]]

stabletime = [[0,7],[11,36],[38,58],[60,67],[68,76],[78,90],[94,99],[103,122],[129,135],[142,148],[155,160],[167,170],[180,185],[192,197],[200,204]]

vaverages = []
times1 = times3.tolist()
for timeset in stabletime:
    
    startindex = times1.index(timeset[0])
    endindex = times1.index(timeset[1])
    vaverages.append(np.average(PPT3[startindex:endindex]))
    plt.plot(timeset, [vaverages[-1], vaverages[-1]],
             marker='p', linestyle='-', color='green',
             markerfacecolor='green', markeredgecolor='green')

plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.title('Voltage - Time graph ')

print(vaverages)
vaverages = np.array(vaverages)
pressures = np.array([1,2,4,6,8,10,15,20,15,10,8,6,4,2,1])



# Linear fit (pressure -> PPT average)
slope, intercept = np.polyfit(pressures, vaverages, 1)


# Line for plotting
x_line = np.linspace(pressures.min(), pressures.max(), 200)
y_line = slope * x_line + intercept

# Plot fit on a new figure
plt.figure(figsize=(8, 6))
plt.scatter(pressures, vaverages, color='blue', label='data points')
plt.plot(x_line, y_line, color='red', label=f'fit: y={slope:.7f}x + {intercept:.7f}')
plt.xlabel('Pressure')
plt.ylabel('PPT average')
plt.title('PPT Average vs Pressure with Linear Fit')
plt.legend()
plt.grid(True)






#plt.plot(times2, PPT2, label='PPT2')
#plt.plot(times3, PPT3, label='PPT3')

plt.xlabel('Pressure (KPa)')
plt.ylabel('Voltage (V)')

plt.legend()
plt.grid(True)

plt.show()