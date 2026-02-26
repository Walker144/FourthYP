import pandas
import numpy as np
import matplotlib.pyplot as plt
import h5py
import scipy.io
import cv2
from PIL import Image
import taufactor as tau












#################################
#####       FUNCTIONS       #####
#################################

def calculate_elipse_rotation(xpoints,ypoints):
    

    
    xpoints = np.array(xpoints)
    ypoints = np.array(ypoints)

    xmid = np.mean(xpoints)
    ymid = np.mean(ypoints)

    xpoints = xpoints - xmid
    ypoints = ypoints - ymid

    mu20 = 0
    mu02 = 0
    mu11 = 0
    for j in range(len(xpoints)):
        mu20 += xpoints[j] **2
        mu02 += ypoints[j]**2
        mu11 += xpoints[j] * ypoints[j]

    theta = 180 / np.pi *0.5 * np.atan2(2*mu11,(mu20 - mu02))
    return theta


def create_index_dict(maxindex,L):
    ydict = {}
    xdict = {}

    for i in range(1,maxindex+1):
        ydict[i] = []
        xdict[i] = []
    
    for dy in range(len(L)):
        for dx in range(len(L[0])):
            a =  L[dy][dx]
            if a != 0:
                ydict[a].append(dy)
                xdict[a].append(dx)
    return ydict,xdict


def create_taufactor_arrays(imagesize,Centersv,Centersu,Areas,Contactlist,L):
    Radius1 = [.97,1,1,.97,.90,.82,.76,.73,.70,.68,.67,.67]
    Radius2 = [.93,.99,1,1,.99,.94,.90,.87,.85,.84,.83,.82,.82]

    ydict,xdict = create_index_dict(len(Areas),L)



    layers = np.zeros(shape=(len(Radius1),int(imagesize[0][0]),int(imagesize[1][0])))
    CircleAcutoff = 4000
    ElipseAcutoff = 8000
    for i in range(len(Areas)):
        Area = Areas[i]
        sv = int(Centersv[i])
        su = int(Centersu[i])
        Contacts = Contactlist[i] 

        
        if Area > CircleAcutoff and Area <  ElipseAcutoff:
            for j in range(len(Radius1)):
                cv2.circle(layers[j],(su,sv),int(Radius1[j] * (Area/np.pi) **0.5),255,-1)

        elif Area > ElipseAcutoff:
            angle = calculate_elipse_rotation(xdict[i+1],ydict[i+1])
            alpha = 7.5/14
            a = int((Area/(np.pi*alpha))**0.5)
            b = int(a * alpha)

            for j in range(len(Radius1)):
                cv2.ellipse(layers[j],(su,sv),(int(a*Radius2[j]),int(b*Radius1[j])),-angle+90,0,360,color= 255,thickness=-1)

    return layers
def run_taufactor_from_mat(f):
    matdata = h5py.File(f,'r+')
    imagesize = np.array(matdata["imsize"])
    Centersv = np.array(matdata["Centersv"])[0]
    Centersu = np.array(matdata["Centersu"])[0]
    Areas = np.array(matdata["Areas"])[0]
    Contactlist = np.array(matdata["CN"])[0]
    L = np.array(matdata["L"])

    slices = create_taufactor_arrays(imagesize,Centersv,Centersu,Areas,Contactlist,L)

    newslices = []

    for slice in slices:
        slice = cv2.resize(slice, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
        newslices.append(slice)

    slices = np.array(newslices)

    img = np.stack(slices, axis = 0)
    # Convert to binary
    conductive_label = 0   # change if needed
    img_bin = (img == conductive_label).astype(np.uint8)
    img_bin = np.transpose(img_bin, (1, 2, 0))
    print("Stack shape:", img_bin.shape)

    solver = tau.AnisotropicSolver(img_bin, (217, 217, 192))
    solver.solve(iter_limit = 50000)
    print("tau:", solver.tau)
    print("D_eff:", solver.D_eff)
    return solver.tau




