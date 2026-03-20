import matplotlib.pyplot as plt
import numpy as np
import PIL
import random

#####################################
#####       PARAMETERS          #####
#####################################

#pixel per inch
dpi = 450

#print area (mm)
printlength = 24
printwidth = 240

#speckle size (mm)
specklesize = 0.53

savepath = 'OneDrive_1_22-10-2025\DIC\OtherPythoncode'
filetype = '.png'

#################################
#####       FUNCTIONS       #####
#################################

def generate_circle_on_array(imarray,x,y,radius):
    theta = np.array(list(range(0,360,18)))
    theta = theta * np.pi / 180
    
    rlist = np.array(list(range(0,10))) * radius/10

    for r in rlist:
        for t in theta:
            try:
                imarray[int(x + r * np.cos(t))][int(y + r * np.sin(t))] = 0
            except:
                pass
            
    return imarray






#############################################
#####       SPECKLE GENREATION          #####
#############################################


inches_to_mm = 25.4

dpmm = dpi/ inches_to_mm

speckleradius = dpmm * specklesize * .5

imlength = int(printlength*dpmm)
imwidth = int(printwidth * dpmm)
imarray = np.ones((imlength,imwidth))
print(imarray)

print(imwidth,imlength)

for i in range(10000):
    imarray = generate_circle_on_array(imarray,random.randint(0,imlength),random.randint(0,imwidth),speckleradius + random.randint(-100,100)/60)

plt.imshow(imarray)

plt.show()
PIL.Image.fromarray((imarray * 255).astype(np.uint8)).save(savepath +'\specklepattern' +filetype)




