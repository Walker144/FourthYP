filetoimport = 'fridaytest1.mat';

load(filetoimport)



exportfilename = extractBefore(filetoimport, strlength(filetoimport) - 3) + "dataexport.xlsx"

FLOWcounter = [0;cumsum(abs(diff(sign(FLOWdata-2.5)))>1)];


FLOWcalibration = 1;
FLOWcounterCalibrated = FLOWcounter * FLOWcalibration;





T = table(timestamps,FLOWcounterCalibrated,PPTdata(:,1),PPTdata(:,2),PPTdata(:,3));
writetable(T,exportfilename,'Sheet',1,'Range','A1')