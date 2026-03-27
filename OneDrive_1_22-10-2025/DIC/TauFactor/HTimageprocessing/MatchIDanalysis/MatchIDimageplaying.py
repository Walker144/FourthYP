import taufactor as tau
import numpy as np
import h5py
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
import pandas as pd
import copy
from matplotlib.patches import Ellipse

imagepath = "i:\Mar16\Test2\SomeImages\Image_0000_0.tiff"

#left,top,right,bottom
cropsizes = [1397,384,3770,4744]

imarray = Image.open(imagepath).crop(cropsizes)



plt.imshow(imarray)

plt.show()
