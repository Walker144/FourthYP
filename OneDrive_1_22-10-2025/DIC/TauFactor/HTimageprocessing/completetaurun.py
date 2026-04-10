import newimageprep

import matlab.engine

eng = matlab.engine.start_matlab()
eng.addpath("OneDrive_1_22-10-2025\DIC\TauFactor\HTimageprocessing")
eng.Taufactor_ImagePrepimagebw(nargout=0)

