from scipy.signal import butter, filtfilt

import numpy as np


def butterfilter(data,fs,cutoff):
    order = 4
    nyquist = fs / 2
    normal_cutoff = cutoff / nyquist

    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_signal = filtfilt(b,a,data)
    return filtered_signal

def butterworthparts(data,fs,cutoff,times,regions):
    basesignal = butterfilter(data,fs,cutoff)

    for setoftimes in regions:
        startindex = min(range(len(times)), key=lambda i: abs(times[i] - setoftimes[0]))
        endindex = min(range(len(times)), key=lambda i: abs(times[i] - setoftimes[1]))
        part = data[startindex:endindex]
        basesignal[startindex:endindex] = butterfilter(part,fs  ,cutoff/ 2)
    return basesignal
        




def replacewithconstants(data,timelist,regions):
    data = np.copy(data)
    for setoftimes in regions:
        startindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - setoftimes[0]))
        endindex = min(range(len(timelist)), key=lambda i: abs(timelist[i] - setoftimes[1]))
        part = data[startindex:endindex]
        average = np.average(part)
        data[startindex:endindex] = np.ones(len(part)) * average
    return data