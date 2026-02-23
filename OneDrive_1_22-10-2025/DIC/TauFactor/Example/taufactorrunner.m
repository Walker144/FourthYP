
addpath('Users\andre\AppData\Roaming\MathWorks\MATLAB Add-Ons\Apps\TauFactor')
% Load all .tif files from the current directory
tif_files = dir('*.tif');

% Create a cell array to store the images
images = [];

for i = 1:length(tif_files)
    img = imread(tif_files(i).name);
    if i == 1
        images = zeros(size(img, 1), size(img, 2), length(tif_files));
    end
    images(:,:,i) = img;
end
images = images / 255;

 
PhaDir = [[1 0 0] [0 0 0] [0 0 0]];
VoxDims = [0.216 0.216 0.192];
RVAmode = 0;

Results = TauFactor('InLine',1,1,RVAmode,images,PhaDir,VoxDims)

