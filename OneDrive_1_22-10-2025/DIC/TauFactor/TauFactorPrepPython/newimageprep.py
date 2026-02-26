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




#############################################
#####           Main Code               #####
#############################################
image_path = "OneDrive_1_22-10-2025\DIC\TauFactor\TauFactorPrepPython\Image_0002_0.tiff"
image = Image.open(image_path)
#current setup is 25 3 62 88
image = image.crop((image.width * .25, image.height * .3, image.width * .62, image.height *.88))

saturation = np.array(image)
plt.figure(figsize=(10, 6))
plt.hist(saturation.flatten(), bins=256, range=(0, 256))
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')
plt.title('Histogram of Saturation')
plt.show()

cutoff = 72

saturation[saturation > cutoff] = 250
saturation[saturation <= cutoff] = 255
saturation[saturation == 250] = 0

Image.fromarray(saturation.astype(np.uint8)).save("OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\processed_image.jpg")



display_image(saturation, "Greyscale TIFF Image")
