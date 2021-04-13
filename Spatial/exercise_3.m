cd('~/Kurser/Spatial/')
addpath('./files/TMS016_Matlab')
tms016path;
%%
clf
n = 50;
[loc_x, loc_y] = meshgrid(1:n, 1:n);
loc = [reshape(loc_x, [1, n^2]); reshape(loc_y, [1, n^2])]';
D = squareform(pdist(loc));

sigma = 1;
nu = 5;
%r = 5;
kappa = 1;


Sigma = matern_covariance(D, sigma, kappa, nu);
R = chol(Sigma);
Mu = zeros(n^2, 1);
rng(123)
z = randn(n^2, 1);
Z = Mu + R'*z;

betas = [1, 0.01];
X = SIM(loc, Z, betas(1), betas(2));

subplot(2, 1, 1)
imagesc(reshape(Z, [n, n]))
title('Z(s)')


subplot(2, 1, 2)
imagesc(reshape(X, [n, n]))
title('X(s)')

n_obs = 500;
rng(123)
ind = randperm(n*n);
ind_o = ind(1:n_obs);
ind_p = ind(n_obs+1:n*n);
hold on
c = 'red';
scatter(loc(ind_o, 1), loc(ind_o, 2), c)

sigma_e = 0.1;
Y = X(ind_o) + normrnd(0, sigma_e, [n_obs,1]);



%%
clf
b1 = ones(n_obs,1);
b2 = loc(ind_o, 1);
B = [b1, b2];
betas_ols = (B' * B) \ B' * Y; %[b1, b2]\Y;

residuals = Y - mean(Y); %[b1, b2] * betas;

scatter(1:n_obs, residuals')
title('Residuals')
%% variograms
clf
sample_ind = loc(ind_o, :);
emp = emp_variogram(sample_ind, Y, 50);

subplot(2, 2, 1)
plot(emp.h, emp.variogram)
title('Binned estimate')
%scatter(residuals, emp.N)

h = linspace(0, 80);

params = cov_ls_est(Y, 'matern', emp);
matern_est = matern_variogram(h, params.sigma, params.kappa, params.nu, params.sigma_e);
subplot(2, 2, 2)
plot(h, matern_est)
title('Matern estimate')

matern = matern_variogram(h, sigma, kappa, nu, sigma_e);
subplot(2, 2, 3)
plot(h, matern)
title('True matern')

subplot(2, 2, 4)
plot(h, matern_covariance(h, sigma, kappa, nu))
title('Matern covariance')

%%
D = squareform(pdist(sample_ind));
nugget = params.sigma_e^2;
D = D + diag(ones([1,n_obs]) * nugget);
Sigma = matern_covariance(D, sigma, kappa, nu);
betas_gls = (B' * inv(Sigma) * B) \ (B' * inv(Sigma) * Y);

Sigma_est = matern_covariance(D, params.sigma, params.kappa, params.nu);
betas_gls_est = (B' * inv(Sigma_est) * B) \ (B' * inv(Sigma_est) * Y);

%%
clf
D_kriging = squareform(pdist(loc(ind, :)));
nugget = params.sigma_e^2;
Sigma_op = matern_covariance(D_kriging, params.sigma, params.kappa, params.nu);
Sigma_op = Sigma_op + diag(ones([1,n*n]) * nugget);
Sigma_o = Sigma_op(1:n_obs, 1:n_obs);
Sigma_p = Sigma_op(1:n_obs, n_obs+1:end);

mu = betas_gls_est(1) * 1 + betas_gls_est(2) * loc(ind,1);
mu_o = mu(1:n_obs);
mu_p = mu(n_obs+1:end);

mu_p = mu_p + Sigma_p' * inv(Sigma_o) * (residuals);


est = [Y; mu_p];

est_ord(ind) = est;


subplot(3, 1, 1)
imagesc(reshape(X, [n, n]))
title('X(s)')
hold on
c = 'red';
scatter(loc(ind_o, 1), loc(ind_o, 2), c)

subplot(3, 1, 2)
imagesc(reshape(est_ord, [n,n]))
hold on
c = 'red';
title('X_{pred}')
scatter(loc(ind_o, 1), loc(ind_o, 2), c)
%%
params_ml = cov_ml_est(Y, 'matern', sample_ind);
Sigma_est_ml = matern_covariance(D, params_ml.sigma, params_ml.kappa, params_ml.nu);
betas_ml_est = (B' * inv(Sigma_est) * B) \ (B' * inv(Sigma_est) * Y);

nugget = params_ml.sigma_e^2;
Sigma_op = matern_covariance(D_kriging, params_ml.sigma, params_ml.kappa, params_ml.nu);
Sigma_op = Sigma_op + diag(ones([1,n*n]) * nugget);
Sigma_o = Sigma_op(1:n_obs, 1:n_obs);
Sigma_p = Sigma_op(1:n_obs, n_obs+1:end);

mu = betas_ml_est(1) * 1 + betas_ml_est(2) * loc(ind,1);
mu_o = mu(1:n_obs);
mu_p = mu(n_obs+1:end);

mu_p = mu_p + Sigma_p' * inv(Sigma_o) * (residuals);


est = [Y; mu_p];

est_ord(ind) = est;
subplot(3, 1, 3)
imagesc(reshape(est_ord, [n,n]))
hold on
c = 'red';
title('X_{pred} ML')
scatter(loc(ind_o, 1), loc(ind_o, 2), c)

%%
function X = SIM(loc, Z, beta1, beta2)
    X = beta1 + loc(:,1) * beta2 + Z;
end