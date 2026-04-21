
import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py
import pandas as pd
import os




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
    



def package_experimentset_to_csv(folder,cutoff,DataOutRate,matstarttime):
    filestocompact = os.listdir(folder)
    for f in filestocompact:
        if f[-4::] == ".mat":
            matdata = h5py.File(folder + r'\\' + f,'r+')
            PPT1  = np.array(matdata['PPTdata'][1])
            PPT2 = np.array(matdata['PPTdata'][0])
            PPT3 = np.array(matdata['PPTdata'][2])
            PPTtimes = np.array(matdata['timestamps'][0])
            FLOWdata = np.array(matdata['FLOWdata'])
            FLOWcounter = np.concatenate([[0], np.cumsum(np.abs(np.diff(np.sign(FLOWdata - 2.5))) > 1)])
            flowvolume = FLOWcounter * 3.87 * 10**(-7)
            fs = int(1/(PPTtimes[100] - PPTtimes[99]))
            flowrate = np.gradient(flowvolume) * fs
            flowrate = plottingfunctions.butterfilter(flowrate,fs,cutoff)

            


            PPT1 = PPT1 * 608.5052 - 4.2710
            PPT2 = PPT2 * 613.0834 - 4.998270
            PPT3 = PPT3 * 611.7754 - 3.2881
            PPT1 = plottingfunctions.butterfilter(PPT1,fs,cutoff)
            PPT2 = plottingfunctions.butterfilter(PPT2,fs,cutoff)
            PPT3 = plottingfunctions.butterfilter(PPT3,fs,cutoff)
            plt.plot(PPTtimes,PPT1)
            plt.show()

            timestosmooth = input('Enter times to smooth at the times between changes split by commas (normally the first 5 intevals):')
            smoothtimes = timestosmooth.split(',')
            timestosmoothlist = []
            print(smoothtimes)
            for timeindex in range(len(smoothtimes[0:-1:])):
                timestosmoothlist.append([int(smoothtimes[timeindex]),int(smoothtimes[timeindex+1])])
            PPT1,PPT2,PPT3 = plottingfunctions.replacewithconstants(PPT1,PPTtimes,timestosmoothlist),plottingfunctions.replacewithconstants(PPT2,PPTtimes,timestosmoothlist),plottingfunctions.replacewithconstants(PPT3,PPTtimes,timestosmoothlist)

            timelist = PPTtimes.tolist()
            startindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - int(smoothtimes[0])))
            endindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - int(smoothtimes[1])))
            PPT1base = np.average(PPT1[startindex:endindex])
            PPT2base = np.average(PPT2[startindex:endindex])
            PPT3base = np.average(PPT3[startindex:endindex])


            PPT1a,PPT2a,PPT3a = PPT1 - PPT1base, PPT2-PPT2base, PPT3 - PPT3base
            print(fs)
            pptdatastorerate = int(fs / DataOutRate)
            outputdf = pandas.DataFrame({"time":PPTtimes[::pptdatastorerate],"PPT1 adjusted":PPT1a[::pptdatastorerate],"PPT2 adjusted":PPT2a[::pptdatastorerate],"PPT3 adjusted":PPT3a[::pptdatastorerate],"flowrate":flowrate[::pptdatastorerate]})
            
    f = pd.read_csv(folder + r'\\' + "Tortuosity12.csv")
    imagetimes,Tort12 = convert_datafile_to_relative_time(f,matstarttime,"Tortuosity")
    
    closest_imagetime_indices = [imagetimes.index(min(imagetimes, key=lambda x: abs(x - t))) for t in outputdf["time"]]
    Torttodf = []
    for i in closest_imagetime_indices:
        Torttodf.append(Tort12.iloc[i])
    outputdf.insert(len(outputdf.columns),"Tortuosity12",Torttodf)
 
    
    filenames = ['Tortuosity23.csv','Tortuosity13.csv','VoidRatio12.csv','VoidRatio23.csv','VoidRatio13.csv','CoordinationNumbers12.csv','CoordinationNumbers23.csv','CoordinationNumbers13.csv']
    datatocollate  = [["Tortuosity"],["Tortuosity"],["VoidRatio"],["VoidRatio"],["VoidRatio"],["CoordinationNumber","MechanicalCoordination"],["CoordinationNumber","MechanicalCoordination"],["CoordinationNumber","MechanicalCoordination"]]
    headernames = [["Tortuosity23"],["Tortuosity13"],["VoidRatio12"],["VoidRatio23"],["VoidRatio13"],["CoordinationNumber12","MechanicalCoordination12"],["CoordinationNumber23","MechanicalCoordination23"],["CoordinationNumber13","MechanicalCoordination13"]]

    j = 0
    for filename in filenames:
        if filename in filestocompact:
            print(filename)
            f = pd.read_csv(folder + r'\\' + filename)
            k =0
            for collumn in datatocollate[j]:
                datacol = f[collumn]
                dfdata = []
                for i in closest_imagetime_indices:
                    dfdata.append(datacol.iloc[i])
                outputdf.insert(len(outputdf.columns),headernames[j][k],dfdata)



                k += 1
        j += 1

    outputdf.to_csv(folder + '\\TestCombineddata.csv')















if __name__ == "__main__":
    package_experimentset_to_csv("I:\Mar27\Test3",2,100,"12:28:49")