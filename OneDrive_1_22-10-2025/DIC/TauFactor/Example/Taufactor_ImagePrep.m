% Prepare images for taufactor + Coordination number calc + local e
% O. Adamidis 2024

clear

% Find number of images, all placed in subfolder Images within current
% directory, update image type, here .png
images = dir([pwd '\*.jpg']);
totalimages = size(images,1);

ii=1; % image number to prepare for TauFactor
% Open image - Change image adjust properties as needed
Image = OpenImage(images,ii);
%  Crop image [left right bottom top] values from 0 to 1
Image = CropImage(Image,[0.1 0.90 0.15 0.70]);
% Binarize image - Change radius range for particles as needed
ImageBW = BinIm(Image);
% Identify particles
[Centersu,Centersv,Areas,L,CN]=ParticleWatershed(ImageBW);
%% Calculate coordination number
% CN figure
ImageCN=zeros(size(ImageBW));
for kk=1:size(Centersu,1)
    ImageCN(L==kk)=CN(kk);
end
%figure; surface(ImageCN,'EdgeColor','none'); axis equal; view(0,-90); h=colorbar; h.Ticks=[[min(CN):max(CN)]];
rgbCN = label2rgb(ImageCN,'lines','k');
figure; imshow(rgbCN); 
colormap(lines(max(CN))); clim([min(CN), max(CN)]); h=colorbar; h.Ticks=min(CN):max(CN);

figure; plot(Areas,'o'); %to help identify areas
CNup=CN;
CNup(Areas<6000)=[]; % get rid of oversegmented particles
Average_Coordination = sum(CNup)/size(CNup,1);
Mechanical_Coordination = (sum(CNup)-size(CNup(CNup==1),1))/(size(CNup,1)-size(CNup(CNup==0),1)-size(CNup(CNup==1),1));
%% Check segmentation
figure 
rgb = label2rgb(L,'lines',[.5 .5 .5]);
for kk=1:size(Centersu,1)
    rgb = insertText(rgb,[Centersu(kk), Centersv(kk)],num2str(kk));
end
imshow(rgb)

%% Create 13 sections 6 + 1 + 6 for Taufactor
Radius1 = [1 1 1 1 0.96 0.88 0.83]; % Reduction of Radius for section 1. TO BE DEFINED based on Solidworks drawing
Radius2 = [1 1 1 1 0.96 0.88 0.83]; % Reduction of Radius for section 2. TO BE DEFINED based on Solidworks drawing
figure; plot(Areas,'o'); %to help identify areas

Section = zeros(size(ImageBW,1),size(ImageBW,2),size(Radius1,2));
for kk=1:size(Radius1,2)
    Image = Section(:,:,kk);
    for jj=1:size(Centersu,1)
        %lowered lower area from 6000
        if Areas(jj)>2000 && Areas(jj)<10000 % Use Radius1
            Image = drawCircle(Image, [Centersu(jj) Centersv(jj)], Radius1(kk)*sqrt(Areas(jj)/pi));
        %adjusted lower end of radius2
        elseif Areas(jj)>10000 && Areas (jj)<28000 % Use Radius 2
            Image = drawCircle(Image, [Centersu(jj) Centersv(jj)], Radius2(kk)*sqrt(Areas(jj)/pi));
        else
            Image(L==jj)=0; % if not one of the radii identified, IGNORE particle
        end
    end
    % imshow(Image)
    Section(:,:,kk) = Image;
end

%% save images for tau factor Scale down to make it faster if needed
% figure; imshow(imresize(Section(:,:,1),0.5,'nearest')); % check resizing
for kk=1:size(Section,3)
    imwrite(imresize(Section(:,:,kk),0.5,'nearest'),['I' num2str(kk) '.tif'],'tif')
end
%% calculate local void ratio based on particle cross section
e = eCrop(Section);

% %% plot displacement
% j1=1;
% j2=4;
% figure
% % rgb = label2rgb(L,'lines',[.5 .5 .5]); imshow(rgb)
% % imshow(Image)
% C = imfuse(OpenImage(images,j1),OpenImage(images,j2),'falsecolor','Scaling','joint','ColorChannels',[1 2 2]);
% imshow(C)
% hold on;
% quiver(Centersu(:,j1),Centersv(:,j1),Centersu(:,j2)-Centersu(:,j1),Centersv(:,j2)-Centersv(:,j1),0.5)

