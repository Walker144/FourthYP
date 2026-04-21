import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import matplotlib.colors as mcolors
import pandas as pd
import os 
import cv2

#multiplier for distance between particles for contact
DISTANCETHEASHOLD = 1.1


def give_ellipse_point(a,b,Angle,h,k,t):
    angleRad = Angle *  np.pi / 180
    return h + a* np.cos(t) * np.cos(angleRad) - b * np.sin(t) * np.sin(angleRad), k + a * np.cos(t) * np.sin(angleRad) + b * np.sin(t) * np.cos(angleRad)

def check_if_point_in_ellipse(a,b,Angle,h,k,x,y):
    theta = Angle * np.pi / 180
    distance = ((( x-h) * np.cos(theta) + (y-k) * np.sin(theta)) ** 2 / (a**2)) + (((x-h) * np.sin(theta) - (y-k) * np.cos(theta))**2 / (b**2))
    if distance < 1:
        return True
    else:
        return False
    

def drawcontactsonarray(contactdic,vectorfilepath):
    imagedata = pd.read_csv(vectorfilepath)
    Alist,Blist,AngleList,CentreX,CentreY = np.array(imagedata["Alist"]),np.array(imagedata["Blist"]),np.array(imagedata["AngleList"]),np.array(imagedata["CentreX"]),np.array(imagedata["CentreY"])
    size  = (int(max(CentreY) + Alist[0]),int(max(CentreX)+ Alist[0]))
    imarray = np.zeros(shape=size)
    imarray2 = np.zeros(shape=size)



    for i in list(contactdic.keys()):
        cv2.ellipse(imarray,(int(CentreX[i]),int(CentreY[i])),(int(Alist[i] ),int(Blist[i] )),AngleList[i],0,360,color = len(contactdic[i]), thickness = -1)
        cv2.ellipse(imarray2,(int(CentreX[i]),int(CentreY[i])),(int(Alist[i] ),int(Blist[i] )),AngleList[i],0,360,color = 255, thickness = -1)

    return imarray,imarray2

def calculate_contacts(vectorfilepath,DISTANCETHREASHOLD,yrange = [0,10000]):
    imagedata = pd.read_csv(vectorfilepath)
    Alist,Blist,AngleList,CentreX,CentreY = np.array(imagedata["Alist"]),np.array(imagedata["Blist"]),np.array(imagedata["AngleList"]),np.array(imagedata["CentreX"]),np.array(imagedata["CentreY"])
    
    numberofparticles = len(Alist)
    contactlist = {}

    for i in range(numberofparticles):
        contactlist[i] = []

    if Alist[0] == Blist[0]:
        pixelpermm = Alist[0]/7.5
    else:
        pixelpermm = Alist[0] / 14

    centretheathhold = pixelpermm * 14 * 2

    for p1 in range(numberofparticles):
        for p2 in range(numberofparticles):
            if p1 >= p2:
                #same particle or the inverse will already have been checked
                continue
            if p2 in contactlist[p1]:
                #particle already detected
                continue
            
            p1A,p1B,p1Angle,p1CentreX,p1CentreY = Alist[p1],Blist[p1],AngleList[p1],CentreX[p1],CentreY[p1]
            p2A,p2B,p2Angle,p2CentreX,p2CentreY = Alist[p2],Blist[p2],AngleList[p2],CentreX[p2],CentreY[p2]

            if (p2CentreY - p1CentreY) **2  + (p2CentreX - p1CentreX) **2 > centretheathhold**2:
                
                continue
            contactfound = False
            
            imagearray = np.zeros((5000,5000))
            for t in np.linspace(0,2*np.pi,360):
                xtocheck,ytocheck = give_ellipse_point(p2A * DISTANCETHREASHOLD ,p2B*DISTANCETHREASHOLD,p2Angle,p2CentreX,p2CentreY,t)
                
                
                isinside = check_if_point_in_ellipse(p1A ,p1B,p1Angle,p1CentreX,p1CentreY,xtocheck,ytocheck)
                
                if not contactfound:
                    if isinside:
                        
                        contactlist[p1].append(p2)
                        contactlist[p2].append(p1)
                        contactfound = True
    
    for p in range(numberofparticles):
        if CentreY[p] > yrange[1] or CentreY[p] < yrange[0]:
            #outside the desired area
            for p2 in contactlist[p]:
                contactlist[p2].remove(p)
            del contactlist[p]
            
    return contactlist
    
def calculate_coordination_number(contactdic,numberofparticles):
    totalcontacts = 0
    keylist = list(contactdic.keys())
    for i in keylist:
        totalcontacts += len(contactdic[i])
    return totalcontacts / numberofparticles
    
