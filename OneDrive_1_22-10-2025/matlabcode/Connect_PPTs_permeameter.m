clear all
% https://uk.mathworks.com/help/daq/examples.html?category=analog-data-acquisition&s_tid=CRUX_topnav

% Discover Analog Input Devices
d = daqlist("ni");
deviceInfo = d{1, "DeviceInfo"};

% Create a DataAcquisition and Add Analog Input Channels
dq = daq("ni");
dq.Rate = 10; % sampling rate (s)
addinput(dq, "Dev1", "ai0", "Voltage");
addinput(dq, "Dev1", "ai1", "Voltage");

% Plot Live Data
dq.ScansAvailableFcn = @(src,evt) plotDataAvailable(src, evt);

% Set ScansAvailableFcnCount
dq.ScansAvailableFcnCount = 1*dq.Rate;

% Start Background Acquisition
start(dq, "Duration", seconds(5))

% End of acquisition
fprintf("Acquisition stopped with %d scans acquired\n", dq.NumScansAcquired);

% % Record data for x seconds
% data = read(dq,2*dq.Rate);
% 
% % Plot data
% plot(data.Time, data.Variables);
% ylabel("Voltage (V)")

% Save data
% save('data.mat', 'data');

function plotDataAvailable(src, ~)
    [data, timestamps, ~] = read(src, src.ScansAvailableFcnCount, "OutputFormat", "Matrix");
    plot(timestamps, data);
end

function stopWhenEqualsOrExceedsOneV(src, ~)
    [data, timestamps, ~] = read(src, src.ScansAvailableFcnCount, "OutputFormat", "Matrix");
    if any(data >= 1.0)
        disp('Detected voltage exceeds 1V: stopping acquisition')
        % stop continuous acquisitions explicitly
        src.stop()
        plot(timestamps, data)
    else
        disp('Continuing to acquire data')
    end
end