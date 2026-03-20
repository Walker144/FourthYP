import taufactor as tau
import numpy as np
import h5py
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
import pandas as pd
correlationoutputpath = "I:\Mar16\Test2\BottomHalfExport"
csvlist = os.listdir(correlationoutputpath)



fullmask = np.array(Image.open('OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\MatchIDanalysis\Fullmask.tif'))
plt.imshow(fullmask)


csv0 = pd.read_csv(correlationoutputpath + "\\" + csvlist[0])
plt.scatter(csv0["Coordinates.Image X [Pixel]"],csv0["Coordinates.Image Y [Pixel]"],marker ='o',s=5)


plt.show()