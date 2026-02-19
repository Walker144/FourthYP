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



#################################################################
#####    INPUT FILE, INITIAL MASS, FINAL MASS               #####
#################################################################



#18th Feb calibration 1
matdata = h5py.File('OneDrive_1_22-10-2025\matlabcode\HTdatacollection\Feb18\Flowcalibration1.mat','r+')
initialMass = 197.06 #grams
finalMass =  2102.02 #grams

#18th Feb calibration 2
matdata = h5py.File('OneDrive_1_22-10-2025\matlabcode\HTdatacollection\Feb18\Flowcalibration2.mat','r+')
initialMass = 197.06 #grams
finalMass =  2318.87 #grams

#19th Feb calibration 3
matdata = h5py.File('OneDrive_1_22-10-2025\matlabcode\HTdatacollection\Feb19\Flowcalibration3.mat','r+')
initialMass = 195 #grams
finalMass =  3325 #grams



#19th Feb Calibration 4

matdata = h5py.File('OneDrive_1_22-10-2025\matlabcode\HTdatacollection\Feb19\Flowcalibration4.mat','r+')
initialMass = 195 #grams
finalMass =  4255 #grams

#19th Feb Calibration 5

matdata = h5py.File('OneDrive_1_22-10-2025\matlabcode\HTdatacollection\Feb19\Flowcalibration5.mat','r+')
initialMass = 195 #grams
finalMass =  3490 #grams


#19th Feb Calibration 6

matdata = h5py.File('OneDrive_1_22-10-2025\matlabcode\HTdatacollection\Feb19\Flowcalibration6.mat','r+')
initialMass = 195 #grams
finalMass =  3805 #grams

#19th Feb Calibration 7

matdata = h5py.File('OneDrive_1_22-10-2025\matlabcode\HTdatacollection\Feb19\Flowcalibration7.mat','r+')
initialMass = 195 #grams
finalMass =  4715 #grams

#finally 3 results that actually match each other (happy to put the 2% difference to timings of removing the water etc). 
# #Trying to work out the exact time of the start of the program is probably the source of a lot of the errors when doing calibration)








times = np.array(matdata['timestamps'][0])
FLOWdata = np.array(matdata['FLOWdata'])
FLOWvolume = np.concatenate([[0], np.cumsum(np.abs(np.diff(np.sign(FLOWdata - 2.5))) > 1)])


#converting voltages and counts into volumes and pressures
fs = int(1 / (times[100] - times[99]))
print(fs)
cutoff = 2  # cutoff frequency in Hz



#calculate flowrate based off flowvolume, must be multiplied to get from gradient / frame to gradient/ s 
flowrate = np.gradient(FLOWvolume) * fs
flowrate = plottingfunctions.butterfilter(flowrate,fs,cutoff)
flowrateraw = np.array(flowrate)

#Calculating max counts and therefore volume per count

print(finalMass,initialMass)
maxcounts = max(FLOWvolume)
countvolume = (finalMass - initialMass) / maxcounts /1000000

print(countvolume)


fig, (ax1,ax2) = plt.subplots(2, 1, figsize=(10, 8))

#plotting total counts against time
ax1.plot(times,FLOWvolume)
ax1.set_title('Flow counts against time')
ax1.set_ylabel('Flow counts')
ax1.set_xlabel('Time (s)')


#plotting flowrate against time
ax2.plot(times,flowrate)
ax2.set_title('Flow rate against time\nEnsure that this does not have a massive drop during loading to ensure there are not issues with maxing counts')
ax2.set_ylabel('Flow rate')
ax2.set_xlabel('Time (s)')


plt.tight_layout()
plt.show()