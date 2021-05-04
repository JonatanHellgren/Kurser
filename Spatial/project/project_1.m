cd('~/Kurser/Spatial/project')
addpath('../files/TMS016_Matlab')
tms016path;
%% Loading the images
rosetta = imread('images/rosetta.jpg');
rosetta = mean(rosetta,3);
rosetta = double(rosetta)/255;

titan = imread('images/titan.jpg');
titan = double(titan)/255;

%% Taking a look
subplot(1,2,1)
imagesc(titan)
title('Titian')
axis image
colormap gray

subplot(1,2,2)
imagesc(rosetta)
title('Rosetta')
axis image
colormap gray

%% Removing pixels
img = titan;

% probability for observing pixel
p_c = 0.1;

% storing the dimnetions of the image
[m, n] = size(img);

% converting into a column vector
x = reshape(img, [m*n, 1]);

% calculating amount of pixels to remove
rng(123)
N = binornd(m*n, p_c);

% selecting which pixels to keep with seed

ind = randperm(m*n);

% divding up the data in to convinent vectors
ind_obs = ind(1:N);
ind_mis = ind(N+1:end);
x_obs = x(ind_obs);
x_mis = x(ind_mis);

% defining the locations for each pixel 
[loc_x, loc_y] = meshgrid(1:m, 1:n);
loc = [reshape(loc_x, [1, m*n]); reshape(loc_y, [1, m*n])]';

loc_obs = loc(ind_obs,:);

%% comparing original image with sampled one
clf

% original image
subplot(1, 2, 1)
imagesc(img)

% sampled image
sample_x(ind) = [x_obs; zeros(m*n - N, 1)];
subplot(1, 2, 2)
imagesc(reshape(sample_x, [m, n]))

%% 1 %%


%% estimating paramers
emp = emp_variogram(loc_obs(1:min(N,10000),:), x_obs(1:min(N,10000)), 50);
params = cov_ls_est(x_obs, 'matern', emp);


%      sigma: 6.5949e+04
%      kappa: 8.4947e-10
%         nu: 0.9627
%    sigma_e: 0.0819

%      sigma: 0.1754
%      kappa: 0.0192
%         nu: 1.0001
%    sigma_e: 0.1761

%% Plotting the binned estimate and the matern estimate
% Binned estimate
subplot(1,2,1)
plot(emp.h, emp.variogram)
title('Binned estimate')

% matern estimate
nu = 1; % specified in assignment text
matern_est = matern_variogram(emp.h, params.sigma, params.kappa, nu, params.sigma_e);
subplot(1,2,2)
plot(emp.h, matern_est)
title('Matern estimate')

%% 2 %%


%% Defining stenctil
kappa = params.kappa;
stencil = kappa^4 * [0 0 0 0 0; 0 0 0 0 0; 0 0 1 0 0; 0 0 0 0 0; 0 0 0 0 0] + ...
          2*kappa^2 * [0 0 0 0 0; 0 0 -1 0 0; 0 -1 4 -1 0; 0 0 -1 0 0; 0 0 0 0 0] + ...
          [0 0 1 0 0; 0 2 -8 2 0; 1 -8 20 -8 1; 0 2 -8 2 0; 0 0 1 0 0];
      
tau = 2 * pi / params.sigma^2;

Q = tau *  stencil2prec([m, n],stencil);

%%
clf

Qop = Q(ind_mis, ind_obs);
%Qo = Q(ind_obs, ind_obs);
Qp = Q(ind_mis, ind_mis);


mu_B = mean(x_obs);
mu_A = mu_B;

post_mean = mu_A - Qp\Qop*(x_obs - mu_B);

reconstructed_x(ind) = [x_obs; post_mean];

subplot(2, 2, 1)
imagesc(reshape(x, [m,n]))
title('Original')

subplot(2, 2, 2)
imagesc(reshape(sample_x, [m, n]))
title('Sampled')

subplot(2, 2, 3)
imagesc(reshape(reconstructed_x, [m, n]))
title('Reconstructed')









