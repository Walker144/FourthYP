import locateparticlepins
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
import pandas as pd

import os
os.system("")
cutoff = 40

#Apr1 Test 1
cropsizes = [1474,360,3950,4875]

#Apr1 Test 2,3,4
cropsizes = [1860,933,4300,4730]

#Apr1 Test 5
#cropsizes = [1570,590,4000,4800]

#Apr1 Test 6
#cropsizes = [1570,590,4000,4800]

#Mar31 Test 2
'''cropsizes = [1570,590,4000,4800]'''


imagefile = "H:\Apr01\Test2\Test\Image.csv"
vectorfolder = "H:\Apr01\Test2\ImageVectors2\\"

def filterimage(imarray,cutoff):
    filterimarray = imarray
    filterimarray[filterimarray < cutoff] = 1
    filterimarray[filterimarray >= cutoff] = 2
    filterimarray[filterimarray == 1] = 1

    return filterimarray
import sys

def loading_bar(percent, width=30,texttoshow=""):
    
    percent = max(0, min(100, percent))
    filled = int(width * percent / 100)

    green = "\033[92m"
    reset = "\033[0m"

    bar = green + "█" * filled + reset + "-" * (width - filled)

    sys.stdout.write(f"\r|{bar}| {percent:6.2f}% {texttoshow}")
    sys.stdout.flush()

    if percent == 100:
        print()


if __name__ == "__main__":
    Alist = []
    imagestoconvert = open(imagefile).read().split('\n')
    first = True
    countnum = 0
    print(len(imagestoconvert[1::2]))
    for imagestring in imagestoconvert[1::2]:
        countnum += 1

        imagestring = imagestring.split(';')
        imagename = imagestring[0][-17:-5:]
        imageToOpen = imagefile.split('.')[0] + imagename[-7::] + '.tiff'
        vectorfilename = vectorfolder + imagename + '.csv'
        csvlist = os.listdir(vectorfolder)

        
        if imagename + '.csv' in csvlist:
            print(imagename, "already processed")
            continue


        
        loading_bar((countnum/ len(imagestoconvert[1::2])*100),texttoshow = str(imagename) + " previous length " + str(len(Alist)))


      
        imagereal = Image.open(imageToOpen)

        imagearraycropped = np.array(imagereal.crop(cropsizes))
        filteredimage = filterimage(imagearraycropped.copy(),cutoff)

        if first:
            
            fig, (ax1, ax2,ax3) = plt.subplots(1, 3)
            fig.suptitle("Image Analysis, close after checking everything is correct")

            
            ax1.imshow(imagearraycropped,cmap = 'grey')
            ax2.hist(imagearraycropped.flatten(), bins=256, range=(0, 256), color='gray', edgecolor='black')
            ax3.imshow(filteredimage,cmap = 'grey')
            plt.show()
        pincentres,averagearea = locateparticlepins.find_pins(filteredimage)
        pinradiuspx = (averagearea / np.pi)**.5

        Alist,Blist,AngleList,CentreX,CentreY = locateparticlepins.create_shapes_from_pins(pincentres,averagearea,False,True)
        dfexport = pd.DataFrame({"Alist":Alist,"Blist":Blist,"AngleList":AngleList,"CentreX":CentreX,"CentreY":CentreY})
        dfexport.to_csv(vectorfolder + imagename + '.csv')


        if first:
            fig, (ax4,ax5) = plt.subplots(1,2)
            ax5.imshow(imagearraycropped,cmap = 'grey')
            ax4.imshow(filteredimage,cmap = 'grey')
            for piny,pinx in pincentres:
                ax4.add_patch(matplotlib.patches.Circle([pinx,piny],pinradiuspx,edgecolor = "red",fill = False))
            
            for i in range(len(Alist)):
                ax5.add_patch(matplotlib.patches.Ellipse([CentreX[i],CentreY[i]],Alist[i] *2,Blist[i]*2,angle = AngleList[i],edgecolor = "red",fill= False))
            fig.suptitle("Image Analysis, close after checking everything is correct")
            plt.show()
            first = False

        


           


            



