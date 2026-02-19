#This version of the data processing program (forked on 18/02/26) doesn't use the smoothed average, 
# only using a butterworth filter to remove noise
#This also imports the .mat file directly rather than using the .xlsx so that there isn't the limitation for data processing
#if processing a full experiment, purging half the rows is probably worthwile so that it can process quickly **** after calculating flowcount ****


import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py


#data = pandas.read_excel('OneDrive_1_22-10-2025\Matlabcode\HTdatacollection\Feb18\Test2dataexport.xlsx')

matdata = h5py.File('OneDrive_1_22-10-2025\matlabcode\HTdata\Feb17\Test2.mat','r+')

PPT1  = np.array(matdata['PPTdata'][1])
PPT2 = np.array(matdata['PPTdata'][0])
PPT3 = np.array(matdata['PPTdata'][2])

times = np.array(matdata['timestamps'][0])
FLOWdata = np.array(matdata['FLOWdata'])

FLOWcounter = np.concatenate([[0], np.cumsum(np.abs(np.diff(np.sign(FLOWdata - 2.5))) > 1)])


#converting voltages and counts into volumes and pressures

flowvolume = FLOWcounter * 4.260 * 10**(-7)
PPT1 = PPT1 * 608.5052 - 4.2710
PPT2 = PPT2 *613.0834 - 4.99827
PPT3 = PPT3 * 611.7754 - 3.2881

#constants defined for butterworth function 
fs = int(1 / (times[100] - times[99]))
cutoff = 2  # cutoff frequency in Hz

PPT1 = plottingfunctions.butterfilter(PPT1,fs,cutoff)
PPT2 = plottingfunctions.butterfilter(PPT2,fs,cutoff)
PPT3 = plottingfunctions.butterfilter(PPT3,fs,cutoff)



#calculate flowrate based off flowvolume, must be multiplied to get from gradient / frame to gradient/ s 
flowrate = np.gradient(flowvolume) * fs
flowrate = plottingfunctions.butterfilter(flowrate,fs,cutoff)
flowrateraw = np.array(flowrate)




#adjusting PPT data to get the change in pressure rather than considering total pressure as Darcy's law ignores the head difference ( so for static h = 0 at both)
noflowtimes = [1,7]
timelist = times.tolist()
startindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - noflowtimes[0]))
endindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - noflowtimes[1]))
PPT1base = np.average(PPT1[startindex:endindex])
PPT2base = np.average(PPT2[startindex:endindex])
PPT3base = np.average(PPT3[startindex:endindex])

PPT1adjusted = (PPT1 - PPT1base) * 1000
PPT2adjusted = (PPT2 - PPT2base) * 1000
PPT3adjusted = (PPT3 - PPT2base) * 1000






fig, (ax1, ax2,ax3,ax4) = plt.subplots(4, 1, figsize=(10, 8))


#plotting of PPT1, PPT2, PPT3
ax1.plot(times,PPT1adjusted, label = 'PPT1 offset')
ax1.plot(times,PPT2adjusted, label = 'PPT2 offset')
ax1.plot(times,PPT3adjusted, label = 'PPT3 offset')

ax1.set_xlabel('Time')
ax1.set_ylabel('Pressure (Pa)')
ax1.legend()
ax1.grid(True)



#Plotting flowrate
ax2.plot(times, flowrate)
ax2.set_xlabel('Time')
ax2.set_ylabel('Flow Rate (m^3 / s)')
ax2.grid(True)


plt.tight_layout()
plt.show()