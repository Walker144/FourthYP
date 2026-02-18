filetoimport = 'valvecomparison2.mat';

load(filetoimport)



exportfilename = extractBefore(filetoimport, strlength(filetoimport) - 3) + "dataexport.xlsx"

FLOWcounter = [0;cumsum(abs(diff(sign(FLOWdata-2.5)))>1)];


FLOWcalibration = 1;
FLOWcounterCalibrated = FLOWcounter * FLOWcalibration;

PPT1 = PPTdata(:,1) ;
PPT2 = PPTdata(:,2); 
PPT3 = PPTdata(:,3);
timestamps;




T = table(timestamps,FLOWcounterCalibrated,PPT1,PPT2,PPT3);
%T(2:2:end, :) = []; % Delete alternate rows
writetable(T,exportfilename,'Sheet',1,'Range','A1')