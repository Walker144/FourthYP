filetoimport = 'pptcalibration4.mat';

load(filetoimport)



exportfilename = extractBefore(filetoimport, strlength(filetoimport) - 3) + "dataexport.xlsx"

%FLOWcounter = [0;cumsum(abs(diff(sign(FLOWdata-2.5)))>1)];
PPTdata = data;




%PPT calibration Values

SF1 = 1000; %Convert input voltage to mV for equation
SF2 = 1; 

%PPTs(:,1) = (PPTdata(:,1) * SF1 * 0.6572121772 -5.901765352)*SF2;
%PPTs(:,2) = (PPTdata(:,2) * SF1 * 0.6575476561 -6.187523444)*SF2;
%PPTs(:,3) = (PPTdata(:,3) * SF1 * 0.6557315234 -4.36061463)*SF2;



T = table(timestamps,PPTdata(:,1),PPTdata(:,2),PPTdata(:,3));
writetable(T,exportfilename,'Sheet',1,'Range','A1')