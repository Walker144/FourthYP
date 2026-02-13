from PIL import Image
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import math as m

#set the name of the file to load
filename = 'OneDrive_1_22-10-2025\DIC\TauFactor\TauFactorPrepPython\IBW.tif'
PINRADIUS = 12


def load_binary_tif(file):
    img = Image.open(file)
    # Convert to grayscale if needed
    if img.mode != 'L':
        img = img.convert('L')
    img_array = np.array(img)
    # Normalize to 0 and 1 (white pixels become 1, black become 0)
    binary_array = (img_array > 127).astype(int)
    return binary_array


baseimage = load_binary_tif(filename)



#plotting function, add other colours and bases as needed for plotting
def plot_array_as_image(array):
    array[0][0] = 2
    array[0][1] = 3
    colors = ['black', 'white','green','red']  # 0=black, 1=white
    cmap = ListedColormap(colors)
    plt.imshow(baseimage, cmap=cmap)
    plt.axis('off')
    plt.show()

def generate_circle_vectors(radius):
    thetalist = np.linspace(0, 2*m.pi, 12)
    xlist = np.sin(thetalist) * radius
    ylist = np.cos(thetalist) * radius

    vectors = np.empty((len(thetalist), 2), dtype=int)
    for i in range(len(thetalist)):
      
        vectors[i] = [int(xlist[i]), int(ylist[i])]

    return vectors

def generate_circle_positions(radius,x0,y0):
    return generate_circle_vectors(radius) + np.array([x0,y0])

def check_position_of_pin_centres(array,):
    ysize = len(array)
    xsize = len(array[0])
    
    listpossible = []
    for ymid in range(ysize):
        for xmid in range(xsize):
            positions_to_check = np.concatenate([generate_circle_positions(PINRADIUS, ymid, xmid), generate_circle_positions(PINRADIUS/2, ymid, xmid)])
            possible = True
            
            for pos in positions_to_check:
                try:
                    if array[pos[0]][pos[1]] == 1:
                        possible = False
                        break
    
                except:
                    possible = False
                    break
            if possible:
                listpossible.append([ymid,xmid])
                array[ymid][xmid] = 2
        if ymid % 10 == 0:
            print(ymid)
    
    return array
            







baseimage = check_position_of_pin_centres(baseimage)
plot_array_as_image(baseimage)



