import taufactor as tau
import tifffile
import numpy as np
import h5py

import cv2
import inspect






def run_tau_factor(slices,fx=0.5,fy=0.5):
    newslices = []
    for slice in slices:
        slice = cv2.resize(slice, None, fx=fx, fy=fy, interpolation=cv2.INTER_NEAREST)
        newslices.append(slice)
    slices = np.array(newslices)

    img = np.stack(slices, axis = 0)
    # Convert to binary
    conductive_label = 0   # change if needed
    img_bin = (img == conductive_label).astype(np.uint8)
    img_bin = np.transpose(img_bin, (1, 2, 0))
    #print("Stack shape:", img_bin.shape)

    solver = tau.AnisotropicSolver(img_bin, (75, 75, 192))
    solver.solve(iter_limit = 50000,verbose=False)
    #print("tau:", solver.tau)
    #print("D_eff:", solver.D_eff)

    return solver.tau, solver.D_eff
