function out = emp_variogram(D,data,N)
% out = emp_variogram(loc,data,N) computed a binned estimate of the
% semivariogram for spatial data. The input parameters are:
%
% D    : Measurement locations n x 2 matrix or distance matrix n x n.
% data : The measurements, n x 1 vector
% N    : The number of bins 
%
% out is a structure containing 
% variogram : The estimated semivariogram
% h         : The center points for each bin
% N         : Number of lags in each bin
%
% David Bolin (david.bolin@chalmers.se) 2018. 

if nargin < 3; error('Too few input parameters.'); end

if size(D,1) ~= size(D,2)
  D = squareform(pdist(D));
end
max_dist = max(D(:));
d = linspace(0,max_dist,N);
D(find(tril(D)))=-1;

out = struct;
out.h = (d(2:end)+d(1:end-1))/2;
out.variogram = zeros(1,N-1);
out.N = zeros(1,N-1);

for i=1:N-1
    [I,J] = find(d(i)< D & D<=d(i+1));
    out.N(i) = length(I);
    out.variogram(i) = 0.5*mean((data(I)-data(J)).^2);
end
