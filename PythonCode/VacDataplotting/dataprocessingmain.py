
import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd

#This also imports the .mat file directly rather than using the .xlsx so that there isn't the limitation for data processing
#if processing a full experiment, purging half the rows is probably worthwile so that it can process quickly **** after calculating flowcount ****
#data = pandas.read_excel('OneDrive_1_22-10-2025\Matlabcode\HTdata\Feb17\Test2dataexport.xlsx')

#####################################
#####       FILE TO OPEN        #####
#####################################


## Apr01 Test 3
f  = "I:\Apr01\Test3\Apr01Test3.mat"
tortuosity12file = "I:\Apr01\Test3\Tortuosity12.csv"
tortuosity23file = "I:\Apr01\Test3\Tortuosity23.csv"
tortuosity13file = "I:\Apr01\Test3\Tortuosity13.csv"
voidratio12file = "I:\Apr01\Test3\VoidRatio12.csv"
voidratio23file = "I:\Apr01\Test3\VoidRatio23.csv"
voidratio13file = "I:\Apr01\Test3\VoidRatio13.csv"
ppt_start_time = "11:26:46"
cleanuptimes = [[0,13],[13,63],[950,992],[992,1008]]



#Apr01 Test 6
'''f  = "I:\Apr01\Test6\Apr01Test6.mat"
tortuosity12file = "I:\Apr01\Test6\Tortuosity12.csv"
tortuosity23file = "I:\Apr01\Test6\Tortuosity23.csv"
#tortuosity13file = "I:\Apr01\Test6\Tortuosity13.csv"
voidratio12file = "I:\Apr01\Test6\VoidRatio12.csv"
voidratio23file = "I:\Apr01\Test6\VoidRatio23.csv"
voidratio13file = "I:\Apr01\Test6\VoidRatio13.csv"
ppt_start_time = "17:11:28"'''

'''f  = "I:\Apr01\Test5\Apr01Test5.mat"
tortuosity12file = "I:\Apr01\Test5\Tortuosity12.csv"
tortuosity23file = "I:\Apr01\Test5\Tortuosity23.csv"
#tortuosity13file = "I:\Apr01\Test6\Tortuosity13.csv"
voidratio12file = "I:\Apr01\Test5\VoidRatio12.csv"
voidratio23file = "I:\Apr01\Test5\VoidRatio23.csv"
voidratio13file = "I:\Apr01\Test5\VoidRatio13.csv"
ppt_start_time = "16:25:09"'''




## Apr01 Test 1
'''f  = "H:\Apr01\Test1\Apr01Test1.mat"
tortuosity12file = "H:\Apr01\Test1\Tortuosity12.csv"
tortuosity23file = "H:\Apr01\Test1\Tortuosity23.csv"
tortuosity13file = "H:\Apr01\Test1\Tortuosity13.csv"
voidratio12file = "H:\Apr01\Test1\VoidRatio12.csv"
voidratio23file = "H:\Apr01\Test1\VoidRatio23.csv"
voidratio13file = "H:\Apr01\Test1\VoidRatio13.csv"
ppt_start_time = "9:51:49"'''


'''#Mar 27 Test 1
f  = "I:\Mar27\Test1\Mar27Test1.mat"
tortuosity12file = "I:\Mar27\Test1\Tortuosity12.csv"
tortuosity23file = "I:\Mar27\Test1\Tortuosity23.csv"
voidratio12file = "I:\Mar27\Test1\VoidRatio12.csv"
voidratio23file = "I:\Mar27\Test1\VoidRatio23.csv"
voidratio13file = "I:\Mar27\Test1\VoidRatio13.csv"
ppt_start_time = "11:28:41"'''

#Mar 27 Test 3

'''f  = "I:\Mar27\Test3\Mar27Test3.mat"
tortuosity12file = "I:\Mar27\Test3\Tortuosity12.csv"
tortuosity23file = "I:\Mar27\Test3\Tortuosity23.csv"
voidratio12file = "I:\Mar27\Test3\VoidRatio12.csv"
voidratio23file = "I:\Mar27\Test3\VoidRatio23.csv"
voidratio13file = "I:\Mar27\Test3\VoidRatio13.csv"
ppt_start_time = "12:28:49"'''

#Apr01 Test 4
'''f  = "H:\Apr01\Test4\Apr01Test4.mat"
tortuosity12file = "H:\Apr01\Test4\Tortuosity12.csv"
tortuosity23file = "H:\Apr01\Test4\Tortuosity12Right.csv"
tortuosity13file = "H:\Apr01\Test4\Tortuosity13.csv"
voidratio12file = "H:\Apr01\Test4\VoidRatio12.csv"
voidratio23file = "H:\Apr01\Test4\VoidRatio23.csv"
voidratio13file = "H:\Apr01\Test4\VoidRatio13.csv"
ppt_start_time = "11:44:29"'''


