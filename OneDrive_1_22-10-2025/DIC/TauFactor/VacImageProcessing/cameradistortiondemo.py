import numpy as np
import matplotlib.pyplot as plt
import pandas
from PIL import Image

backgroundimage = "I:\Mar16\Calibration\Image_0000_0.tiff"

calibrationdata = open("I:\Mar16\Calibration\calibration.caldat").read().split('\n')
print(calibrationdata)

Fx,Fy,k1,k2,k3 = float(calibrationdata[0].split(';')[1]),float(calibrationdata[1].split(';')[1]),float(calibrationdata[3].split(';')[1]),float(calibrationdata[4].split(';')[1]),float(calibrationdata[5].split(';')[1])


imarray = np.array(Image.open(backgroundimage))

distortionarray = np.zeros_like(imarray, dtype=float)
width = len(distortionarray[0]) / 2
height = len(distortionarray) / 2
print(width,height)
print(Fx,Fy)

for x in range(len(distortionarray[0])):
    for y in range(len(distortionarray)):

        r = (((x - width) / Fx) ** 2  + ((y - height) / Fy) ** 2 ) **  .5
        distortionarray[y][x] = (k1 * r **3 + k2 * r ** 5 + k3 * r **7) * 100
print(distortionarray[100][100])
plt.imshow(imarray,cmap = 'gray')

plt.imshow(distortionarray, cmap = 'jet_r', alpha = 0.3)
plt.colorbar(label='Distortion (%)')
plt.show()
