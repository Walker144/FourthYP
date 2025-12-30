
import pandas
import numpy as np
import matplotlib.pyplot as plt



data = pandas.read_excel('OneDrive_1_22-10-2025\FlowCalibrationData\watercalibration5dataexport.xlsx')

times = data['timestamps']
print(data)
print(times)
totalvolume = data['FLOWcounterCalibrated']

print(max(totalvolume))