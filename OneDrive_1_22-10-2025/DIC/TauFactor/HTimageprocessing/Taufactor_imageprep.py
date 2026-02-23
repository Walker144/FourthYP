import numpy as np
import matplotlib.pyplot as plt
import newimageprep
from skimage import morphology, segmentation, measure, util, feature, filters
from scipy import ndimage as ndi


# test image for now
cutoff = 63
file ="OneDrive_1_22-10-2025\DIC\TauFactor\TauFactorPrepPython\Testimagetiff.tiff"

BWimage = newimageprep.binarise_image(file,cutoff)
newimageprep.display_image(BWimage)