def calculate_mechanical_coordination_number(contactdic,numberofparticles):
    totalcontacts = 0
    Numberofparticleswith2contacts = 0
    keylist = list(contactdic.keys())
    for i in keylist:
        if len(contactdic[i]) <=1:
            pass
        else:
            Numberofparticleswith2contacts += 1
            totalcontacts  += len(contactdic[i])
    return totalcontacts / Numberofparticleswith2contacts


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








def runsetofcoords(imagevectorfolder,imagedatafile,outputfile,yrange,first= True):
    vectorfilelist = os.listdir(imagevectorfolder)



    imagedatasheet = open(imagedatafile).read().split('\n')[1::]

    


    if os.path.exists(outputfile):
        coordinationdataold = pd.read_csv(outputfile)
        coordinationdata = pd.DataFrame({"Imagename":coordinationdataold["Imagename"],"CoordinationNumber":coordinationdataold["CoordinationNumber"],"MechanicalCoordination":coordinationdataold["MechanicalCoordination"],"Timestamp":coordinationdataold["Timestamp"]})
        print("Existing File located")
    else:
        coordinationdata = pd.DataFrame(columns=["Imagename","CoordinationNumber","MechanicalCoordination","Timestamp"])


    for vectorfile in vectorfilelist:


        imagenum = vectorfile[-10:-6]
        currentim = "Image_" +  imagenum
        if currentim in list(coordinationdata["Imagename"]):
            print("Image",imagenum,"Already processed")
            continue

        for imagemetadata in imagedatasheet:
                imageindex = imagemetadata.split(';')[0][-11:-7]
                if imagenum == imageindex:
                    imagetimestamp = imagemetadata.split(';')[1]
                    break




        vectorfilepath = imagevectorfolder + "\\" + vectorfile

        contactdic = calculate_contacts(vectorfilepath,DISTANCETHEASHOLD,yrange=yrange)
        numberofparticles = len(list(contactdic.keys()))



        coordinationnumber, mechanicalcoordination, = calculate_coordination_number(contactdic,numberofparticles),calculate_mechanical_coordination_number(contactdic,numberofparticles)
        
        coordinationdata.loc[len(coordinationdata)] = ["Image_" +  imagenum,coordinationnumber,mechanicalcoordination,imagetimestamp]
        coordinationdata.to_csv(outputfile)

        loading_bar(len(coordinationdata) / len(vectorfilelist)*100,30,f'{len(coordinationdata)} Coordination: {coordinationnumber} Mechanical coordination: {mechanicalcoordination}')


        if first:
            imarray,imarray2 = drawcontactsonarray(contactdic,vectorfilepath)


            imagedata = pd.read_csv(vectorfilepath)
            Alist,Blist,AngleList,CentreX,CentreY = np.array(imagedata["Alist"]),np.array(imagedata["Blist"]),np.array(imagedata["AngleList"]),np.array(imagedata["CentreX"]),np.array(imagedata["CentreY"])



            print(contactdic)
            fig, (ax1,ax2) = plt.subplots(1,2)
            cmap = plt.get_cmap("viridis", 7)
            bounds = [0, 1, 2, 3, 4, 5, 6, 7]
            norm = mcolors.BoundaryNorm(bounds, cmap.N)

            im1 = ax1.imshow(imarray, cmap=cmap, norm=norm, interpolation="nearest")
            im2 = ax2.imshow(imarray2, cmap=cmap, norm=norm, interpolation="nearest")
            keylist = list(contactdic.keys())
            for i in keylist:
                ax1.text(CentreX[i], CentreY[i], i, ha="center", va="center", fontsize="small")
                ax2.text(CentreX[i], CentreY[i], i, ha="center", va="center", fontsize="small")

            cbar = fig.colorbar(im1, ax=ax1, ticks=[0, 1, 2, 3, 4, 5, 6], boundaries=bounds)
            cbar.set_ticklabels(['0', '1', '2', '3', '4', '5', '6'])
            
            plt.show()
        


        first = False
       

if __name__ == "__main__":
    imagevectorfolder = "I:\Mar27\Test3\ImageVectors"
    imagedatafile = "I:\Mar27\Test3\Test\Image.csv"


    outputfile = "I:\Mar27\Test3\CoordinationNumbers23.csv"
    yrange = [750,2400]
    runsetofcoords(imagevectorfolder,imagedatafile,outputfile,yrange,True)




    outputfile = "I:\Mar27\Test3\CoordinationNumbers13.csv"
    yrange = [750,10000]
    runsetofcoords(imagevectorfolder,imagedatafile,outputfile,yrange,False)

    outputfile = "I:\Mar27\Test3\CoordinationNumbers12.csv"
    yrange = [2400,10000]
    runsetofcoords(imagevectorfolder,imagedatafile,outputfile,yrange,False)



