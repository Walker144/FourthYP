import pandas
import numpy as np
import matplotlib.pyplot as plt
import h5py
import scipy.io
import cv2



f = 'OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\Tauimagevec.mat'
matdata = h5py.File(f,'r+')

imagesize = np.array(matdata["imsize"])
Centersv = np.array(matdata["Centersv"])[0]
Centersu = np.array(matdata["Centersu"])[0]
Areas = np.array(matdata["Areas"])[0]
Contactlist = np.array(matdata["CN"])[0]

Radius1 = [1,.97,1,1,.97,.90,.82,.76,.73,.70,.68,.67,.67]
Radius2 = [1,.97,1,1,.97,.90,.82,.76,.73,.70,.68,.67,.67]
layers = np.zeros(shape=(len(Radius1),int(imagesize[0][0]),int(imagesize[1][0])))
CircleAcutoff = 4000
ElipseAcutoff = 8000








#################################
#####       FUNCTIONS       #####
#################################











#################################
#####       MAIN CODE       #####
#################################


print(Areas[142:150])

for i in range(len(Areas)):
    Area = Areas[i]
    sv = int(Centersv[i])
    su = int(Centersu[i])
    print(sv,su)
    Contacts = Contactlist[i] 


    
    if Area > CircleAcutoff and Area <  ElipseAcutoff:
        for j in range(len(Radius1)):
            cv2.circle(layers[j],(su,sv),int(Radius1[j] * (Area/np.pi) **0.5),255,-1)

    elif Area > ElipseAcutoff:
        for j in range(len(Radius1)):
            cv2.ellipse(layers[j],(su,sv),int(Radius1[j] * (Area/np.pi) **0.5),255,-1)

plt.imshow(layers[0])
plt.show()