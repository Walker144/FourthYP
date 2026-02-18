
import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
#data = pandas.read_excel('OneDrive_1_22-10-2025\Matlabcode\HTdata\Feb17\Test2dataexport.xlsx')


data = pandas.read_excel('OneDrive_1_22-10-2025\Matlabcode\HTdata\Feb13\Test1dataexport.xlsx')
#data = pandas.read_excel('OneDrive_1_22-10-2025\FlowCalibrationData\watercalibration2dataexport.xlsx')


times = data['timestamps']


flowvolume = data['FLOWcounterCalibrated'] * 4.260 * 10**(-7)

#PPT 1 and 2 are wired the wrong way around as of 17/02/26. When we re calibrate it might be worth changing that..
PPT1 = data['PPT2']
PPT2 = data['PPT1']
PPT3 = data['PPT3']



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
#using constant over region to give a better smoothed signal, will plot both together with chainlinked for 'more smoothed' data

#idk where this data was collected from but probably shouldn't delete it lol
#smoothregions  = [[0,25],[28,57],[59,73],[75,88],[91,99],[101,127],[127,146],[148,168],[170,196],[200,214],[216,242],[243,251],[253,256],[257,264],[265,271],[272,281],[282,290]]



#17th feb
#smoothregions = [[0.8,12.4],[16,38],[40,71],[73,97],[108,138],[143,172],[176,206],[214,243],[247,277],[290,326],[330,363],[365,395],[398,428],[437,472],[477,508],[511,542],[576,606],[609,643],[764,778],[793,812],[835,861],[866,895],[898,940],[946,971],[981,1010],[1013,1040],[1046,1076],[1080,1103],[1120,1152],[1159,1186],[1190,1219],[1221,1261],[1263,1300],[1303,1331],[1334,1365],[1367,1395],[1398,1451]]
smoothregions = [[1.8,11],[13,24],[26,55],[57,86],[88,118],[120,148],[150,178],[181,208],[211,240],[243,271],[274,303],[306,331],[337,366],[368,396],[400,419],[421,451],[454,482],[485,514],[517,547],[548,580],[700,756],[760,784],[790,822],[828,848],[851,865],[868,897],[900,928],[930,960],[964,995],[998,1027],[1030,1080],[1083,1107],[1110,1140],[1145,1178],[1185,1209],[1214,1239],[1246,1270],[1278,1303],[1310,1340]]


PPT1smoothed = plottingfunctions.replacewithconstants(PPT1,times,smoothregions)

PPT2smoothed = plottingfunctions.replacewithconstants(PPT2,times,smoothregions)
PPT3smoothed = plottingfunctions.replacewithconstants(PPT3,times,smoothregions)






#calculate flowrate based off flowvolume, must be multiplied to get from gradient / frame to gradient/ s 
flowrate = np.gradient(flowvolume) * fs


flowrate = plottingfunctions.butterfilter(flowrate,fs,cutoff)
flowrateraw = np.array(flowrate)
flowrate = plottingfunctions.replacewithconstants(flowrateraw,times,smoothregions)



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


PPT1sadjusted = (PPT1smoothed - PPT1base) * 1000
PPT2sadjusted = (PPT2smoothed - PPT2base) * 1000
PPT3sadjusted = (PPT3smoothed - PPT3base) * 1000



#plotting of PPT1 , PPT2 (and in the future PPT3), and flow rate 

fig, (ax1, ax2,ax3,ax4) = plt.subplots(4, 1, figsize=(10, 8))

'''ax1.plot(times, PPT1, label='PPT1')
ax1.plot(times, PPT2, label='PPT2')'''



ax1.plot(times,PPT1sadjusted, label = 'PPT1 offset')
ax1.plot(times,PPT2sadjusted, label = 'PPT2 offset')
ax1.plot(times,PPT3sadjusted, label = 'PPT3 offset')

ax1.set_xlabel('Time')
ax1.set_ylabel('Pressure (Pa)')
ax1.legend()
ax1.grid(True)




ax2.plot(times, flowrate)

#ax2.plot(times, flowrateraw,label = 'raw')

ax2.set_xlabel('Time')
ax2.set_ylabel('Flow Rate (m^3 / s)')
ax2.grid(True)



#calculating hydraulic gradient is deltah = deltap / rho g
rhog = 1000 * 9.806

#hgradient = (PPT3adjusted - PPT1adjusted) / rhog
hgraidentsmoothed = (PPT1sadjusted - PPT3sadjusted) / (rhog * 0.2)  



#ax4.plot(times[20000::], smooth_data(hgradient,1000)[20000::], label = 'unsmoothed')
ax4.plot(times, smooth_data(hgraidentsmoothed,1000),label = 'Hydrualic Gradient between PPT1 and PPT3' , color = 'blue')
icrit = 1.1113
ax4.plot([0,times[len(times)-1]],[icrit,icrit],color = 'red',linestyle = '--')

ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Hydraulic Gradient')
ax4.legend()
ax4.grid(True)


#permiability = flowrate / hgradient * 100 #multiplied by 100 due to geometry, this needs checking next term so don't use for report results
permiabilitysmoothed = flowrate / hgraidentsmoothed * 100

#permiability = np.array(smooth_data(permiability,1000))
permiabilitysmoothed = np.array(smooth_data(permiabilitysmoothed,1000))
#ax3.plot(times[20000::],permiability[20000::], label = 'unsmoothed')


#plot only the smoothed regions for permiability so it's easier to see
timestoplot = []
permstoplot = []
for s in smoothregions:
    startindex = min(range(len(times)), key=lambda i: abs(times[i] - s[0]))
    endindex = min(range(len(times)), key=lambda i: abs(times[i] - s[1]))
    permstoplot = np.concatenate([permstoplot, permiabilitysmoothed[startindex:endindex]])
    timestoplot  = np.concatenate([timestoplot ,  times[startindex:endindex]])


ax3.plot(timestoplot,permstoplot, label = 'smoothed',color = 'deepskyblue',linestyle = '--')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Permiability')
ax3.grid(True)
ax3.legend()


plt.tight_layout()
plt.show()