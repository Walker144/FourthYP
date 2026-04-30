import taufactor as tau
import numpy as np
import h5py
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import os
import time
import newimageprep
import runtaufactor
import createTaufactorlayersellipse



#crop left,top,right,bottom
#crop for test1 [.35,.1,.88,.97]
#crop for test 2 [.32,.06]


def single_image_run(file,cutoff,vectorfile,first = True):
    im = newimageprep.binarise_image(file,cutoff,[.28,.06,.79,.95])
    if first:
        plt.imshow(im)
        plt.show()

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
    
    print("matlabdone", len(Areas))
    slices,exportdf = createTaufactorlayersellipse.create_taufactor_arrays(imagesize,Centersv,Centersu,Areas,Contactlist,L,GenerateExport=True)
    
    exportdf.to_csv(vectorfile)
    
    

    

#test 1 cutoff = 72
cutoff= 80


'''imagefolder = "H:\Mar27\Test1\Test"
vectorfolder = "H:\Mar27\Test1\ImageVectors"'''

'''imagefolder = "H:\Mar27\Test3\Test"
vectorfolder = "H:\Mar27\Test3\ImageVectors"'''

imagefolder = "I:\Mar31\Test1\Test"
vectorfolder = "I:\Mar31\Test1\ImageVectors"



imagecsvpath =  imagefolder + "\\Image.csv"



imagefile = open(imagecsvpath,'r').read().split('\n')
filepath  =imagecsvpath.split('.csv')[0]


timestamps = []
taus = []
Deff = []
particlecounts = []
tauout = ''
first = True

for im in imagefile[1::4]:
    im = im.split(';')
    timestamps.append(im[1])
    part = im[0].split('Image')[1]
    print(part)
    im[0] = filepath + part
    vectorpath = vectorfolder + "\\Image" + part[:-4] + 'csv'
    


    csvlist = os.listdir(vectorfolder)
    if "Image" + part[:-4] + 'csv' in csvlist:
        print(part[:-4], "already processed")
        continue


    
    print(im[0])
    
    single_image_run(im[0],cutoff,vectorpath,first = first)
    first = False


    '''taus.append(float(t))
    Deff.append(float(d))
    particlecounts.append(numareas)
    tauout += f'{im[1]},{d},{t},{numareas}\n'
    tauoutfile = open('OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\Tauout2.txt','w')
    tauoutfile.write(tauout)
    tauoutfile.close()'''




