
import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
data = pandas.read_excel('OneDrive_1_22-10-2025\matlabcode\Fridaytest2dataexport.xlsx')
#data = pandas.read_excel('OneDrive_1_22-10-2025\FlowCalibrationData\watercalibration2dataexport.xlsx')

times = data['timestamps']


flowvolume = data['FLOWcounterCalibrated'] * 4.260 * 10**(-7)
PPT1 = data['Var4']
PPT2 = data['Var3']
PPT3 = data['Var5']



#Using data collected to convert PPT voltages to Pressure (KPa), and to convert the flow count into a flowrate






PPT1 = PPT1 * 608.5052 - 4.2710
PPT2 = PPT2 *613.0834 - 4.99827
PPT3 = PPT3 * 611.7754 - 3.2881









def smooth_data(data, window_size):
    return pandas.Series(data).rolling(window=window_size, min_periods=1).mean().tolist()




fs = int(1 / (times[100] - times[99]))
cutoff = 2  # cutoff frequency in Hz

PPT1 = plottingfunctions.butterfilter(PPT1,fs,cutoff)
PPT2 = plottingfunctions.butterfilter(PPT2,fs,cutoff)
PPT3 = plottingfunctions.butterfilter(PPT3,fs,cutoff)


#calculate flowrate based off flowvolume, must be multiplied to get from gradient / frame to gradient/ s 
flowrate = np.gradient(flowvolume) * fs
flowrate = plottingfunctions.butterfilter(flowrate,fs,cutoff)
flowrate = np.array(flowrate)


#adjusting PPT data to get the change in pressure rather than considering total pressure as Darcy's law ignores the head difference ( so for static h = 0 at both)
noflowtimes = [13,24]
timelist = times.tolist()
startindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - noflowtimes[0]))
endindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - noflowtimes[1]))
PPT1base = np.average(PPT1[startindex:endindex])
PPT2base = np.average(PPT2[startindex:endindex])

PPT1adjusted = (PPT1 - PPT1base) * 1000
PPT2adjusted = (PPT2 - PPT2base) * 1000




#plotting of PPT1 , PPT2 (and in the future PPT3), and flow rate 

fig, (ax1, ax2,ax3,ax4) = plt.subplots(4, 1, figsize=(10, 8))

'''ax1.plot(times, PPT1, label='PPT1')
ax1.plot(times, PPT2, label='PPT2')'''



ax1.plot(times,smooth_data(PPT1adjusted,100), label = 'PPT1 offset')
ax1.plot(times,smooth_data(PPT2adjusted,100), label = 'PPT2 offset')
ax1.set_xlabel('Time')
ax1.set_ylabel('Pressure (KPa)')
ax1.legend()
ax1.grid(True)




ax2.plot(times, flowrate)
ax2.set_xlabel('Time')
ax2.set_ylabel('Flow Rate (m^3 / s)')
ax2.grid(True)



#calculating hydraulic gradient is deltah = deltap / rho g
rhog = 1000 * 9.806

hgradient = (PPT2adjusted - PPT1adjusted) / rhog
ax4.plot(times[20000::], smooth_data(hgradient,1000)[20000::])
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Hydraulic Gradient')
ax4.grid(True)


permiability = flowrate / hgradient * 100 #multiplied by 100 due to geometry, this needs checking next term so don't use for report results
permiability = smooth_data(permiability,1000) 

permiability = np.array(smooth_data(permiability,100))

ax3.plot(times[20000::],permiability[20000::])
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Permiability')
ax3.grid(True)


plt.tight_layout()
plt.show()