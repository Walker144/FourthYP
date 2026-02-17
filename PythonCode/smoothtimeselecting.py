
import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
data = pandas.read_excel('OneDrive_1_22-10-2025\matlabcode\HTdata\Feb17\Test2dataexport.xlsx')
#data = pandas.read_excel('OneDrive_1_22-10-2025\FlowCalibrationData\watercalibration2dataexport.xlsx')

times = data['timestamps']


flowvolume = data['FLOWcounterCalibrated'] * 4.260 * 10**(-7)
PPT1 = data['PPT1']
PPT2 = data['PPT2']
PPT3 = data['PPT3']


fs = int(1 / (times[100] - times[99]))
cutoff = 2  # cutoff frequency in Hz

PPT1 = plottingfunctions.butterfilter(PPT1,fs,cutoff)
#test 1 from 13/02/26 as not worth deleting but not really needed
#smoothtimes = [[1.8,11],[13,24],[26,55],[57,86],[88,118],[120,148],[150,178],[181,208],[211,240],[243,271],[274,303],[306,331],[337,366],[368,396],[400,419],[421,451],[454,482],[485,514],[517,547],[548,580],[700,756],[760,784],[790,822],[828,848],[851,865],[868,897],[900,928],[930,960],[964,995],[998,1027],[1030,1080],[1083,1107],[1110,1140],[1145,1178],[1185,1209],[1214,1239],[1246,1270],[1278,1303],[1310,1340]]

smoothtimes = [[0.8,12.4],[16,38],[40,71],[73,97],[108,138],[143,172],[176,206],[214,243],[247,277],[290,326],[330,363],[365,395],[398,428],[437,472],[477,508],[511,542],[576,606],[609,643],[764,778],[793,812],[835,861],[866,895],[898,940],[946,971],[981,1010],[1013,1040],[1046,1076],[1080,1103],[1120,1152],[1159,1186],[1190,1219],[1221,1261],[1263,1300],[1303,1331],[1334,1365],[1367,1395],[1398,1451]]



fig = plt.figure()
plt.plot(times, PPT1)

for sec in smoothtimes:
    start, end = sec
    avg_PPT1 = np.mean(PPT1[(times >= start) & (times <= end)])
    plt.plot([start,end], [avg_PPT1,avg_PPT1], color='red', linestyle='solid', linewidth=1)  # Plot average as a line for the time region

plt.xlabel('Time')
plt.ylabel('PPT1')
plt.title('PPT1 vs Time')
plt.show()