function [step,grad] = normmix_gradient(pars, y, P)
% [step,grad] = normmix_gradient(pars, y, P) calculates the gradients of
% the likelihood of a Gaussian mixture model. pars is a structure with the
% parameter of the model:
%   pars.mu : a cell with the mean values for each class.
%   pars.Sigma: a cell with the covariance matrices for each class.
%   pars.p : a cell with the class probabilities.
% y is an n x d matrix with the data, and P are the posterior class
% probabilities.
%
% David Bolin (david.bolin@chalmers.se) 2018.


K = length(pars.mu);
[n, d] = size(y);

D = duplicatematrix(d);

step = struct;
step.mu = cell(1,K);
step.Sigma = cell(1,K);
step.alpha = zeros(1,K);

grad = struct;
grad.mu = cell(1,K);
grad.Sigma = cell(1,K);
grad.alpha = zeros(1,K);

for k = 1:K
  %compute gradients of mu
  Qk = inv(pars.Sigma{k});
  z_k = P(:,k);
  yc = bsxfun(@minus, y, pars.mu{k}');
  Syc = yc*Qk;
  dmu = sum(bsxfun(@times,z_k , Syc));
  sum_z_k = sum(z_k);
  ddmu = -sum_z_k*Qk;
  
  %compute gradients of Sigma
  Syc_z = bsxfun(@times,z_k , Syc);

  dSigma = (Syc_z'*Syc)/2;
  dSigma = D'*dSigma(:);
  dSigma = dSigma -sum_z_k*D'*Qk(:)/2;
  ddSigma = -(sum_z_k/2) * D' * kron(Qk ,Qk) * D;

  dmuSigma = Qk*(kron( sum(Syc_z,1),eye(d))*D);
    
  H = [ddmu dmuSigma;dmuSigma' ddSigma];
  H = (H + H')/2;
  e = sort(eig(H));
  b = 1e-12;
  if e(end)/e(1) < b
    H = H + eye(size(H))*(b*e(1)-e(end))/(1-b);
  end
  grad.mu{k} = dmu(:)/n;
  grad.Sigma{k} = reshape(D*dSigma,[d d])/n;
  g_temp = [dmu(:); dSigma];
  p_temp = - H\g_temp;
  step.mu{k} = p_temp(1:d);
  step.Sigma{k} = reshape(D*p_temp(d+1:end),[d d]);
end
alpha =  prior_o_alpha(pars.p, 0);
[g_temp, p_temp] = gradient_alpha(alpha, P);
step.alpha = p_temp;
grad.alpha = g_temp;    
    

function [g, p] = gradient_alpha(alpha, p)

% computes the gradient and search direction of the probabilites using the
% transformation p_i = exp(\alpha_i) / sum (exp(\alpha_j))
%

g = zeros(size(alpha));
H = eye(length(alpha));
sum_exp = sum(exp(alpha));
p_sum = sum(p,1);
n = length(p(:,1));
g(2:end) = p_sum(2:end);
g(2:end) = g(2:end) - n*exp(alpha(2:end))/sum_exp;
H(2:end,2:end) = - n* diag(exp(alpha(2:end))/sum_exp);
H(2:end,2:end) =  H(2:end,2:end) + n * exp(alpha(2:end))*exp(alpha(2:end))' /sum_exp^2;
p = - H\g;
g = g /n;





function D = duplicatematrix(n)

% Creates the matrix D such that for a symmetric matrix one has
% D * vech*(A) = vec(A)
% where vech*(A) = [a_11 a_22 a_nn a_21 a 31 ... a_n-1n]
% thus first the diagonal entries, then the lower triangular entries
% comlunmn stacked
%

I = find(eye(n));
I2 = find(tril(ones(n,n),-1));
I3 = find(triu(ones(n,n), 1));
n_I = n;
n_I2 = n*(n-1)/2;
D = sparse([I;I2;I3],[1:n_I,n_I + (1:n_I2),n_I + (1:n_I2)]',1,n*n,n_I+n_I2);