#Apr16 Test 1
f  = "I:\Apr16\Test1\Apr16Test1.mat"
tortuosity12file = "I:\Apr16\Test1\Tortuosity12.csv"
tortuosity23file = "I:\Apr16\Test1\Tortuosity23.csv"
tortuosity13file = "I:\Apr16\Test1\Tortuosity13.csv"
voidratio12file = "I:\Apr16\Test1\VoidRatio12.csv"
voidratio23file = "I:\Apr16\Test1\VoidRatio23.csv"
voidratio13file = "I:\Apr16\Test1\VoidRatio13.csv"
CN12file = "I:\Apr16\Test1\CoordinationNumbers12.csv"
CN23file = "I:\Apr16\Test1\CoordinationNumbers23.csv"
CN13file = "I:\Apr16\Test1\CoordinationNumbers13.csv"


ppt_start_time = "15:18:45"

cleanuptimes = [[0,18],[18,57],[57,100],[100,143],[143,185]]


#Apr16 Test 2
'''f  = "I:\Apr16\Test2\Apr16Test2.mat"
tortuosity12file = "I:\Apr16\Test2\Tortuosity12.csv"
tortuosity23file = "I:\Apr16\Test2\Tortuosity23.csv"
tortuosity13file = "I:\Apr16\Test2\Tortuosity13.csv"
voidratio12file = "I:\Apr16\Test2\VoidRatio12.csv"
voidratio23file = "I:\Apr16\Test2\VoidRatio23.csv"
voidratio13file = "I:\Apr16\Test2\VoidRatio13.csv"


ppt_start_time = "15:42:24"

cleanuptimes = [[0,17],[17,59],[59,101],[101,142],[142,186]]'''




# set the nth sampling rate, so the data that will be used is 1 in n, starting from 0
nrate = 10
#This needs updating whenever the test is changed

# Apr01 Test 2 ppt_start_time = "10:42:26"

#Apr01 Test 3
#
#Mar27 test 1



def smooth_data(data, window_size):
    return pandas.Series(data).rolling(window=window_size, min_periods=1).mean().tolist()

def convert_time_to_seconds(Timestamp):
    Timestamp = Timestamp.split(':')
    return float(Timestamp[-1]) + 60* float(Timestamp[-2]) + 3600 * float(Timestamp[-3])


def convert_datafile_to_relative_time(TortDF,ppt_start_time,datacolumn = "Tortuosity"):
    offsettime = convert_time_to_seconds(ppt_start_time)
    timestamps = TortDF["Timestamp"]
    torttimes = []
    for t in timestamps:
        torttimes.append(convert_time_to_seconds(t.split(' ')[1]) - offsettime)
    
    Tortuosity = TortDF[datacolumn]
    return torttimes,Tortuosity
    



matdata = h5py.File(f,'r+')
#PPT 1 and 2 are wired the wrong way around as of 17/02/26. When we re calibrate it might be worth changing that..
PPT1  = np.array(matdata['PPTdata'][1])[1::nrate]
PPT2 = np.array(matdata['PPTdata'][0])[1::nrate]
PPT3 = np.array(matdata['PPTdata'][2])[1::nrate]
times = np.array(matdata['timestamps'][0])[1::nrate]
FLOWdata = np.array(matdata['FLOWdata'])



#Using data collected to convert PPT voltages to Pressure (KPa), and to convert the flow count into a flowrate
fs = int(1 / (times[100] - times[99])) 
cutoff = 2  # cutoff frequency in Hz
FLOWcounter = np.concatenate([[0], np.cumsum(np.abs(np.diff(np.sign(FLOWdata - 2.5))) > 1)])[1::nrate]
flowvolume = FLOWcounter * 3.87 * 10**(-7)



flowrate = np.gradient(flowvolume) * fs
PPT1 = PPT1 * 608.5052 - 4.2710
PPT2 = PPT2 *613.0834 - 4.99827
PPT3 = PPT3 * 611.7754 - 3.2881

#opening tortuosity folder
TortDF = pd.read_csv(tortuosity12file)
Tort23DF = pd.read_csv(tortuosity23file)
#Tort13DF = pd.read_csv(tortuosity13file)
void12DF = pd.read_csv(voidratio12file)
void23DF = pd.read_csv(voidratio23file)
void13DF = pd.read_csv(voidratio13file)

