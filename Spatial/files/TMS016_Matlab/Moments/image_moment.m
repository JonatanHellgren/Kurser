function m = image_moment(x,p,q)

% m = image_moment(x,p,q) computes the moment of order (p,q) for the image x.
% Inputs:
%  x : the image (mxn matrix).
%  p,q: the order of the moment.
%
% David Bolin (david.bolin@chalmers.se) 2018

[i j] = ndgrid(1:size(x,1),1:size(x,2));
m = sum(sum((i.^p).*(j.^q).*x));
