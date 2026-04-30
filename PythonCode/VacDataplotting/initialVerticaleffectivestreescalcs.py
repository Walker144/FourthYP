import taufactor as tau
import numpy as np
import h5py
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
import time
import pandas as pd
import math



def verticaleffectivestressrun(vectorfile,pptheights,topvectorfile = ""):

    #we are assuming that the top vector folder fell above all the PPTs, so would be added to all the simgav's
    ellipticalparticleeffweight = 
    circularparticleeffweight = 


    if topvectorfile != "":
        topdf = pd.read_csv(topvectorfile)
        Alist,Blist,AngleList,CentreX,CentreY = topdf["Alist"],topdf["Blist"],topdf["AngleList"],topdf["CentreX"],topdf["CentreY"]
        for pindex in range(len(Alist)):
            if Alist[pindex] == Blist[pindex]



















if __name__ == "__main__":


    vectorfolder = "I:\Apr16\Test1\ImageVectors"
    imagedatafile = "I:\Apr16\Test1\Test\Image.csv"
    topimagevectorfolder = "I:\Apr16\Test1\ImageVectors"

    outputfile = "I:\Apr01\Test1\Effectivestresses.csv"

    pptheights = [10000,1929,0]



