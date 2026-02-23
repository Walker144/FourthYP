import numpy as np
from PIL import Image
import matplotlib.pyplot as plt



#############################################
#####           Functions               #####
#############################################

def display_image(image_array, title="Image"):
    plt.figure(figsize=(8, 6))
    plt.imshow(image_array, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

cutoff = 65
file ="OneDrive_1_22-10-2025\DIC\TauFactor\TauFactorPrepPython\Image_0002_0.tiff"

def plot_hisogram(file):
    image = Image.open(file)
    image_array = np.asarray(image)
    plt.figure(figsize=(10, 6))
    plt.hist(image_array.flatten(), bins=256, range=(0, 256), color='gray', edgecolor='black')
    plt.xlabel('Light Intensity')
    plt.ylabel('Frequency')
    plt.title('Image Histogram')
    plt.show()

def binarise_image(file,cutoff):
    image_path = file
    image = Image.open(image_path)
    image = image.crop((image.width * .19, image.height * .3, image.width * .55, image.height *.88))
    saturation = np.asarray(image).copy()
    saturation[saturation > cutoff] = 250
    saturation[saturation <= cutoff] = 255
    saturation[saturation == 250] = 0
    return saturation

plot_hisogram(file)
im = binarise_image(file,cutoff)
display_image(im)
