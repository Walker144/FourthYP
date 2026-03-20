
import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py

#This also imports the .mat file directly rather than using the .xlsx so that there isn't the limitation for data processing
#if processing a full experiment, purging half the rows is probably worthwile so that it can process quickly **** after calculating flowcount ****
#data = pandas.read_excel('OneDrive_1_22-10-2025\Matlabcode\HTdata\Feb17\Test2dataexport.xlsx')

#####################################
#####       FILE TO OPEN        #####
#####################################

f  = 'OneDrive_1_22-10-2025\matlabcode\HTdatacollection\Mar02\Test2.mat'
# set the nth sampling rate, so the data that will be used is 1 in n, starting from 0
nrate = 10



def smooth_data(data, window_size):
    return pandas.Series(data).rolling(window=window_size, min_periods=1).mean().tolist()


matdata = h5py.File(f,'r+')
#PPT 1 and 2 are wired the wrong way around as of 17/02/26. When we re calibrate it might be worth changing that..
PPT1  = np.array(matdata['PPTdata'][1])[1::nrate]
PPT2 = np.array(matdata['PPTdata'][0])[1::nrate]
PPT3 = np.array(matdata['PPTdata'][2])[1::nrate]
times = np.array(matdata['timestamps'][0])[1::nrate]
FLOWdata = np.array(matdata['FLOWdata'])

#This needs updating whenever the test is changed
ppt_start_time = "16:25:10"

#Using data collected to convert PPT voltages to Pressure (KPa), and to convert the flow count into a flowrate
fs = int(1 / (times[100] - times[99])) 
cutoff = 2  # cutoff frequency in Hz
FLOWcounter = np.concatenate([[0], np.cumsum(np.abs(np.diff(np.sign(FLOWdata - 2.5))) > 1)])[1::nrate]
flowvolume = FLOWcounter * 3.87 * 10**(-7)
flowrate = np.gradient(flowvolume) * fs
PPT1 = PPT1 * 608.5052 - 4.2710
PPT2 = PPT2 *613.0834 - 4.99827
PPT3 = PPT3 * 611.7754 - 3.2881






# Data smoothing
PPT1 = plottingfunctions.butterfilter(PPT1,fs,cutoff)
PPT2 = plottingfunctions.butterfilter(PPT2,fs,cutoff)
PPT3 = plottingfunctions.butterfilter(PPT3,fs,cutoff)







#calculate flowrate based off flowvolume, must be multiplied to get from gradient / frame to gradient/ s 
flowrate = plottingfunctions.butterfilter(flowrate,fs,cutoff)
flowrateraw = np.array(flowrate)




#adjusting PPT data to get the change in pressure rather than considering total pressure as Darcy's law ignores the head difference ( so for static h = 0 at both)
noflowtimes = [0,10]
plotendtime = times[-1] - 10


timelist = times.tolist()
startindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - noflowtimes[0]))
endindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - noflowtimes[1]))
PPT1base = np.average(PPT1[startindex:endindex])
PPT2base = np.average(PPT2[startindex:endindex])
PPT3base = np.average(PPT3[startindex:endindex])

PPT1adjusted = (PPT1 - PPT1base) * 1000
PPT2adjusted = (PPT2 - PPT2base) * 1000
PPT3adjusted = (PPT3 - PPT2base) * 1000





#plotting of PPT1 , PPT2 (and in the future PPT3)

fig, (ax1, ax2,ax3,ax4) = plt.subplots(4, 1, figsize=(10, 8))


ax1.plot(times,PPT1adjusted, label = 'PPT1 offset')
ax1.plot(times,PPT2adjusted, label = 'PPT2 offset')
ax1.plot(times,PPT3adjusted, label = 'PPT3 offset')
ax1.set_xlabel('Time')
ax1.set_ylabel('Pressure (Pa)')
ax1.legend()
ax1.grid(True)
ax1.set_xlim(0,plotendtime)



#Plotting of Flow rate
ax2.plot(times, flowrate)
ax2.set_xlabel('Time')
ax2.set_ylabel('Flow Rate (m^3 / s)')
ax2.grid(True)
ax2.set_xlim(0,plotendtime)



#calculating hydraulic gradient is deltah = deltap / rho g
rhog = 1000 * 9.806
hgraident = (PPT1adjusted - PPT3adjusted) / (rhog * 0.2)  #0.2 as 200mm between PPT1 and PPT3


#plotting hydraulic gradient with critical hydraulic gradient
ax3.plot(times, smooth_data(hgraident,1000),label = 'Hydrualic Gradient between PPT1 and PPT3' , color = 'blue')
icrit = 1.1113
ax3.plot([0,times[len(times)-1]],[icrit,icrit],color = 'red',linestyle = '--')

ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Hydraulic Gradient')
ax3.legend()
ax3.grid(True)
ax3.set_xlim(0,plotendtime)



permiabilitysmoothed = flowrate / hgraident * 1000 #multiplied by 1000 due to geometry, this needs checking next term so don't use for report results
permiabilitysmoothed = np.array(smooth_data(permiabilitysmoothed,1000)) #rolling average of 1000 frames taken so that the data plots better






ax4.plot(times,permiabilitysmoothed, label = 'Permiability')
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Permiability')
ax4.grid(True)
ax4.legend()
ax4.set_xlim(0,plotendtime) 
ax4.set_ylim(0,max(permiabilitysmoothed)*1.2)


plt.tight_layout()
plt.show()