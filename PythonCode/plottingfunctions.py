from scipy.signal import butter, filtfilt

import numpy as np


def butterfilter(data,fs,cutoff):
    order = 4
    nyquist = fs / 2
    normal_cutoff = cutoff / nyquist

    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    filtered_signal = filtfilt(b,a,data)
    return filtered_signal