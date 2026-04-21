import taufactor as tau
import numpy as np
import h5py
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
import time
from collections import deque
import matplotlib.patches
import locateparticlepins


imagefile  = "I:\Apr01\Test3\Test\Image_0000_0.tiff"
cutoff = 42
cropsizes = [1891,1144,4341,4736]
imagein = Image.open(imagefile)
imagein = imagein.crop(cropsizes)
imarray = np.array(imagein).astype(np.int32)
filterimarray = imarray.copy()
filterimarray[filterimarray < cutoff] = 1
filterimarray[filterimarray >= cutoff] = 0
filterimarray[filterimarray == 1] = 1

plt.imshow(filterimarray)
plt.show()


pincentres,averagearea,particlesizes = locateparticlepins.find_pins(filterimarray,[1000,2000],1,True)
print(particlesizes)
print(pincentres)

fig, (ax1,ax2,ax3) = plt.subplots(1,3,figsize=(15,5))

ax1.vlines(averagearea,0,3500,color = 'red',linestyles= '--')
ax2.imshow(filterimarray)


for i in range(len(pincentres)):
    ax1.scatter(particlesizes[i],pincentres[i][0],color= 'blue')
ax1.invert_yaxis()
ax1.set_ylabel('Y Coordinate')
ax1.set_xlabel('Pin size (pixels)')
ax3.imshow(imarray, cmap='gray')


plt.show()