tort12times, Tortuosity12 = convert_datafile_to_relative_time(TortDF,ppt_start_time,"Tortuosity")
tort12times, Tortuosity23 = convert_datafile_to_relative_time(Tort23DF,ppt_start_time,"Tortuosity")
#tort12times, Tortuosity13 = convert_datafile_to_relative_time(Tort13DF,ppt_start_time,"Tortuosity")
void12times, VoidRatio12 = convert_datafile_to_relative_time(void12DF,ppt_start_time,"VoidRatio")
void23times, VoidRatio23 = convert_datafile_to_relative_time(void23DF,ppt_start_time,"VoidRatio")
void13times, VoidRatio13 = convert_datafile_to_relative_time(void13DF,ppt_start_time,"VoidRatio")




# Data smoothing
PPT1 = plottingfunctions.butterfilter(PPT1,fs,cutoff)
PPT2 = plottingfunctions.butterfilter(PPT2,fs,cutoff)
PPT3 = plottingfunctions.butterfilter(PPT3,fs,cutoff)







#calculate flowrate based off flowvolume, must be multiplied to get from gradient / frame to gradient/ s 
flowrate = plottingfunctions.butterfilter(flowrate,fs,cutoff)
flowrateraw = np.array(flowrate)




#adjusting PPT data to get the change in pressure rather than considering total pressure as Darcy's law ignores the head difference ( so for static h = 0 at both)
noflowtimes = [0,18]
plotendtime = times[-1] - 10




timelist = times.tolist()
startindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - noflowtimes[0]))
endindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - noflowtimes[1]))
PPT1base = np.average(PPT1[startindex:endindex])
PPT2base = np.average(PPT2[startindex:endindex])
PPT3base = np.average(PPT3[startindex:endindex])

PPT1adjusted = (PPT1 - PPT1base) * 1000
PPT2adjusted = (PPT2 - PPT2base) * 1000
PPT3adjusted = (PPT3 - PPT3base) * 1000

PPT1adjusted = plottingfunctions.replacewithconstants(PPT1adjusted,timelist,cleanuptimes)
PPT2adjusted = plottingfunctions.replacewithconstants(PPT2adjusted,timelist,cleanuptimes)
PPT3adjusted = plottingfunctions.replacewithconstants(PPT3adjusted,timelist,cleanuptimes)


#plotting of PPTs

fig, ((ax1,ax2),(ax3,ax4),(ax5,ax6)) = plt.subplots(3, 2, figsize=(10, 8))


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
hgradient13 = (PPT1adjusted - PPT3adjusted) / (rhog * 0.2)  #0.2 as 200mm between PPT1 and PPT3
hgradient12 = (PPT1adjusted - PPT2adjusted) / (rhog * 0.1)
hgradient23 = (PPT2adjusted - PPT3adjusted) / (rhog * 0.1)


#plotting hydraulic gradient with critical hydraulic gradient

ax3.plot(times, smooth_data(hgradient12,1000),label = 'PPT1 - PPT2' )
ax3.plot(times, smooth_data(hgradient23,1000),label = 'PPT2 - PPT3' )
ax3.plot(times, smooth_data(hgradient13,1000),label = 'PPT1 - PPT3' )

icrit = 1.1113

#calcualting critical hydraulic gradient
Gs = 2.5 #This is from the particle design, it's slightly less and varies for each but close enough
icrit12 = (Gs-1) / (1 + np.mean(VoidRatio12[0:30]))
icrit23 = (Gs-1) / (1 + np.mean(VoidRatio23[0:30]))
icrit13 = (Gs-1) / (1 + np.mean(VoidRatio13[0:30]))

ax3.plot([0,times[len(times)-1]],[icrit12,icrit12],linestyle = '--',color = 'tab:blue', label = r'$i_{cr}$ PPT1-PPT2')
ax3.plot([0,times[len(times)-1]],[icrit23,icrit23],linestyle = '--',color = 'tab:orange', label = r'$i_{cr}$ PPT2-PPT3')
ax3.plot([0,times[len(times)-1]],[icrit13,icrit13],linestyle = '--',color = 'tab:green', label = r'$i_{cr}$ PPT1-PPT3')

ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Hydraulic Gradient')
ax3.legend()
ax3.grid(True)
ax3.set_xlim(0,plotendtime)



permeabilitysmoothed12 = flowrate / hgradient12 * 1000 #multiplied by 1000 due to geometry, this needs checking next term so don't use for report results
permeabilitysmoothed12 = np.array(smooth_data(permeabilitysmoothed12,1000)) #rolling average of 1000 frames taken so that the data plots better

permeabilitysmoothed23 = flowrate / hgradient23 * 1000 #multiplied by 1000 due to geometry, this needs checking next term so don't use for report results
permeabilitysmoothed23 = np.array(smooth_data(permeabilitysmoothed23,1000)) #rolling average of 1000 frames taken so that the data plots better

