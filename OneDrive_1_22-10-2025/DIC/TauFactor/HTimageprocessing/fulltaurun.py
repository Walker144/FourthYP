import taufactor as tau
import numpy as np
import h5py
import cv2
from PIL import Image
import matplotlib.pyplot as plt

import time
import newimageprep
import runtaufactor
import createTaufactorlayersellipse







def single_taufactor_run(file,cutoff):
    im = newimageprep.binarise_image(file,cutoff)
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
    
    
    slices = createTaufactorlayersellipse.create_taufactor_arrays(imagesize,Centersv,Centersu,Areas,Contactlist,L)
    taufactor, effectivediff  = runtaufactor.run_tau_factor(slices)
    return taufactor,effectivediff,len(Areas)

cutoff = 72


imagecsvpath = "H:\Feb24\Test2\Image.csv"
imagefile = open(imagecsvpath,'r').read().split('\n')
filepath  =imagecsvpath.split('.csv')[0]


timestamps = []
taus = []
Deff = []
particlecounts = []
tauout = ''
for im in imagefile[1::2]:
    im = im.split(';')
    timestamps.append(im[1])
    part = im[0].split('Image')[1]
    im[0] = filepath + part


    

    t,d,numareas = single_taufactor_run(im[0],cutoff)
    taus.append(float(t))
    Deff.append(float(d))
    particlecounts.append(numareas)
    tauout += f'{im[1]},{d},{t},{numareas}\n'
    tauoutfile = open('OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\Tauout2.txt','w')
    tauoutfile.write(tauout)
    tauoutfile.close()




