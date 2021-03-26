function [cl,p]=normmix_classify(x,pars)
% [cl,p]=normmix_classify(x,pars) classifies an image based on a
% Gaussian mixture model estimated using normmix_sgd.
%
% Input:
% x: n-by-d matrix with values to be classified.
% pars : result object obtained by running normmix_sgd.
%
% Output:
% cl: n-by-1 vector containing the classes for each pixel.
% p: The posterior class probabilities, n-by-K matrix.
%
% David Bolin (david.bolin@chalmers.se) 2018

p = normmix_posterior(x,pars);

[tmp,cl] = max(p,[],2);

