cd('~/Kurser/Spatial/exercises')
addpath('../files/TMS016_Matlab')
tms016path;
%%
clf
m = 100;
kappa = 1;
q1 = kappa^2*[0 0 0;0 1 0;0 0 0] + [0 -1 0; -1 4 -1;0 -1 0];

dot_ind = 1:12:10000;
smiley_ind = [5050, 4050, 3860, 3961, 4062, 4162, 4163, 4263, 4363, 4463, 4563, 4663, 4763, 4863, 4963, 4962, 5062, 5161, 5260];

subplot(1,2,1)
c = plotGMFR(q1, m, smiley_ind);
imagesc(reshape(c, [m, m]))
title('smiely')

subplot(1,2,2)
c = plotGMFR(q1, m, dot_ind);
imagesc(reshape(c, [m, m]))
title('dots')
%%
clf
q2 = kappa^2*[0 0 0;0 1 0;0 0 0] + [-10 -0.1 0; -0.1 20.4 -0.1;0 -0.1 -10];

subplot(1,2,1)
c = plotGMFR(q2, m, smiley_ind);
imagesc(reshape(c, [m, m]))
title('smiely')
    
subplot(1,2,2)
c = plotGMFR(q2, m, dot_ind);
imagesc(reshape(c, [m, m]))
title('dots')

%%
clf
q3 = kappa^2*[0 0 0;0 1 0;0 0 0] + [0 -1 -10; -1 24 -1;-10 -1 0];

subplot(1,2,1)
c = plotGMFR(q3, m, smiley_ind);
imagesc(reshape(c, [m, m]))
title('smiely')

subplot(1,2,2)
c = plotGMFR(q3, m, dot_ind);
imagesc(reshape(c, [m, m]))
title('dots')

%%
clf
z = randn(m^2, 1);

subplot(2, 2, 1)
imagesc(reshape(z, [m, m]))
title('z, random noise')

subplot(2,2,2)
imagesc(reshape(apply_stencil(q1, m, z), [m, m]))
title('q_1')

subplot(2,2,3)
imagesc(reshape(apply_stencil(q2, m, z), [m, m]))
title('q_2')

subplot(2,2,4)
imagesc(reshape(apply_stencil(q3, m, z), [m, m]))
title('q_3')

%%
clf
m = 100;
kappa = 1;
qb1 = kappa^2*[0 0 0 0 0;0 0 0 0 0;0 0 1 0 0;0 0 0 0 0;0 0 0 0 0] + [0 0 -1 0 0;0 0 -1 0 0;-1 -1 4 -1 -1;0 0 -1 0 0;0 0 -1 0 0;];

subplot(2,2,1)
c = plotGMFR(q1, m, smiley_ind);
imagesc(reshape(c, [m, m]))
title('smiely')

subplot(2,2,2)
c = plotGMFR(qb1, m, smiley_ind);
imagesc(reshape(c, [m, m]))
title('smiely')

subplot(2,2,3)
c = plotGMFR(q1, m, dot_ind);
imagesc(reshape(c, [m, m]))
title('dots')

subplot(2,2,4)
c = plotGMFR(qb1, m, dot_ind);
imagesc(reshape(c, [m, m]))
title('dots')

%%
clf
Q = stencil2prec([m, m],q1);
Q11 = Q * Q;
Q1111 = Q11 * Q11;
R = chol(Q11);
x = R\z;
N = 5000;

rng(123)
ind = randperm(m^2);
ind_obs = ind(1:N);
ind_mis = ind(N+1:end);
x_obs = x(ind_obs);
x_mis = x(ind_mis);

subplot(2,2,1)
imagesc(reshape(x, [m,m]))

sample_x(ind) = [x(ind_obs); zeros(m^2 - N, 1)];
subplot(2,2,2)
imagesc(reshape(sample_x, [m, m]))


Qop = Q11(ind_mis, ind_obs);
Qo = Q11(ind_obs, ind_obs);
Qp = Q11(ind_mis, ind_mis);

mu_A = 0;
mu_B = mean(x_obs);
post_mean = mu_A - inv(Qp)*Qop*(x_obs - mu_B);

subplot(2,2,3)
reconstructed_x(ind) = [x(ind_obs); post_mean];
imagesc(reshape(reconstructed_x, [m, m]))
%%
clf
jens = imread('~/trams/images/other/IMG_20210416_143255.png');
mean_jens = mean(jens,3);
gray_jens = reshape(double(mean_jens)/255, [320*240, 1]);

N = 50000;
Q = stencil2prec([320, 240],q3);

subplot(2,2,1)
imagesc(reshape(gray_jens, [320, 240]))

rng(123)
ind = randperm(320 * 240);
ind_obs = ind(1:N);
ind_mis = ind(N+1:end);
x_obs = gray_jens(ind_obs);
x_mis = gray_jens(ind_mis);



sample_x(ind) = [x_obs; zeros(320 * 240 - N, 1)];
subplot(2,2,2)
imagesc(reshape(sample_x, [320, 240]))

Qop = Q(ind_mis, ind_obs);
Qo = Q(ind_obs, ind_obs);
Qp = Q(ind_mis, ind_mis);

mu_B = mean(x_obs);
mu_A = mu_B;
post_mean = mu_A - inv(Qp)*Qop*(x_obs - mu_B);

subplot(2,2,3)
reconstructed_x(ind) = [x_obs; post_mean];
imagesc(reshape(reconstructed_x, [320, 240]))

subplot(2,2,4)
reconstructed2_x(ind) = [x_obs; ones([320*240 - N, 1]) * mu_A];
imagesc(reshape(reconstructed2_x, [320, 240]))

%%
clf
sigma_e = 0.1;
noisy_jens = gray_jens + sigma_e*randn(240*320,1);
subplot(2, 2, 1)
imagesc(reshape(gray_jens, [320, 240]))

subplot(2, 2, 2)
imagesc(reshape(noisy_jens, [320, 240]))
%%
function x = apply_stencil(q, m, z)
    Q = stencil2prec([m, m],q);
    R = chol(Q);
    x = R\z;
end
%% 
function c = plotGMFR(stencil, m, ind)
    Q = stencil2prec([m, m],stencil);
    v = zeros(m^2, 1);
    v(ind) = 1;
    c = Q\v;
end