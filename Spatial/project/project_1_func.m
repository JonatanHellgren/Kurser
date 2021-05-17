cd('~/Kurser/Spatial/project')
addpath('../files/TMS016_Matlab')
tms016path;
%%
rosetta = imread('images/rosetta.jpg');
rosetta = mean(rosetta,3);
rosetta = double(rosetta)/255;

titan = imread('images/titan.jpg');
titan = double(titan)/255;

img = rosetta;
p_c = 0.10;

main(img, p_c)
%%
function main(img, p_c)   
    % storing the dimnetions of the image
    [m, n] = size(img);
    
    % converting into a column vector
    x = reshape(img, [m*n, 1]);

    [ind_obs, ind_mis, loc_obs, N] = sample_pixels(p_c, m, n);
    x_obs = x(ind_obs);

    params = get_params(x_obs, loc_obs, N, m, n);


    Q = get_stencil(params.kappa, params.sigma, m, n);

    reconstruct_img(Q, ind_obs, ind_mis, x_obs, params.mu_p, params.mu_o, p_c, N, m, n);
end 

function [ind_obs, ind_mis, loc_obs, N] = sample_pixels(p_c, m, n)

    % calculating amount of pixels to remove
    rng(123)
    N = binornd(m*n, p_c);

    % selecting which pixels to keep with seed
    ind = randperm(m*n);

    % divding up the data in to convinent vectors
    ind_obs = ind(1:N);
    ind_mis = ind(N+1:end);

    % defining the locations for each pixel 
    [loc_x, loc_y] = meshgrid(1:m, 1:n);
    loc = [reshape(loc_x, [1, m*n]); reshape(loc_y, [1, m*n])]';

    loc_obs = loc(ind_obs,:);
end

function params = get_params(x_obs, loc_obs, N, m, n)
    N_sub = min(N,10000);
    B_obs = ones(N_sub,1);
    x_o = x_obs(1:N_sub);
    beta_OLS = (B_obs' * B_obs) \ B_obs' * x_o;
    residuals = x_o - B_obs * beta_OLS;

    binned_estimate = emp_variogram(loc_obs(1:N_sub,:), residuals, 50);
    params = cov_ls_est(residuals, 'matern', binned_estimate);

    params.mu_p = ones(m*n-N, 1) * beta_OLS;
    params.mu_o = ones(N, 1) * beta_OLS;
    
    plot_variogram(binned_estimate, params)
end

function Q = get_stencil(kappa, sigma, m, n)
    stencil = kappa^4 * [0 0 0 0 0; 0 0 0 0 0; 0 0 1 0 0; 0 0 0 0 0; 0 0 0 0 0] + ...
            2*kappa^2 * [0 0 0 0 0; 0 0 -1 0 0; 0 -1 4 -1 0; 0 0 -1 0 0; 0 0 0 0 0] + ...
                        [0 0 1 0 0; 0 2 -8 2 0; 1 -8 20 -8 1; 0 2 -8 2 0; 0 0 1 0 0];

    tau = 2 * pi / sigma^2;

    Q = tau *  stencil2prec([m, n],stencil);
end

function reconstruct_img(Q, ind_obs, ind_mis, x_obs, mu_p, mu_o, p_c, N, m, n)
    Qop = Q(ind_mis, ind_obs);
    Qp = Q(ind_mis, ind_mis);
    

    post_mean = mu_p - Qp\(Qop * (x_obs - mu_o));

    re_x([ind_obs, ind_mis]) = [x_obs; post_mean];    
    
    sampled_x([ind_obs, ind_mis]) = [x_obs; zeros(m*n-N, 1)];
    
    plot_reconstruction(re_x, sampled_x, p_c, m, n)
end

function plot_variogram(binned_estimate, params)
    clf 
    figure(1)
    % Binned estimate
    subplot(1,2,1)
    plot(binned_estimate.h, binned_estimate.variogram)
    title('Binned estimate')

    % matern estimate
    nu = 1; % specified in assignment text
    matern_est = matern_variogram(binned_estimate.h, params.sigma, params.kappa, nu, params.sigma_e);
    subplot(1,2,2)
    plot(binned_estimate.h, matern_est)
    title('Matern estimate')
end

function plot_reconstruction(re_x, sampled_x, p_c, m, n)

    figure(2)
    subplot(1,2,1)
    imagesc(reshape(sampled_x, [m, n]))
    title('Sampled p_c = '+string(p_c))
    colormap gray
    
    subplot(1,2,2)
    imagesc(reshape(re_x, [m, n]))
    title('Reconstructed p_c = '+string(p_c))
    colormap gray
    
end
