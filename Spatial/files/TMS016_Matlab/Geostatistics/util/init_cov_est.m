function [p0, names] = init_cov_est(cov, fixed, d_max, s2)
% init_cov_est is an internal function used by cov_ls_est and cov_ml_est.

if strcmp(cov,'exponential')
  n_pars = 3;
  parameter_names = {'sigma','kappa','sigma_e'};
elseif strcmp(cov,'gaussian')
  n_pars = 3;
  parameter_names = {'sigma','rho','sigma_e'};
elseif strcmp(cov,'matern')
  n_pars = 4;
  parameter_names = {'sigma','kappa','nu','sigma_e'};
else
  error('Unknown covariance function.')
end

p0 = zeros(n_pars,1);
fixed_pars = zeros(n_pars,1);
if ~isempty(fixed)
  names = fieldnames(fixed);
  for i = 1:length(names)
    if strcmp(names(i),'sigma')
      p0(1) = fixed.(names{i});
      fixed_pars(1) = 1;
    elseif strcmp(names(i),'kappa')
      p0(2) = fixed.(names{i});
      fixed_pars(2) = 1;
    elseif strcmp(names(i),'nu')
      if strcmp(cov,'matern')
        p0(3) = fixed.(names{i});
        fixed_pars(3) = 1;
      end
    elseif strcmp(names(i),'sigma_e')
      p0(end) = fixed.(names{i});
      fixed_pars(end) = 1;
    else
      error('Unknown fixed parameter.')
    end
  end
end
%Set start value for variance parameters
if p0(1)== 0
  if p0(end) == 0 %no fixed parameters
    p0(1) = sqrt(s2*4/5);
    p0(end) = sqrt(s2/5);
  else %nugget fixed
    s2_start = s2 - p0(end)^2;
    if s2_start < 0
      warning('Nugget fixed to value larger than data variance.')
      s2_start = s2/5;
    end
    p0(1) = sqrt(s2_start);
  end
else %variance of field fixed
  if p0(end) ~= 0
    s2_start = s2 - p0(1)^2;
    if s2_start < 0
      s2_start = s2/5;
    end
    p0(end) = sqrt(s2_start);
  end
end

%set start value for smoothness
if strcmp('matern',cov)
  if p0(3) == 0
    p0(3) = 1;
  end
end

%Set start value for range parameter
if p0(2) == 0
  if strcmp('matern',cov)
    p0(2) = sqrt(8*p0(3))/(d_max/2);
  elseif strcmp('exponential',cov)
    p0(2) = 2/(d_max/2);
  elseif strcmp('gaussian',cov)
    p0(2) = d_max/2;
  end
end

p0 = p0(find(fixed_pars==0));
names = {parameter_names{find(fixed_pars==0)}};
