function Sigma = exponential_covariance(h,sigma,kappa)
% exponential_covariance(h,sigma,kappa) computes the exponential
% covariance function C(h) = sigma^2 * exp(-kappa*h) at the distances given
% in the vector or matrix h. All parameters of the covariance function are
% postive. sigma^2 is the variance and kappa decides the practical
% correlation length r through r=2/kappa.
%
% See also matern_covariance
%
% David Bolin (david.bolin@chalmers.se) 2018.

if nargin < 3; error('Too few input parameters'); end
if kappa<=0; error('kappa must be postive'); end
if sigma<=0; error('sigma must be postive'); end

hpos = h>0;
Sigma = zeros(size(h));
Sigma(~h) = sigma^2;
[hunique,~,J] = unique(h(hpos));
B = sigma^2*exp(-kappa*hunique);
Sigma(hpos) = B(J);


