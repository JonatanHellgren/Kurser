function [p l]=normmix_loglike(x,pars)
% NORMMIX_loglike Compute class probabilities for a Gaussian mixture model.
%
% p=normmix_em(x,theta,prior)
%
% Input:
% x: n-by-d matrix
% theta{k}.mu: 1-by-d matrix, class expected value.
% theta{k}.Sigma: d-by-d matrix, class covariance.
% prior: 1-by-K matrix with the class probabilities.
%
% Output:
% p: The posterior class probabilities, n-by-K matrix.

[n,d] = size(x);
K = length(pars.mu);

% calculate log-probabilites for each class
p = zeros(n,1); 

xt = x';

for k=1:K
  p = p + pars.p(k)*mvnpdf(x,pars.mu{k},pars.Sigma{k});
end
ll = sum(log(p));
