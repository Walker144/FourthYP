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





def find_continuity_shape(imarray,seedpoint,value=1):
    h,w = imarray.shape    
    seed = tuple(seedpoint)
    queue = deque([seedpoint])
    visited = {seed}
    locations = []

    #check if value is correct, arguably this could be done by setting value to whatever is in that cell
    if imarray[seed] != value:
        return []
    
    directions = [(-1,0),(1,0),(0,-1),(0,1)]
    while queue:
        r,c = queue.popleft()
        if imarray[r,c] != value:
            continue

        locations.append((r,c))    
        for dr,dc in directions:
            nr,nc = r+dr,c+dc
            if 0 <= nr < h and 0 <= nc < w:
                if (nr,nc) not in visited:
                    visited.add((nr,nc))
                    queue.append((nr,nc))
    
    return locations


def find_pins(imarray,pinsize = [1000,2000],value=1,returnpinsizes = False):
    #This function has 2 parts, identifying the size and position of pins, and converting them to a vector form 

    particleindex = 0
    particlepoints = {}
    particlesizes = []
    
    placestocheck = (imarray == value)
    while placestocheck.any():
        
        seed= np.argwhere(placestocheck)[0]
  
        seedpoint = (seed[0],seed[1])
        pointsinparticle = find_continuity_shape(imarray,seedpoint)

        particlepoints[particleindex] = pointsinparticle
        particlesizes.append(len(pointsinparticle))

        
        particleindex += 1


        for r,c in pointsinparticle:
            placestocheck[r,c] = False
    
    #converting pins to vectors
    #This makes it the last particle that has an index in the list
    maxparticleindex = particleindex - 1

    pincentres = []
    totalarea = 0
    numberofpins = 0

    

    for currentpin in range(maxparticleindex+1):
        
        if pinsize[0] < particlesizes[currentpin] < pinsize[1]:
            ycoords,xcoords = [],[]
            for pixely,pixelx in particlepoints[currentpin]:
                ycoords.append(pixely)
                xcoords.append(pixelx)
            ycentre,xcentre = np.mean(ycoords),np.mean(xcoords)
            pincentres.append([ycentre,xcentre])
            numberofpins += 1
            totalarea += particlesizes[currentpin]
        
    if numberofpins == 0:
        if returnpinsizes:
            return [],0,[]
        else:
            return [],0
        

    averagearea = totalarea / numberofpins
    if returnpinsizes:
        return pincentres,averagearea,particlesizes

    return pincentres, averagearea

def create_shapes_from_pins(pincentres,averagearea,contains_circles,contains_Elipses):
    pinradiuspx = (averagearea / np.pi)**.5
    
    #These are hard-coded for the particles we are using
    circleradiusscale = 7.5/3
    ellipsepindistancescale = 4.1/1.5
    ellipsemajoraxisscale = 14/3
    ellipseminoraxisscale = 7.5/3

    circleradius = pinradiuspx * circleradiusscale
    ellipsepindistance = ellipsepindistancescale * pinradiuspx
    ellipsemajoraxis = pinradiuspx * ellipsemajoraxisscale
    ellipseminoraxis = pinradiuspx * ellipseminoraxisscale

    Alist,Blist,AngleList,CentreX,CentreY = [],[],[],[],[]


    if contains_circles and not contains_Elipses:
        for y,x in pincentres:
            Alist.append(circleradius)
            Blist.append(circleradius)
            AngleList.append(0)
            CentreX.append(x)
            CentreY.append(y)

    else:
        pinindexesused = []
        for i in range(len(pincentres)):
            if i in pinindexesused:
                continue
            
            y,x = pincentres[i]
            distances = []
            for j in range(len(pincentres)):
                y2,x2 = pincentres[j]
                distance = ((y-y2) **2 + (x-x2) **2)**.5
                distances.append(distance)

            sorteddistances = sorted(distances)
            if len(sorteddistances) > 1:
                mindistance = sorteddistances[1]
            else:
                mindistance = 1000000000000

            if mindistance < ellipsepindistance*1.2:

                secondpinindex = distances.index(mindistance)
                pinindexesused.append(secondpinindex)
                pinindexesused.append(i)
                y2,x2 = pincentres[secondpinindex]
                anglevector = [y2-y,x2-x]
                angle = np.arccos(anglevector[1] / (anglevector[0] **2 + anglevector[1] **2)**.5) * 180 / np.pi
                Alist.append(ellipsemajoraxis)
                Blist.append(ellipseminoraxis)
                AngleList.append(angle)
                CentreX.append((x2 + x )/ 2)
                CentreY.append((y2  + y)/2)
            else:
                Alist.append(circleradius)
                Blist.append(circleradius)
                AngleList.append(0)
                CentreX.append(x)
                CentreY.append(y)


    


    


    return Alist,Blist,AngleList,CentreX,CentreY










if __name__ == "__main__":
    imagefile  = "H:\Apr01\Test6\Test\Image_0000_0.tiff"
    cutoff = 42
    cropsizes = [1591,1144,4041,4736]
    imagein = Image.open(imagefile)
    imagein = imagein.crop(cropsizes)
    imarray = np.array(imagein).astype(np.int32)
    filterimarray = imarray.copy()
    filterimarray[filterimarray < cutoff] = 1
    filterimarray[filterimarray >= cutoff] = -2
    filterimarray[filterimarray == 1] = -1



    plt.hist(imarray.flatten(), bins=256, range=(0, 256), color='gray', edgecolor='black')
    plt.show()
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(imarray)
    ax2.imshow(filterimarray)
    plt.show()

    start = time.time()

    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.imshow(imarray)
    ax2.imshow(filterimarray)

    pincentres,averagearea = find_pins(filterimarray)
    pinradiuspx = (averagearea / np.pi)**.5


    for piny,pinx in pincentres:
        ax2.add_patch(matplotlib.patches.Circle([pinx,piny],pinradiuspx,edgecolor = "red",fill = False))

    Alist,Blist,AngleList,CentreX,CentreY = create_shapes_from_pins(pincentres,averagearea,False,True)

    for i in range(len(Alist)):
        ax1.add_patch(matplotlib.patches.Ellipse([CentreX[i],CentreY[i]],Alist[i] *2,Blist[i]*2,angle = AngleList[i],edgecolor = "red",fill= False))
    end = time.time()
    print(f'execution time: {end - start:.4f} seconds')

    plt.show()























