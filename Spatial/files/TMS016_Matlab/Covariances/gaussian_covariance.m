function Sigma = gaussian_covariance(h,sigma,rho)
% gaussian_covariance(h,sigma,rho) computes the gaussian covariance
% function C(h) = sigma^2 * exp(-h^2/rho) at the distances given
% in the vector or matrix h. All parameters of the covariance function are
% postive. sigma^2 is the variance and rho is the practical correlation
% length.
%
% See also matern_covariance
%
% David Bolin (david.bolin@chalmers.se) 2018.

if nargin < 3; error('Too few input parameters'); end
if sigma<=0; error('sigma must be postive'); end
if rho<=0; error('rho must be postive'); end

%compute range
hpos = h>0;
Sigma = zeros(size(h));
Sigma(~h) = sigma^2;

[hunique,~,J] = unique(h(hpos));
B = sigma^2*exp(-2*(hunique/rho).^2);
Sigma(hpos) = B(J);

