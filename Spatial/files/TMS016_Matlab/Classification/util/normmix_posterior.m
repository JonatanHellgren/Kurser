function p = normmix_posterior(x,pars)
% p = normmix_posterior(x,pars) computes class probabilities for a Gaussian mixture model estimated using normmix_sgd.
%
% Input:
% x: n-by-d matrix with values to be classified.
% pars : result object obtained by running normmix_sgd.
%
% Output:
% p: The posterior class probabilities, n-by-K matrix.
%
% David Bolin (david.bolin@chalmers.se) 2018

[n,d] = size(x);
K = length(pars.mu);

% calculate log-probabilites for each class
p = zeros(n,K);

xt = x';
for k=1:K
  y = bsxfun(@minus,xt,pars.mu{k});
  v = pars.Sigma{k} \ y;
  v = sum(v .* y , 1);
  p(:,k) = -0.5*v - log(det(pars.Sigma{k}))/2 - (d/2)*log(2*pi);
end

%add prior information and transform to linear scale
p = bsxfun(@plus,p,log(pars.p));
p = bsxfun(@minus,p,max(p,[],2));
p = exp(p);
p = bsxfun( @rdivide, p, sum(p,2) );

