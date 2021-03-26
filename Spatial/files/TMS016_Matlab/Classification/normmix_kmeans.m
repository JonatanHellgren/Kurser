function [idx,pars]=normmix_kmeans(x,K,maxiter,verbose)
% [idx,pars]=normmix_kmeans(x,K,maxiter,verbose) uses the K-means algorithm to
% estimate a Gaussian mixture model.
%
% Inputs:
% x: n-by-d matrix (column-stacked image with n pixels)
% K: number of classes
% maxiter: maximum number of iterations in algorithm
% verbose: set to 1 in order to print output
%
% Outputs:
% idx : the class numbers for each pixel in the image.
% theta{k}.mu: 1-by-d matrix, class expected value.
% theta{k}.Sigma: d-by-d matrix, class covariance.
%
% David Bolin (david.bolin@chalmers.se) 2018

% Parse input parameters
if nargin < 4; verbose = 0; end
if nargin<3, maxiter = []; end
if isempty(maxiter), maxiter = 1; end

if verbose >0
  [idx,theta] = kmeans(x,K,'MaxIter',maxiter,'Display','iter');
else
  [idx,theta] = kmeans(x,K,'MaxIter',maxiter);
end
pars = struct;
pars.mu = cell(1,K);
pars.Sigma = cell(1,K);
pars.p = ones(1,K)/K;
[n,d] = size(x);
sigma2 = 0;
for k=1:K
  pars.mu{k} = theta(k,:)';
  y = x(idx==k,:)-repmat(pars.mu{k}',[sum(idx==k),1]);
  sigma2 = sigma2 + sum(sum(y.*y,1),2);
end
Sigma = sigma2*eye(d)/n/d;
for k=1:K
  pars.Sigma{k} = Sigma;
end

