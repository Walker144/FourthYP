import taufactor as tau
import numpy as np
import h5py
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
import time
import pandas as pd
import runtaufactor 





def draw_taufactor_layer(Alist,Blist,AngleList,CentreX,CentreY,size ,ScaleFactor= [1,1]):
    taulayer = np.zeros(shape =size)
    
    for i in range(len(Alist)):
        if Alist[i] != Blist[i]:
            cv2.ellipse(taulayer,(int(CentreX[i]),int(CentreY[i])),(int(Alist[i] * ScaleFactor[0]),int(Blist[i] * ScaleFactor[0])),AngleList[i],0,360,color = 255, thickness = -1)
        else:
            cv2.ellipse(taulayer,(int(CentreX[i]),int(CentreY[i])),(int(Alist[i] * ScaleFactor[1]),int(Blist[i] * ScaleFactor[1])),0,0,360,color = 255, thickness = -1)
    return taulayer
    
def create_taufactor_set(Alist,Blist,AngleList,CentreX,CentreY,ellipsescalefactors = [1],circlescalefactors = [1],size = False):
    if not size:
        size  = (int(max(CentreY)),int(max(CentreX)))
        numberoflayers = len(ellipsescalefactors)
        tauset = np.zeros(shape = (numberoflayers,size[0],size[1])).astype(np.int8)
        for i in range(numberoflayers):
            tauset[i] = draw_taufactor_layer(Alist,Blist,AngleList,CentreX,CentreY,size,[ellipsescalefactors[i],circlescalefactors[i]])
    return tauset




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





def run_file_set(vectorfolder,imagedatafile,outputfile,XrangeWanted,YrangeWanted,isfirst = True):
    vectorfilelist = os.listdir(vectorfolder)
    first = isfirst
    imagedatasheet = open(imagedatafile).read().split('\n')[1::]

    if os.path.exists(outputfile):
        tortdataold = pd.read_csv(outputfile)
        tortdata = pd.DataFrame({"Imagename":tortdataold["Imagename"],"Tortuosity":tortdataold["Tortuosity"],"Deff":tortdataold["Deff"],"Timestamp":tortdataold["Timestamp"]})
        print("Existing File located")
    else:
        tortdata = pd.DataFrame(columns=["Imagename","Tortuosity","Deff","Timestamp"])
    


    
    imagecount = 0
    for vectorset in vectorfilelist:
        
        imagecount += 1
        #identify timestamp of image
        imagenum = vectorset[-10:-6]
        currentim = "Image_" +  imagenum
        if currentim in list(tortdata["Imagename"]):
            print("Image",imagenum,"Already processed")
            continue

        for imagemetadata in imagedatasheet:
            imageindex = imagemetadata.split(';')[0][-11:-7]
            if imagenum == imageindex:
                imagetimestamp = imagemetadata.split(';')[1]
                break
        imagedata = pd.read_csv(vectorfolder + '\\' + vectorset)
        
        Alist,Blist,AngleList,CentreX,CentreY = np.array(imagedata["Alist"]),np.array(imagedata["Blist"]),np.array(imagedata["AngleList"]),np.array(imagedata["CentreX"]),np.array(imagedata["CentreY"])
        size  = (int(max(CentreY) + Alist[0]),int(max(CentreX)+ Alist[0]))
        

        

        taufactorlayersuc = create_taufactor_set(Alist,Blist,AngleList,CentreX,CentreY,ellipsescalefactors=[.93,.99,1,1,.99,.94,.90,.87,.85,.84,.83,.82,.82],circlescalefactors=[.87,.97,1,1,.97,.9,.82,.76,.73,.70,.68,.67,.67])
        taufactorlayers = taufactorlayersuc[:,max(0,YrangeWanted[0]):min(size[0],YrangeWanted[1]),max(0,XrangeWanted[0]):min(size[1],XrangeWanted[1])]



        if first:
            fig, (ax1,ax2) = plt.subplots(1,2)
            ax1.imshow(taufactorlayersuc[1])
            plt.suptitle("Check it looks correct and then close")
            ax2.imshow(taufactorlayers[1])
            plt.show()
            first = False




        Tortuosity, Deff = runtaufactor.run_tau_factor(taufactorlayers)
        tortdata.loc[len(tortdata)] = ["Image_" +  imagenum,Tortuosity[0],Deff[0],imagetimestamp]
        tortdata.to_csv(outputfile)

        loading_bar(imagecount / len(vectorfilelist) * 100, texttoshow= f' Current image {imagenum} Tortuosity {Tortuosity}')
        




vectorfolder = "I:\Mar31\Test1\ImageVectors"
imagedatafile = "I:\Mar31\Test1\Test\Image.csv"
outputfile = "I:\Mar31\Test1\Tortuosity12.csv"

XrangeWanted = [0,10000]
YrangeWanted = [1929,10000]
#apr1Test 6 450, 2344
#Mar27Test1 PPT2 location 500
#Apr1Test3 PP2 location 1870

if __name__ == "__main__":
    outputfile = "I:\Mar31\Test1\Tortuosity23.csv"
    YrangeWanted = [770,2550]
    run_file_set(vectorfolder,imagedatafile,outputfile,XrangeWanted,YrangeWanted)

    outputfile = "I:\Mar31\Test1\Tortuosity12.csv"
    YrangeWanted = [2550,10000]
    run_file_set(vectorfolder,imagedatafile,outputfile,XrangeWanted,YrangeWanted,isfirst=False)

    outputfile = "I:\Mar31\Test1\Tortuosity13.csv"
    YrangeWanted = [770,10000]
    run_file_set(vectorfolder,imagedatafile,outputfile,XrangeWanted,YrangeWanted,isfirst= False)






        