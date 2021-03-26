function pars=cov_ml_est(data,cov,loc,X,fixed,reml)
% pars=cov_ls_est(data,cov,loc) does maximum likelihood estimation of a
% model data(s) = u(s) + e(s), where u is a mean-zero Gaussian field with
% covariance specified by cov (one of 'matern','exponential', 'spherical',
% or 'gaussian') and e(s) is independent measurement noise with standard
% deviation sigma_e. loc are the measurement locations.
%
% pars=cov_ls_est(data,cov,loc,X) does maximum likelihood estimation of a
% model data(s) = X(s)*beta + u(s) + e(s), where X(s) are covariates for
% the mean. The input X is a matrix with the covariates evaluated at the
% measurement locations. 
%
% pars=cov_ls_est(...,fixed) specifies parameter of the parametric
% covariance model that should be kept fixed during the estimation. For
% example, if cov = 'matern', using fixed = struct('nu',1) will fix the
% smoothness parameter to one. fixed = struct('sigma_e',0) corresponds to
% a model without any measurement noise. 
%
% pars=cov_ls_est(...,fixed,reml) specifies whether REML estimation should
% be used instead of profile-likelihood estimation (default is false).
%
% See also cov_ls_est
%
% David Bolin (david.bolin@chalmers.se) 2018

if nargin < 6; reml = 0; end
if nargin < 5; fixed = []; end
if nargin < 4; X = []; end
if nargin < 3; error('Too few input parameters.'); end

if isempty(X)
  n_cov = 0;
else
  n_cov = size(X,2);
end

if isempty(X) && reml > 0
  error('X must be supplied if REML is used.')
end

%select covariance function
covf = select_covariance(cov, fixed);

%compute distance matrix
D = squareform(pdist(loc));

%precompute identiy matrix
I = eye(size(loc,1));

%initial regression estimate of beta
if n_cov > 0
  e = data - X*((X'*X)\(X'*data));
  s2 = var(e);
else
  s2 = var(data);
end

%set initial values for parameters
[p0, names] = init_cov_est(cov, fixed, max(D(:)), s2);

%minimize loss function 
par = fminsearch(@(x) log_like(x), log(p0));
options = optimoptions(@fminunc,'Display','none','Algorithm','quasi-newton');
par = fminunc(@(x) log_like(x), par,options);

%extract parameters
pars = fixed;
for i = 1:length(names)
  pars.(names{i}) = exp(par(i));
end

%compute regression coefficients
if strcmp(names{end},'sigma_e') % nugget not fixed
  Sigma = covf(D,exp(par(1:end-1))) + exp(2*par(end))*I;
else
  Sigma = covf(D,exp(par)) + (fixed.sigma_e)^2*I;
end
if n_cov > 0
  pars.beta = (X'*(Sigma\X))\(X'*(Sigma\data));
end

function ll=log_like(p)
  
  %compute covariance matrix 
  if strcmp(names{end},'sigma_e') % nugget not fixed
    Sigma = covf(D,exp(p(1:end-1))) + exp(2*p(end))*I;
  else
    Sigma = covf(D,exp(p)) + (fixed.sigma_e)^2*I;
  end
  
  %compute Cholesky factor, if it fails, return large value
  [R,p] = chol(Sigma);
  if p>0 
    ll = realmax;
    return
  end
  
  SiY = R\(R'\data); 
  
  if n_cov > 0
    SiX = R\(R'\X);
    v = SiY - SiX*((X'*SiX)\(X'*SiY));
  else 
    v = SiY;
  end
  ll = -sum(log(diag(R))) -0.5*data'*v;
  
  if reml == 1 && n_cov > 0
    [Rreml,p] = chol(X'*SiX);
    if p>0 
      ll = realmax;
      return
    end
    ll = ll - sum(log(diag(Rreml)));
  end
  ll = -ll;
end
end