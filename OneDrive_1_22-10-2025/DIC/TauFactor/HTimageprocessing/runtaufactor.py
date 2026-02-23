import taufactor as tau
import tifffile
import numpy as np

filelist = []

for i in range(1,14):
    filelist.append(f'OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing\I{i}.tif')

slices = [tifffile.imread(f) for f in filelist]

img = np.stack(slices, axis = 0)
print("Stack shape:", img.shape)

# Convert to binary
conductive_label = 0   # change if needed
img_bin = (img == conductive_label).astype(np.uint8)
img_bin = np.transpose(img_bin, (1, 2, 0))
 
print("Stack shape:", img_bin.shape)
# Run TauFactor
solver = tau.AnisotropicSolver(img_bin, (217, 217, 192))
solver.solve()

print("tau:", solver.tau)
print("D_eff:", solver.D_eff)


