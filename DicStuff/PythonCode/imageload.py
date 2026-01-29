from matplotlib.widgets import Cursor
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('DicStuff\PythonCode\Image_0000_0.tiff')  # Replace with your image path
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(img)


plt.tight_layout()
plt.show()