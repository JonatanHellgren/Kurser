cd('~/Kurser/Spatial/exercises')
addpath('../files/TMS016_Matlab')
tms016path;
%% Loading the data and plotting some
mnist = load('~/Kurser/Spatial/data/TMS016_data/mnist_data.mat');
imagesc(mnist.x(:,:,7))
colormap gray
axis image

%% Computing moments
s = size(mnist.x);
N = s(3);

m = zeros([N,7]);
for it = 1:N
    m(it,:) = hu_moments(mnist.x(:,:,it));
end
%% Train a linear discriminat classifier
t = templateDiscriminant('DiscrimType','Linear');
C = fitcecoc(m(:,[1,7]),mnist.z,'Learners',t);
plotconfusion(categorical(mnist.z),categorical(resubPredict(C)))

%%
k = 10;
Ccv = crossval(C,'kfold',k);
zhat = kfoldPredict(Ccv);
plotconfusion(categorical(mnist.z),categorical(zhat))

%% Trying out different classifiers

t = templateDiscriminant('DiscrimType','Quadratic');
C = fitcecoc(m, mnist.z,'Learners',t);
Ccv = crossval(C,'kfold',k);
zhat = kfoldPredict(Ccv);
plotconfusion(categorical(mnist.z),categorical(zhat))