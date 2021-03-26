function covf = select_covariance(cov,fixed)
% select_covariance(cov,fixed) is an internal function used by cov_ls_est
% and cov_ml_est.
%
% David Bolin (david.bolin@chalmers.se) 2018. 

sigma_fixed = 0;
kappa_fixed = 0;
rho_fixed = 0;
nu_fixed = 0;
theta_fixed = 0;
if ~isempty(fixed)
  names = fieldnames(fixed);
  for i = 1:length(names)
    if strcmp(names(i),'sigma')
      sigma_fixed = 1;
    elseif strcmp(names(i),'kappa')
      kappa_fixed = 1;
    elseif strcmp(names(i),'rho')
      rho_fixed = 1;
    elseif strcmp(names(i),'nu')
      nu_fixed = 1;
    elseif strcmp(names(i),'theta')
      theta_fixed = 1;
    end
  end
end
switch cov
	case 'exponential'
    if sigma_fixed == 0 && kappa_fixed == 0
      covf = @(d,x) exponential_covariance(d,x(1),x(2));
    elseif sigma_fixed == 1 && kappa_fixed == 0
      covf = @(d,x) exponential_covariance(d,fixed.('sigma'),x(1));
    elseif sigma_fixed == 0 && kappa_fixed == 1
      covf = @(d,x) exponential_covariance(d,x(1),fixed.('kappa'));
    else
      covf = @(d,x) exponential_covariance(d,fixed.('sigma'),fixed.('kappa'));
    end
	case 'gaussian'
    if sigma_fixed == 0 && rho_fixed == 0
      covf = @(d,x) gaussian_covariance(d,x(1),x(2));
    elseif sigma_fixed == 1 && rho_fixed == 0
      covf = @(d,x) gaussian_covariance(d,fixed.('sigma'),x(1));
    elseif sigma_fixed == 0 && rho_fixed == 1
      covf = @(d,x) gaussian_covariance(d,x(1),fixed.('rho'));
    else
      covf = @(d,x) gaussian_covariance(d,fixed.('sigma'),fixed.('rho'));
    end
	case 'matern'
		covf = @(d,x) matern_covariance(d,x(1),x(2),x(3));
    if sigma_fixed == 0 && kappa_fixed == 0 && nu_fixed == 0
      covf = @(d,x) matern_covariance(d,x(1),x(2),x(3));
    elseif sigma_fixed == 1 && kappa_fixed == 0 && nu_fixed == 0
      covf = @(d,x) matern_covariance(d,fixed.('sigma'),x(2),x(3));
    elseif sigma_fixed == 0 && kappa_fixed == 1 && nu_fixed == 0
      covf = @(d,x) matern_covariance(d,x(1),fixed.('kappa'),x(3));
    elseif sigma_fixed == 0 && kappa_fixed == 0 && nu_fixed == 1
      covf = @(d,x) matern_covariance(d,x(1),x(2),fixed.('nu'));
    elseif sigma_fixed == 1 && kappa_fixed == 1 && nu_fixed == 0
      covf = @(d,x) matern_covariance(d,fixed.('sigma'),fixed.('kappa'),x(1));
    elseif sigma_fixed == 1 && kappa_fixed == 0 && nu_fixed == 1
      covf = @(d,x) matern_covariance(d,fixed.('sigma'),x(1),fixed.('nu'));
    elseif sigma_fixed == 0 && kappa_fixed == 1 && nu_fixed == 1
      covf = @(d,x) matern_covariance(d,x(1),fixed.('kappa'),fixed.('nu'));
    elseif sigma_fixed == 1 && kappa_fixed == 1 && nu_fixed == 1
      covf = @(d,x) matern_covariance(d,fixed.('sigma'),fixed.('kappa'),fixed.('nu'));      
    end
  case 'spherical'
    if sigma_fixed == 0 && theta_fixed == 0
      covf = @(d,x) spherical_covariance(d,x(1),x(2));
    elseif sigma_fixed == 1 && theta_fixed == 0
      covf = @(d,x) spherical_covariance(d,fixed.('sigma'),x(1));
    elseif sigma_fixed == 0 && theta_fixed == 1
      covf = @(d,x) spherical_covariance(d,x(1),fixed.('theta'));
    else
      covf = @(d,x) spherical_covariance(d,fixed.('sigma'),fixed.('theta'));
    end
	otherwise
		error('Unknown covariance function.')
end
