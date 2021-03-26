function Sigma = spherical_covariance(h,sigma,theta)
% spherical_covariance(h,theta,n) computes the spherical covariance
% function at the distances given in the vector of matrix h. sigma^2 is the
% variance and theta is the correlation length.
%
% See also euclidshat_covariance
%
% David Bolin (david.bolin@chalmers.se) 2018.

Sigma = zeros(size(h,1),size(h,2));
nz = h<theta;
hs = h(nz)/theta;
Sigma(nz) = sigma^2*(1-1.5*hs + 0.5*hs.^3);
Sigma = sparse(Sigma);

