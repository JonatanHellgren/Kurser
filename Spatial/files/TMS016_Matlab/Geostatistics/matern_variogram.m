function sv = matern_variogram(h,sigma,kappa,nu,sigma_e)
% matern_variogram(h,sigma,kappa,nu) computes the semivariogram
% corresponding to the matern covariance function 
% C(h) = (sigma^2/(2^(nu-1)*Gamma(nu))) * (kappa*h)^nu * K_v(kappa*h) 
% at the distances given in the vector h.
% sigma^2 is the variance, nu decides the smoothness of C(h) at h=0, and
% kappa decides the practical correlation length r through
% r=sqrt(8*nu)/kappa.
%
% matern_variogram(...,sigma_e) adds a nugget sigma_e^2 to the variogram. 
%
% See also matern_covariance
%
% David Bolin (david.bolin@chalmers.se) 2018.

if nargin < 4; sigma_e = 0; end
sv = sigma^2 + sigma_e^2 - matern_covariance(h,sigma,kappa,nu);
