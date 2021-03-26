function m = central_moment(x,p,q,scale_invariant)
% m = central_moment(x,p,q) computes the central moment of order
% (p,q) for the image x.
%
% Inputs:
%  x : the image (mxn matrix).
%  p,q: the order of the moment.
%  scale_invariant : Set to 1 to get scale invariant moments, by default 0.
%
% David Bolin (david.bolin@chalmers.se) 2018

if nargin < 4
  scale_invariant = 0;
end

m10 = image_moment(x,1,0);
m01 = image_moment(x,0,1);
m00 = image_moment(x,0,0);

ibar = m10/m00;
jbar = m01/m00;

[i, j] = ndgrid(1:size(x,1),1:size(x,2));
m = sum(sum(((i-ibar).^p).*((j-jbar).^q).*x));

if scale_invariant
  m = m/m00^(1+(p+q)/2);
end
