function pars=cov_ls_est(data,cov,variogram,fixed)
% pars=cov_ls_est(data,cov,variogram) does weighted least squares
% covariance estimation for data. Here cov is the name of the desired
% covariance model (one of 'matern', 'exponential', 'gaussian', or
% 'spherical'). variogram is a binned estimate of the semivariogram on the
% format given by the output of emp_variogram
%
% pars=cov_ls_est(...,fixed) specifies parameter of the parametric
% covariance model that should be kept fixed during the estimation. For
% example, if cov = 'matern', using fixed = struct('nu',1) will fix the
% smoothness parameter to one. 
%
% See also emp_variogram, cov_ml_est
%
% David Bolin (david.bolin@chalmers.se) 2018


if nargin < 4; fixed = []; end
if nargin < 3; error('Too few input parameters.'); end

if ~isempty(fixed) && ~isstruct(fixed)
  error('fixed should be a struct.')
end
%select covariance function
covf = select_covariance(cov, fixed);

%set initial values for parameters
[p0, names] = init_cov_est(cov, fixed, max(variogram.h), var(data));

%minimize loss function 
par = fminsearch(@(x) WLS_loss(x), log(p0));

%extract parameters
pars = fixed;
for i = 1:length(names)
  pars.(names{i}) = exp(par(i));
end

function S=WLS_loss(p)
  
  %compute variogram
  if strcmp(names{end},'sigma_e') % nugget not fixed
    r = covf(variogram.h,exp(p(1:end-1)));
    r0 = exp(2*p(end)) + covf(0,exp(p(1:end-1)));
  else
    r = covf(variogram.h(variogram.N>0),exp(p));
    r0 = (fixed.('sigma_e'))^2 + covf(0,exp(p));
  end
  v = r0 - r;
  w = variogram.N./v.^2;
  if 0
  figure(1);clf
  plot(variogram.h,variogram.variogram,'o')
  hold on
  plot(variogram.h,v)
  drawnow
  pause(0.1)
  end
  %compute loss function
  S = sum(w(variogram.N>0).*(variogram.variogram(variogram.N>0)-v(variogram.N>0)).^2);
end
end