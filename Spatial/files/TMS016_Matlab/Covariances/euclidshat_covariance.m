function Sigma = euclidshat_covariance(h,sigma,theta,n)
% euclidshat_covariance(h,theta,n) computes the Eudlid's hat covariance
% function at the distances given in the vector of matrix h. sigma^2 is the
% variance, theta is the correlation length and n sets the shape of the
% covariance function. Note that it is only a valid covariance on R^d if n>=d.
%
% See also spherical_covariance
%
% David Bolin (david.bolin@chalmers.se) 2018.

if nargin < 3; error('Too few input parameters'); end
if sigma <= 0; error('sigma should be positive'); end
if theta <= 0; error('theta should be positive'); end

Sigma = zeros(size(h,1),size(h,2));

nz = h<theta;
hs = h(h<theta)/theta;
Sigma(nz) = sigma^2*betainc(1-hs.^2,(n+1)/2,1/2);
Sigma = sparse(Sigma);
