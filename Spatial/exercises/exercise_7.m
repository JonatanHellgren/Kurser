cd('~/Kurser/Spatial/exercises')
addpath('../files/TMS016_Matlab')
tms016path;
%%
clf
n = 100;
N = [0 1 0; 1 0 1; 0 1 0];
k = 2;
alpha = 0;
beta = 1.6;
Beta = eye(n) * beta;
z0 = zeros([n,n,k]);

rng(123)
z = mrf_sim(z0, N, alpha, beta, 15);

imshow(z(:,:,1))

%%
rng(123)
a1 = 0.50;
a2 = 1 - a1;
alpha = [a1, a2];
z = mrf_sim(z0, N, alpha, beta, 15);

imshow(z(:,:,1))

%%
clf
N2 = [1 1 1; 
      1 0 1;
      1 1 1];
  
N3 = [1 1 0;
      1 0 1;
      0 1 1];
  
N4 = [0 0 0 1 1;
      0 0 1 1 0;
      0 1 0 1 0;
      0 1 1 0 0;
      1 1 0 0 0];

rng(123)
z = mrf_sim(z0, N, alpha, beta, 15);
subplot(2,2,1)
imshow(z(:,:,1))


rng(123)
z2 = mrf_sim(z0, N2, alpha, beta, 15);
subplot(2,2,2)
imshow(z2(:,:,1))


rng(123)
z3 = mrf_sim(z0, N2, alpha, beta, 15);
subplot(2,2,3)
imshow(z3(:,:,1))


rng(123)
z4 = mrf_sim(z0, N2, alpha, beta, 15);
subplot(2,2,4)
imshow(z4(:,:,1))