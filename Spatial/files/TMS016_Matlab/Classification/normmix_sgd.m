function [pars,traj]=normmix_sgd(x,K,Niter,step0,plotflag)
% [pars,traj]=normmix_sgd(x,K,Niter,step0,plotflag) uses gradient-descent
% optimization to estimate a Gaussian mixture model.
%
% Inputs:
% x: n-by-d matrix (column-stacked image with n pixels)
% K: number of classes
% Niter: Number of iterations to run the algorithm
% step0: The initial step size
% plotflag: if 1, then parameter tracks are plotted
%
% Outputs:
% pars : A structure containing the estimated parameters.
% traj : the parameter trajectories.
%
% David Bolin (david.bolin@chalmers.se) 2018

if nargin < 3; Niter = 100; end
if nargin < 4; step0 = 1; end
if nargin < 5; plotflag = 0; end

[n,d] = size(x);

%obtain some reasonable starting values using K-means
[idx,pars] = normmix_kmeans(x,K,Niter);

%setup output objects
if nargout>1 || plotflag > 0
  traj = struct;
  traj.mu = zeros(Niter, d, K);
  traj.sigma = zeros(Niter,d*(d+1)/2,K);
  traj.p = zeros(Niter, K);
end
if plotflag > 0
  figure
  ll = zeros(Niter,1);
end

for i=1:Niter
  %Compute posterior probabilities
  p_tmp = normmix_posterior(x, pars);

  %Compute gradients
  [step, grad] = normmix_gradient(pars, x, p_tmp);

  %take step
  tic
  gamma = step0;
  for k = 1:K
    pars.Sigma{k} = pars.Sigma{k} + gamma*step.Sigma{k};
    pars.Sigma{k} = (pars.Sigma{k} +pars.Sigma{k}')/2; %make sure symmetric
    pars.mu{k} = pars.mu{k} + gamma*step.mu{k};
  end
  alpha =  prior_o_alpha(pars.p, 0);
  alpha = alpha + gamma*step.alpha;
  pars.p = prior_o_alpha(alpha, 1)';

  %save sample paths
  if nargout>1 || plotflag > 0
    for k=1:K
      traj.mu(i,:,k) = pars.mu{k};
      traj.sigma(i,:,k) = vech(pars.Sigma{k});
    end
    traj.p(i,:) = pars.p;
  end

  if plotflag>0
    ll(i)=normmix_loglike(x,pars);
    subplot(221);
    plot(reshape(squeeze(traj.mu(1:i,:,:)),[i K*d]))
    title('Means')
    subplot(222);
    plot(reshape(squeeze(traj.sigma(1:i,:,:)),[i K*d*(d+1)/2]))
    title('Covariances')
    subplot(223);
    plot(traj.p(1:i,:))
    title('Class probabilities')
    subplot(224)
    plot(ll(1:i))
    title('log-likelihood')
    drawnow
  end
end

function h = vech(m)
% h = vech(m)
% h is the column vector of elements on or below the main diagonal of m.
% m must be square.

r = repmat((1:size(m,1))', 1, size(m,2));
c = repmat(1:size(m,2), size(m,1), 1);
% c <= r is same as tril(ones(size(m)))
h = m(find(c <= r));

function ll=normmix_loglike(x,pars)
% compute the log-likelihood

[n,d] = size(x);
K = length(pars.mu);

p = zeros(n,1);
for k=1:K
  p = p + pars.p(k)*mvnpdf(x,pars.mu{k}',pars.Sigma{k});
end
ll = sum(log(p));

