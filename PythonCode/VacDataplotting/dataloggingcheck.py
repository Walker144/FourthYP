
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

f = r"C:\Users\andre\Documents\GitHub\FourthYP\FourthYP\OneDrive_1_22-10-2025\Matlabcode\Apr16Test1pre2.mat"


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
    print(convert_time_to_seconds(ppt_start_time))
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
FLOWdata = np.array(matdata['FLOWdata'])[0]

print(FLOWdata)

#Using data collected to convert PPT voltages to Pressure (KPa), and to convert the flow count into a flowrate
fs = int(1 / (times[100] - times[99])) 
cutoff = 2  # cutoff frequency in Hz
FLOWcounter = np.concatenate([[0], np.cumsum(np.abs(np.diff(np.sign(FLOWdata - 2.5))) > 1)])[1::nrate]
flowvolume = FLOWcounter * 3.87 * 10**(-7)
flowrate = np.gradient(flowvolume) * fs


flowrate = plottingfunctions.butterfilter(flowrate,fs,cutoff)

plt.plot(flowrate)

plt.show()