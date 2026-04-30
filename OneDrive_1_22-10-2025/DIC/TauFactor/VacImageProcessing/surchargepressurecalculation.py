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
import Taufactorrunfromvectors
import math

vectorfolder = "I:\Apr01\Test6\ImageVectors"
imagedatafile = "I:\Apr01\Test6\Test2\Image.csv"
outputfile = "I:\Apr01\Test6\VoidRatio23.csv"
XrangeWanted = [0,10000]
YrangeWanted = [450,2344]
#test 2,3,4 y split is 1870
#mar27 test 1, y 650, 2300
#mar27 Test 3 y 750,2400
#Apr01 Test 1 750 ,2434



def effsurcharge_pressure_run(vectorfolder,imagedatafile,outputfile,PPT3height,first=True):


    vectorfilelist = os.listdir(vectorfolder)
    imagedatasheet = open(imagedatafile).read().split('\n')[1::]

    if os.path.exists(outputfile):
        voiddataold = pd.read_csv(outputfile)
        voiddata = pd.DataFrame({"Imagename":voiddataold["Imagename"],"effSurchargePressure":voiddataold["effSurchargePressure"],"Timestamp":voiddataold["Timestamp"]})
        print("Existing File located")
    else:
        voiddata = pd.DataFrame(columns=["Imagename","effSurchargePressure","Timestamp"])
    



    imagecount = 0
    for vectorset in vectorfilelist:
        
        imagecount += 1
        #identify timestamp of image
        imagenum = vectorset[-10:-6]
        currentim = "Image_" +  imagenum
        if currentim in list(voiddata["Imagename"]):
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
        

        

        



        if first:
            taufactorlayersuc = Taufactorrunfromvectors.create_taufactor_set(Alist,Blist,AngleList,CentreX,CentreY,ellipsescalefactors=[.93,.99,1,1,.99,.94,.90,.87,.85,.84,.83,.82,.82],circlescalefactors=[.87,.97,1,1,.97,.9,.82,.76,.73,.70,.68,.67,.67])
               
            plt.imshow(taufactorlayersuc[1])
            plt.suptitle("Check it looks correct and then close")
            
            plt.hline(PPT3height,linestle = '--',color = 'red')
            plt.show()
            first = False




        ###caculate void ratio
        voidnumber = np.sum(taufactorlayers == 0)
        solidnumber = math.prod(taufactorlayers.shape) - voidnumber
       

       
        voidratio = voidnumber/ solidnumber

        voiddata.loc[len(voiddata)] = ["Image_" +  imagenum,voidratio,imagetimestamp]

        voiddata.to_csv(outputfile)
        
        Taufactorrunfromvectors.loading_bar(imagecount / len(vectorfilelist) * 100, texttoshow= f' Current image {imagenum} Void ratio {voidratio}')



if __name__ == "__main__":
    vectorfolder = "I:\Apr16\Test3\ImageVectors"
    imagedatafile = "I:\Apr16\Test3\Test\Image.csv"
    

    outputfile = "I:\Apr16\Test3\VoidRatio13test2.csv"
    XrangeWanted = [0,10000]
    YrangeWanted = [0,10000]
    #test 2,3,4 y split is 1870
    #mar27 test 1, y 650, 2300
    #mar27 Test 3 y 750,2400
    #Apr01 Test 1 750 ,2434
    void_ratio_run(vectorfolder,imagedatafile,outputfile,XrangeWanted,YrangeWanted,first= True)


    outputfile = "I:\Apr16\Test3\VoidRatio12test.csv"
    YrangeWanted = [1929,10000]
    void_ratio_run(vectorfolder,imagedatafile,outputfile,XrangeWanted,YrangeWanted,first= False)

    outputfile = "I:\Apr16\Test3\VoidRatio23test.csv"
    YrangeWanted = [0,1929]
    void_ratio_run(vectorfolder,imagedatafile,outputfile,XrangeWanted,YrangeWanted,first= False)
