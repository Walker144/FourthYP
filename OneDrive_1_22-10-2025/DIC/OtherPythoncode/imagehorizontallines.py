import PIL
import numpy as np
import matplotlib.pyplot as plt

imagefile = "H:\OtherStuff\Particlesideimage.png"

img = PIL.Image.open(imagefile)

ylims = [37,496]
xlimits = []

for y in np.linspace(ylims[0], ylims[1], 27):
	plt.axhline(y=y, color='red', linewidth=2)

plt.imshow(img)
plt.show()