permeabilitysmoothed13 = flowrate / hgradient13 * 1000 #multiplied by 1000 due to geometry, this needs checking next term so don't use for report results
permeabilitysmoothed13 = np.array(smooth_data(permeabilitysmoothed13,1000)) #rolling average of 1000 frames taken so that the data plots better



ax4.plot(times,permeabilitysmoothed12, label = 'PP1 - PPT2')
ax4.plot(times,permeabilitysmoothed23, label = 'PP2 - PPT3')
ax4.plot(times,permeabilitysmoothed13, label = 'PP1 - PPT3')

ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Permeability')
ax4.grid(True)
ax4.legend()
ax4.set_xlim(0,plotendtime) 
ax4.set_ylim(0,max(permeabilitysmoothed12[int(len(permeabilitysmoothed12)*.25):int(len(permeabilitysmoothed12)*.75)])*1.2)




ax5.plot(void12times,VoidRatio12,label = "PPT1 - PPT2")
ax5.plot(void12times,VoidRatio23,label = "PPT2 - PPT3")
ax5.plot(void12times,VoidRatio13,label = "PPT1 - PPT3")

ax5.legend()

ax5.set_xlabel('Time (s)')
ax5.set_xlim(0,plotendtime) 
ax5.set_ylabel('Void Ratio')
ax5.grid(True)

ax6.plot(tort12times,Tortuosity12,label = "PPT1 - PPT2")
ax6.plot(tort12times,Tortuosity23,label = "PPT2 - PPT3")
#ax6.plot(tort12times,Tortuosity13,label = "PPT1 - PPT3")
ax6.set_xlim(0,plotendtime) 
ax6.set_xlabel('Time (s)')
ax6.set_ylabel('Tortuosity')
ax6.grid(True)
ax6.legend()


plt.tight_layout()
plt.show()

fig, (ax1,ax2,ax3 ) = plt.subplots(3,1)








#Plotting Permeability Against Tortuosity, between PPT1 and PPT3
permeabilitylist12 = []
permeabilitylist23 = []
permeabilitylist13 = []

for t in tort12times:
    
    closest_index = min(range(len(times)), key=lambda j: abs(times[j] - t))
    permeabilitylist12.append(permeabilitysmoothed12[closest_index])
    permeabilitylist23.append(permeabilitysmoothed23[closest_index])
    permeabilitylist13.append(permeabilitysmoothed13[closest_index])


Tort12 = np.array(Tortuosity12.copy())
Tort23 = np.array(Tortuosity23.copy())
#Tort13 = np.array(Tortuosity13.copy())
e12 = VoidRatio12.copy()
e23 = VoidRatio23.copy()
e13 = VoidRatio13.copy()

permcalc12 = 1/(Tort12 **2) * ( e12/ (1+e12))**3
permcalc23 = 1/(Tort23 **2 ) * (e23 / (1+e23)) **3
#permcalc13 = 1/(Tort13 **2 ) * (e13 / (1+e13)) **3

permcalc12_100 = np.mean(permcalc12[150:160])
permcalc23_100 = np.mean(permcalc23[150:160])
#permcalc13_100 = permcalc13[100]

permeability12_100 = np.mean(permeabilitylist12[150:160])
permeability23_100 = np.mean(permeabilitylist23[150:160])
permeability13_100 = np.mean(permeabilitylist13[150:160])
fig,ax1 = plt.subplots(figsize = (8,8))

ax1.scatter(permcalc12[160:450]/permcalc12_100,permeabilitylist12[160:450]/permeability12_100,label = "Between PPT1 and PPT2")
ax1.scatter(permcalc23[160:450] / permcalc23_100,permeabilitylist23[160:450]/permeability23_100,label = "Between PPT2 and PPT3")
#ax1.scatter(permcalc13[50:200] / permcalc13_100,permeabilitylist13[50:200]/permeability13_100,label = "Between PPT1 and PPT3")

#ax1.set_xlabel(r'$\frac{\frac{1}{\tau^2} (\frac{e}{1+e})^3}{\tau_0}$')

ax1.set_xlabel(r'Permeability calculated using Kozeny-Carman equation $\frac{k_{Carmen}}{k_{Carmen,0}}$',fontsize = 'large')
ax1.set_ylabel(r'Measured Permeability $\frac{k}{k_0}$',fontsize = 'large')

plt.title(r'Apr16/Test1  Mixture Particles t= 320 $\rightarrow$ t = 1000',fontsize = 'large')
ax1.set_xlim(0.8,2.5)
ax1.set_ylim(0.8,2.5)

ax1.plot([0.8,3],[0.8,3],linestyle = '--',color = 'red')



plt.grid()
plt.legend()

plt.show()

