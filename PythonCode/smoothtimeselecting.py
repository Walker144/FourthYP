import pandas
import numpy as np
import plottingfunctions
import matplotlib.pyplot as plt
import h5py

#data = pandas.read_excel('OneDrive_1_22-10-2025\FlowCalibrationData\watercalibration2dataexport.xlsx')


f  = 'OneDrive_1_22-10-2025\matlabcode\HTdatacollection\Feb23\Test2.mat'

matdata = h5py.File(f,'r+')
PPT1  = np.array(matdata['PPTdata'][1])
PPT2 = np.array(matdata['PPTdata'][0])
PPT3 = np.array(matdata['PPTdata'][2])

times = np.array(matdata['timestamps'][0])
FLOWdata = np.array(matdata['FLOWdata'])

FLOWcounter = np.concatenate([[0], np.cumsum(np.abs(np.diff(np.sign(FLOWdata - 2.5))) > 1)])
flowvolume = FLOWcounter * 3.87 * 10**(-7)



fs = int(1 / (times[100] - times[99]))
cutoff = 2  # cutoff frequency in Hz

PPT1 = plottingfunctions.butterfilter(PPT1,fs,cutoff)
#test 1 from 13/02/26 as not worth deleting but not really needed
#smoothtimes = [[1.8,11],[13,24],[26,55],[57,86],[88,118],[120,148],[150,178],[181,208],[211,240],[243,271],[274,303],[306,331],[337,366],[368,396],[400,419],[421,451],[454,482],[485,514],[517,547],[548,580],[700,756],[760,784],[790,822],[828,848],[851,865],[868,897],[900,928],[930,960],[964,995],[998,1027],[1030,1080],[1083,1107],[1110,1140],[1145,1178],[1185,1209],[1214,1239],[1246,1270],[1278,1303],[1310,1340]]
#test 2 16/02/26
#smoothtimes = [[0.8,12.4],[16,38],[40,71],[73,97],[108,138],[143,172],[176,206],[214,243],[247,277],[290,326],[330,363],[365,395],[398,428],[437,472],[477,508],[511,542],[576,606],[609,643],[764,778],[793,812],[835,861],[866,895],[898,940],[946,971],[981,1010],[1013,1040],[1046,1076],[1080,1103],[1120,1152],[1159,1186],[1190,1219],[1221,1261],[1263,1300],[1303,1331],[1334,1365],[1367,1395],[1398,1451]]

smoothtimes = [[1.7,29],[32,71],[74,114],[118,160],[163,208],[212,250],[253,293],[296,347],[350,390],[392,430],[433,473],[475,514],[520,561],[567,605],[610,646],[655,715],[720,756],[760,802],[807,853],[859,897],[903,966],[973,1027],[1034,1064],[1071,1107],[1114,1151],[1154,1194],[1198,1237],[1240,1282],[1285,1338],[1340,1383],[1385,1417],[1418,1457],[1459,1498],[1500,1545]]


fig = plt.figure()
plt.plot(times, PPT1)
timeswrite = ''



for sec in smoothtimes:
    start, end = sec
    avg_PPT1 = np.mean(PPT1[(times >= start) & (times <= end)])
    plt.plot([start,end], [avg_PPT1,avg_PPT1], color='red', linestyle='solid', linewidth=1)  # Plot average as a line for the time region
    timeswrite += f'{sec[0]},{sec[1]}\n'

timeswrite = timeswrite[:-1]
outfilename = f[:-4] + 'times.txt'

print(outfilename)

fout = open(outfilename,'w')
fout.write(timeswrite)
fout.close()

plt.xlabel('Time')
plt.ylabel('PPT1')
plt.title('PPT1 vs Time')
plt.show()