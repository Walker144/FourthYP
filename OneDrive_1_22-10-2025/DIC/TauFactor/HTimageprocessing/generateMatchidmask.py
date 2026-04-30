import taufactor as tau
import numpy as np
import h5py
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import time
import newimageprep
import runtaufactor
import createTaufactorlayersellipse


cutoff = 70
#Crop Left top right bottom
croplist = [.24,.37,.62,.88]

'''imagecsvpath = "OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\Image_0000_0.tiff"
imagefile = open(imagecsvpath,'r').read().split('\n')
filepath  =imagecsvpath.split('.csv')[0]


im = imagefile[1].split(';')
part = im[0].split('Image')[1]
im[0] = filepath + part
file = im[0]
print(im[0])'''

file = "H:\Image_0000_0.tiff"
newimageprep.plot_hisogram(file)
im = newimageprep.binarise_image(file,cutoff,croplist)
newimageprep.display_image(im)

Image.fromarray(im.astype(np.uint8)).save("OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\processed_image.jpg")

import matlab.engine
eng= matlab.engine.start_matlab()
eng.cd('OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing')
eng.eval("run('Taufactor_Stripped.m')", nargout=0)
fmat = 'OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\Tauimagevec.mat'
matdata = h5py.File(fmat,'r+')

imagesize = np.array(matdata["imsize"])
Centersv = np.array(matdata["Centersv"])[0]
Centersu = np.array(matdata["Centersu"])[0]
Areas = np.array(matdata["Areas"])[0]
Contactlist = np.array(matdata["CN"])[0]
L = np.array(matdata["L"])




print(Areas)
slices,dataexport = createTaufactorlayersellipse.create_taufactor_arrays(imagesize,Centersv,Centersu,Areas,Contactlist,L,True,sizecutoff=[10,6000])
print(dataexport)
dataexport.to_csv("OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\MatchIDanalysis\InitalElipses.csv")


smallmask = slices[1]
imageheight = 5120
imagewidth = 5120

maskheight, maskwidth = smallmask.shape
lefttrim, toptrim = int(imagewidth * croplist[0]), int(imageheight * croplist[1])

open("OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\MatchIDanalysis\Matchidmasktrinsizes.txt",'w').write(f'{lefttrim},{toptrim}')

print(lefttrim,toptrim)
print(maskwidth,maskheight)
rawimage = Image.open(file)

fullmask = np.zeros((5210,5210))
fullmask[toptrim:toptrim + maskheight, lefttrim:lefttrim + maskwidth] = smallmask
print(maskheight,maskwidth,imageheight,imagewidth)

# Convert rawimage to array and overlay the mask
rawimage_array = np.array(rawimage)

# Create a figure with both images

Image.fromarray(fullmask.astype(np.uint8)).save("OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\Fullmask.tif")

# Show image with mask overlay
plt.imshow(np.array(Image.open(file)), cmap='gray')
plt.imshow(fullmask, alpha=0.3)


plt.tight_layout()
plt.show()

