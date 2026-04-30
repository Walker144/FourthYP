import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

file1 = "I:\Apr01\Test3\ImageVectors\Image_0000_0.csv"
file2 = "I:\Apr01\Test3\ImageVectors\Image_0858_0.csv"

num_bins = 15
bin_edges = np.linspace(0, 180, num_bins + 1)


f1df = pd.read_csv(file1)
f1angles = np.sort(np.array(f1df["AngleList"]))
binned_angles1, _ = np.histogram(f1angles, bins=bin_edges)

f2df = pd.read_csv(file2)
f2angles = np.sort(np.array(f2df["AngleList"]))
binned_angles2, _ = np.histogram(f2angles, bins=bin_edges)




bin_edges = (bin_edges[:-1] + bin_edges[1:]) / 2
plt.plot(bin_edges,binned_angles1,label = "t = 0")
plt.plot(bin_edges,binned_angles2,label = "t = 529")



print(len(f2angles),len(f1angles))





plt.xlabel('Angle from horizontal ($\degree$)')
plt.ylabel('Count')
plt.ylim(0,80)
plt.xlim(0,180)

plt.grid()

plt.show()




