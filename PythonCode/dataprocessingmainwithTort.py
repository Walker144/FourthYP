
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

f  = 'OneDrive_1_22-10-2025\matlabcode\HTdatacollection\Feb24\Test2.mat'
# set the nth sampling rate, so the data that will be used is 1 in n, starting from 0
nrate = 10

taufactordatafile = 'OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\Tauout.txt'
taufile = open(taufactordatafile).read().split('\n')

Tortuosity = []
Effective_Diffusion = []
Real_Timestamps = []

for datapoint in taufile[0:-1]:
    datapoint = datapoint.split(',')
    Tortuosity.append(float(datapoint[2][1:-1]))
    Effective_Diffusion.append(float(datapoint[1][1:-1]))
    Real_Timestamps.append(datapoint[0].split(' ')[1])





def smooth_data(data, window_size):
    return pandas.Series(data).rolling(window=window_size, min_periods=1).mean().tolist()


matdata = h5py.File(f,'r+')
#PPT 1 and 2 are wired the wrong way around as of 17/02/26. When we re calibrate it might be worth changing that..
PPT1  = np.array(matdata['PPTdata'][1])[1::nrate]
PPT2 = np.array(matdata['PPTdata'][0])[1::nrate]
PPT3 = np.array(matdata['PPTdata'][2])[1::nrate]
times = np.array(matdata['timestamps'][0])[1::nrate]
FLOWdata = np.array(matdata['FLOWdata'])

#This needs updating whenever the test is changed, i hate that this is hard coded and not pulled from the .mat but that's life
ppt_start_time = "16:25:10".split(':')
matchid_start_time = Real_Timestamps[0].split(':')
matchid_second_time = Real_Timestamps[1].split(':')

timediff = - (int(ppt_start_time[1]) - int(matchid_start_time[1])) * 60 - (float(ppt_start_time[2]) - float(matchid_start_time[2]))
dt = (int(matchid_second_time[1]) - int(matchid_start_time[1])) * 60 + (float(matchid_second_time[2]) - float(matchid_start_time[2]))
Tortuosity_time = timediff + dt * np.arange(len(Real_Timestamps))





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

fsmooth = outfilename = f[:-4] + 'times.txt'
smoothdata = open(fsmooth,'r').read().split('\n')
smoothregions = []

for s in smoothdata:
    slist = s.split(',')
    smoothregions.append([float(slist[0]),float(slist[1])])


PPT1smoothed = plottingfunctions.replacewithconstants(PPT1,times,smoothregions)
PPT2smoothed = plottingfunctions.replacewithconstants(PPT2,times,smoothregions)
PPT3smoothed = plottingfunctions.replacewithconstants(PPT3,times,smoothregions)
plotendtime = smoothregions[-1][1] - 10



#calculate flowrate based off flowvolume, must be multiplied to get from gradient / frame to gradient/ s 
flowrate = plottingfunctions.butterfilter(flowrate,fs,cutoff)
flowrateraw = np.array(flowrate)
flowrate = plottingfunctions.replacewithconstants(flowrateraw,times,smoothregions)



#adjusting PPT data to get the change in pressure rather than considering total pressure as Darcy's law ignores the head difference ( so for static h = 0 at both)
noflowtimes = [smoothregions[0][0] + 1,smoothregions[0][1] - 1]
timelist = times.tolist()
startindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - noflowtimes[0]))
endindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - noflowtimes[1]))
PPT1base = np.average(PPT1[startindex:endindex])
PPT2base = np.average(PPT2[startindex:endindex])
PPT3base = np.average(PPT3[startindex:endindex])

PPT1adjusted = (PPT1 - PPT1base) * 1000
PPT2adjusted = (PPT2 - PPT2base) * 1000
PPT3adjusted = (PPT3 - PPT2base) * 1000


PPT1sadjusted = (PPT1smoothed - PPT1base) * 1000
PPT2sadjusted = (PPT2smoothed - PPT2base) * 1000
PPT3sadjusted = (PPT3smoothed - PPT3base) * 1000



#plotting of PPT1 , PPT2 (and in the future PPT3)

fig, (ax1, ax2,ax3,ax4) = plt.subplots(4, 1, figsize=(10, 8))


ax1.plot(times,PPT1sadjusted, label = 'PPT1 offset')
ax1.plot(times,PPT2sadjusted, label = 'PPT2 offset')
ax1.plot(times,PPT3sadjusted, label = 'PPT3 offset')
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
hgraidentsmoothed = (PPT1sadjusted - PPT3sadjusted) / (rhog * 0.2)  #0.2 as 200mm between PPT1 and PPT3


#plotting hydraulic gradient with critical hydraulic gradient
ax4.plot(times, smooth_data(hgraidentsmoothed,1000),label = 'Hydrualic Gradient between PPT1 and PPT3' , color = 'blue')
icrit = 1.1113
ax4.plot([0,times[len(times)-1]],[icrit,icrit],color = 'red',linestyle = '--')

ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Hydraulic Gradient')
ax4.legend()
ax4.grid(True)
ax4.set_xlim(0,plotendtime)



permiabilitysmoothed = flowrate / hgraidentsmoothed * 1000 #multiplied by 1000 due to geometry, this needs checking next term so don't use for report results
permiabilitysmoothed = np.array(smooth_data(permiabilitysmoothed,1000)) #rolling average of 1000 frames taken so that the data plots better




timestoplot = []
permstoplot = []
for s in smoothregions:
    startindex = min(range(len(times)), key=lambda i: abs(times[i] - s[0]))
    endindex = min(range(len(times)), key=lambda i: abs(times[i] - s[1]))
    permstoplot = np.concatenate([permstoplot, permiabilitysmoothed[startindex:endindex]])
    timestoplot  = np.concatenate([timestoplot ,  times[startindex:endindex]])


ax3.plot(timestoplot,permstoplot, label = 'Permiability',color = 'deepskyblue')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Permiability')
ax3.grid(True)
ax3.set_xlim(0,plotendtime) 
ax3.set_ylim(0,max(permstoplot)*1.2)
ax3.set_ylim(0,0.15)
ax3b = ax3.twinx()

ax3b.plot(Tortuosity_time,Tortuosity,label = 'Tortuosity',color = 'red',linestyle = '--')
ax3b.set_ylabel("Tortuosity")

plt.tight_layout()
plt.show()