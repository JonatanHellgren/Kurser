cd('~/Kurser/Spatial/')

%% Loading and viewing images in Matlab
% Read image
x = imread('data/TMS016_data/chalmersplatsen.jpg');

% Get dimention
[m, n, d] = size(x);

% Transforming color values to the interval [0, 1]
x = double(x)/255;

% Visualise the image
imagesc(x);
axis image;

%% Only plotting the red value
clf
subplot(2,1,1)
imshow(x(:,:,1));

subplot(2,1,2)
imagesc(x(:,:,1));
colormap gray
axis image

%% Color manipulation
clf
subplot(2,1,1)
imagesc(x)
axis image

subplot(2,1,2)
imagesc(x(:,:,[2,1,3]))
axis image
%% Coverting to grayscale
clf
y1 = mean(x,3);
y2 = rgb2gray(x);
subplot(2,1,1)
imshow(y1)

subplot(2,1,2)
imshow(y2)
%% With a histogram
clf
imhist(y2)
%%
clf
sum_x = sum(x,3);
for it = 1:3
    rel = x(:,:,it);
    subplot(2, 2, it)
    imshow(rel./sum_x)
    
end
subplot(2,2,4)
imshow(x)
%%
clf
subplot(2,1,1)
imagesc(x)
axis image

subplot(2,1,2)
xsum = sum(x,3);
xrel = x ./ xsum;
xrel(isnan(xrel)) = 0;
imshow(xrel)
%%
clf
xlab = rgb2lab(x);
for it = 1:3
    subplot(2,2,it)
    imshow(xlab(:,:,it), [])
end
subplot(2,2,4)
imshow(x)
% first one lightness
% second is red and blue
% third is green and yellow
%% Now segmenting image
z(:,:,1) = xrel(:,:,2)>=0.4;
z(:,:,2) = xrel(:,:,2)<0.4 & xrel(:,:,1)<=0.3;
z(:,:,3) = xrel(:,:,2)<0.4 & xrel(:,:,1)>0.3 & xrel(:,:,3)<=0.3;
z(:,:,4) = xrel(:,:,2)<0.4 & xrel(:,:,1)>0.3 & xrel(:,:,3)>0.3;


%%
RGB = [55,54,103; 141,102,102; 43, 153, 136; 189, 167, 125];
RGB = double(RGB)/255;
seg = classification2rgb(z,RGB);

%%
clf
imshow(seg)

%% 
function mat = classification2rgb(z, RGB)
    [row, col, ~] = size(z);
    mat = zeros(row, col, 3); % allocation
    for r = 1:row
        for c = 1:col
            mat(r,c,:) = RGB(z(r,c,:),:);
        end
    end
end




