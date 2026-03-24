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
correlationoutputpath = "I:\Mar16\Test2\BottomHalfExport"
csvlist = os.listdir(correlationoutputpath)



fullmask = np.array(Image.open('OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\MatchIDanalysis\Fullmask.tif'))
plt.imshow(fullmask)


csv0 = pd.read_csv(correlationoutputpath + "\\" + csvlist[0])



initialpointsX = csv0["Coordinates.Image X [Pixel]"]
initialpointsY = csv0["Coordinates.Image Y [Pixel]"]


initialElipseData = pd.read_csv("OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\MatchIDanalysis\InitalElipses.csv")

initialXCentres = np.array(initialElipseData["CentreX"]) + int(open("OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\MatchIDanalysis\Matchidmasktrinsizes.txt").read().split(',')[0])
initialYCentres = np.array(initialElipseData["CentreY"]) + int(open("OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\MatchIDanalysis\Matchidmasktrinsizes.txt").read().split(',')[1])
initialA = np.array(initialElipseData["Alist"])
initialB = np.array(initialElipseData["Blist"])
initialangle = np.array(initialElipseData["AngleList"])
initialanglerad = (initialangle.copy()) * np.pi/ 180
elipseindexes = {}
elipseindexes[-1] = []

for i in range(len(initialA)):
    elipseindexes[i] = []

for pointindex in range(len(initialpointsX)):
    x,y = initialpointsX[pointindex],initialpointsY[pointindex]
    Distance = ((x-initialXCentres)*np.cos(initialanglerad) + (y-initialYCentres) * np.sin(initialanglerad))**2 / (initialA **2) + ((x-initialXCentres)*np.sin(initialanglerad) - (y-initialYCentres) * np.cos(initialanglerad))**2 / (initialB **2)
    if np.min(Distance) > 1:
        
        elipseindexes[-1].append(pointindex)
    else:
        elipseindexes[np.argmin(Distance)].append(pointindex)


particleIDs = np.array(list(elipseindexes.keys())[1:])





def calculate_movement_vectors(particleID,currentdataframe,elipseindexes=elipseindexes,initialpointsX=initialpointsX,initialpointsY=initialpointsY):
    pointslist = elipseindexes[particleID]
    particleXin, particleYin = np.array(initialpointsX[pointslist]), np.array(initialpointsY[pointslist])

    Xdisplacement, Ydisplacement = np.array(currentdataframe["disp.Horizontal Displacement U [Pixel]"][pointslist]),np.array(currentdataframe["disp.Vertical Displacement V [Pixel]"][pointslist])
    

    trackablepointslist = []
    particleXP, particleYP = [],[]
    particleXQ,particleYQ = [],[]

    for i in range(len(Xdisplacement)):
     
        if not np.isnan(Xdisplacement[i]):
            trackablepointslist.append(pointslist[i])
            particleXP.append(particleXin[i])
            particleYP.append(particleYin[i])
            particleXQ.append(particleXin[i] + Xdisplacement[i])
            particleYQ.append(particleYin[i] + Ydisplacement[i])
        
    if particleXP == []:
        return -1,-1
    particleXP, particleYP, particleXQ, particleYQ = np.array(particleXP), np.array(particleYP), np.array(particleXQ), np.array(particleYQ)


    Pbar = [sum(particleXP)/len(particleXP),sum(particleYP)/len(particleYP)]
    Qbar = [sum(particleXQ)/len(particleXQ),sum(particleYQ)/len(particleYQ)]

    particleXPlocal, particleYPlocal, particleXQlocal, particleYQlocal = particleXP - Pbar[0],  particleYP - Pbar[1], particleXQ - Qbar[0], particleYQ - Qbar[1]

    Qmatrix = np.matrix([particleXQlocal,particleYQlocal])
    Pmatrix = np.matrix([particleXPlocal,particleYPlocal])

    #RotationMatrix = Qmatrix * Pmatrix.transpose() * (Pmatrix * Pmatrix.transpose()) **-1

    H = Qmatrix * Pmatrix.transpose() * (Pmatrix * Pmatrix.transpose()) **-1
    U,S,Vt = np.linalg.svd(H)
    RotationMatrix = U * Vt


    print(S)
    if max(abs(S-1)) > 0.45:
        print(particleID)
        

    translationVector = np.matrix(Qbar).transpose() - RotationMatrix * np.matrix(Pbar).transpose()

    return RotationMatrix,translationVector


csvtolookat = pd.read_csv(correlationoutputpath + "\\" + csvlist[800])

finalXpos, finalYpos = np.array(csvtolookat["disp.Horizontal Displacement U [Pixel]"]) + initialpointsX,np.array(csvtolookat["disp.Vertical Displacement V [Pixel]"] + initialpointsY)
  
failed = 0
particleIDs = [394]

for particleID in particleIDs:
    if elipseindexes[particleID] != []:


        RotationMatrix,translationVector = calculate_movement_vectors(particleID,csvtolookat)
        try:
            if RotationMatrix == -1:
                failed += 1
        except:
            newparticlecoords = RotationMatrix * np.matrix([initialXCentres[particleID],initialYCentres[particleID]]).transpose() + translationVector
            newrotation = initialanglerad[particleID] + np.arctan2(RotationMatrix[1,0],RotationMatrix[0,0])
            plt.gca().add_patch(Ellipse(xy=newparticlecoords,width = initialA[particleID]*2,height = initialB[particleID]*2,angle=newrotation * 180/ np.pi,edgecolor="black",linewidth=2))
            plt.scatter(finalXpos[elipseindexes[particleID]],finalYpos[elipseindexes[particleID]],color = 'red')
    else:
        pass
#TO draw an elipse: plt.gca().add_patch(Ellipse(xy=newparticlecoords,width = initialA[particleID]*2,height = initialB[particleID]*2,angle=newrotation * 180/ np.pi,color = "red"))

print( failed)



  








plt.show()