%% %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  F U N C T I O N S
%  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [ImageBW] = OpenImage(images,ii)
% Opens image, adjusts, and turns to greyscale
Image = imread([images(ii).folder '\' images(ii).name]);
% figure; imshow(Image);
% Adjust image if needed
Imageadj = imadjust(Image,[0.2 0.7],[0 1],[0.5 0.7 1]);
% figure; imshow(Imageadj);
% Turn to greyscale
ImageBW = rgb2gray(Imageadj);
% figure; imshow(ImageBW);
end

function [Image] = CropImage(Image,crop)
Image = Image(floor((1-crop(4))*size(Image,1))+1:floor((1-crop(3))*size(Image,1)),...
    floor(crop(1)*size(Image,2))+1:floor(crop(2)*size(Image,2)));
end

function [bw3] = BinIm(Image)
% Use the imbinarize function to convert the grayscale image into a binary image.
bw = imbinarize(Image,'adaptive','ForegroundPolarity','bright','Sensitivity',0.5);
% figure;imshow(bw)
% fill holes within circular particles
[centres,radii] = imfindcircles(bw,[40 100],"ObjectPolarity","bright","Sensitivity",0.91); % change radii range here
% figure;imshow(bw);viscircles(centers,radii);
for kk=1:size(centres,1)
    bw = drawCircle(bw, centres(kk,:), radii(kk)*0.8);
end
% Fill holes with area <20
bw2 = ~bwareaopen(~bw, 20);
% Remove background noise from the image with the bwareaopen function.
bw3 = bwareaopen(bw2,1200); %removes all connected components (objects) that have fewer than P pixels from the binary image BW, producing another binary image, BW2.
% figure;imshow(bw3)
end

function [Centersu,Centersv,Areas,L,CN]=ParticleWatershed(ImageBW)
% Separate particles
% Calculate the distance transform of the complement of the binary image.
% The value of each pixel in the output image is the distance between that
% pixel and the nearest nonzero pixel of bw.
D = bwdist(~ImageBW);
% D(~ImageBW) = -Inf;
D = -D;
% imshow(D,[])
% remove local minima (do surf(D) to check value) to avoid oversegmentation
E = imhmin(D,1);
% Watershed transform to separate particles, also when touching
L = watershed(E,8);
L(~ImageBW) = 0;
%  Region props
CC = regionprops(L,'Area','Centroid','Centroid','BoundingBox','PixelList');
totalparticles=size(CC,1);
Centersu = zeros(totalparticles,1);
Centersv = zeros(totalparticles,1);
Areas = zeros(totalparticles,1);
CN = zeros(totalparticles,1);
for jj=1:size(Centersu,1)
    Centersu(jj) = CC(jj).Centroid(1);
    Centersv(jj) = CC(jj).Centroid(2);
    Areas(jj) = CC(jj).Area;
    % coordination number calculation
    ImageBinWatershed = double(L); 
    ImageBinWatershed(ImageBinWatershed>0)=1;
    mask = zeros(size(ImageBW)); 
    mask(L==jj) = 1;
    dilatedmask = imdilate(mask, strel('disk',4));
    ImageTemp = ImageBinWatershed+dilatedmask-ones(size(ImageBW));
    ImageTemp(ImageTemp==-1)=0;
    ImageTemp = bwareaopen(ImageTemp,6); % delete up to 6 pixel areas
    cn = bwconncomp(ImageTemp);
    CN(jj) = cn.NumObjects-1;
end
end

function Image = drawCircle(Image, center, radius)
    % Create a meshgrid for the image dimensions
    [x,y] = meshgrid(1:size(Image,2), 1:size(Image,1));

    % Calculate the distance of each pixel from the center
    dist = sqrt((x - center(1)).^2 + (y - center(2)).^2);

    % Create a circular mask
    circleMask = dist <= radius;

    % Set pixels within the circle to 1
    Image(circleMask) = 1;
end

function e = eCrop(Section)
figure; imshow(Section(:,:,1));
roi = drawrectangle;
vvoids = zeros(size(Section,3),1);
vsolid = zeros(size(Section,3),1);
for kk=1:size(Section,3)
    Image = Section(:,:,kk);
    ImageCrop = Image(floor(roi.Position(2))+1:floor(roi.Position(2)+roi.Position(4)),floor(roi.Position(1))+1:floor(roi.Position(1)+roi.Position(3)));
    vvoids(kk) = nnz(~ImageCrop);
    vsolid(kk) = nnz(ImageCrop);
end
weights = [0.5;ones(size(Section,3)-2,1);0.5];
e = sum(weights.*vvoids)/sum(weights.*vsolid);
disp(e);
end