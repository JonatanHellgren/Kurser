cd('~/Kurser/Spatial/exercises')
addpath('../files/TMS016_Matlab')
tms016path;
%%
satelite = imread('../data/TMS016_data/gothenburg_satellite.png');
satelite = double(satelite)/255;
[m, n, o] = size(satelite);
x = reshape(satelite, [m*n, o]);

RGB = [55,54,103; 43, 153, 136; 189, 167, 125];
RGB = double(RGB)/255;

%%
clf

subplot(2, 2, 1)
imagesc(satelite)
title('Original')


idx = normmix_kmeans(x, 3, 100);

subplot(2, 2, 2)
imagesc(reshape(idx, [m, n]));
title('K-means')


pars = normmix_sgd(x, 3, 100);
[cl, p] = normmix_classify(x, pars);
class_ml = double(cl)/3;
class = classification2rgb(p, m, n, RGB);


subplot(2, 2, 3)
imagesc(reshape(class_ml, [m, n]))
title('Classification normmix sgd')


subplot(2, 2, 4)
imagesc(class);
title('Probability * class')
%%
clf

pars = normmix_sgd(x, 4, 100);
[cl, p] = normmix_classify(x, pars);

for k=1:4
    I_class = x;
    I_class(cl~=k,:)=256;
    subplot(2,2,k)
    imagesc(reshape(I_class, [m n o]));axis image;
end

%%
clf
rel_satelite = rgb2relative(satelite);
x_rel = reshape(rel_satelite, [m*n, o]);
x_rel = double(x_rel);

subplot(2, 2, 1)
imagesc(rel_satelite)
title('Original')


idx = normmix_kmeans(x_rel, 3, 100);

subplot(2, 2, 2)
imagesc(reshape(idx, [m, n]));
title('K-means')


pars = normmix_sgd(x_rel, 3, 100);
[cl, p] = normmix_classify(x_rel, pars);
class_ml = double(cl)/3;
class = classification2rgb(p, m, n, RGB);


subplot(2, 2, 3)
imagesc(reshape(class_ml, [m, n]))
title('Classification normmix sgd')


subplot(2, 2, 4)
imagesc(class);
title('Probability * class')

%%
clf

I = imread('rice.png');
[Im, In] = size(I);
Ix = reshape(double(I), [Im*In, 1])/256;

subplot(1,2,1)
imagesc(I)

pars = normmix_sgd(Ix, 2, 100);
[cl, p] = normmix_classify(Ix, pars);

subplot(1,2,2)
imagesc(reshape(cl,[Im, In]))

%%
r = 5;
disk = strel('disk', r);
erosion = imerode(I, disk);
dilation = imdilate(I, disk);
opening = imopen(I, disk);

clf
subplot(2,2,1)
imagesc(I)

subplot(2,2,2)
imagesc(erosion)

subplot(2,2,3)
imagesc(dilation)

subplot(2,2,4)
imagesc(opening)

%%
r = 10;
disk = strel('disk', r);
opening = imopen(I, disk);

I_nb = I - opening; % no background

I_nb_x = reshape(double(I_nb), [Im*In, 1])/256;

subplot(1,2,1)
imagesc(I_nb)

pars = normmix_sgd(I_nb_x, 2, 100);
[cl, p] = normmix_classify(I_nb_x, pars);

subplot(1,2,2)
imagesc(reshape(cl,[Im, In]))


%%
function rel_img = rgb2relative(img)
    sum_img = sum(img, 3);
    
    rel_img = img ./ sum_img;
end

%% 
function mat = classification2rgb(p, m, n, RGB)
    mat = zeros(m, n, 3); % allocation
    for c = 1:n
        for r = 1:m
            mat(r,c,:) = RGB * p((c-1)*m + r, :)';
        end
    end
end

