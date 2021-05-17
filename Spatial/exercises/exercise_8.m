cd('~/Kurser/Spatial/exercises')
addpath('../files/TMS016_Matlab')
tms016path;
%% Simulate a discrete Markov random field
K = 3;                                                                      %number of classes
sz = [100 100];                                                             %size of the image
N = [0 1 0;1 0 1;0 1 0];                                                    %Neighborhood structure
alpha = log(ones(1,K)/K);                                                   %alpha parameters
beta = 2*eye(K);                                                            %beta parameters                    

%set a starting value
x = randi(K,[sz(1) sz(2)]);                                                 
z0 = zeros(sz(1),sz(2),K);
for i=1:sz(1)
    for j=1:sz(2)
        z0(i,j,x(i,j)) = 1;
    end
end
%simulate z using Gibbs sampling
[z, Mz,ll] = mrf_sim(z0,N,alpha,beta,100,2);

%% Simulate some 3-dimensional Gaussian data and comibne into an image
yi = cell(1,K);
yi{1} = mvnrnd([1;0;0],0.2*eye(3),sz(1)*sz(2));
yi{2} = mvnrnd([0;1;0],0.2*eye(3),sz(1)*sz(2));
yi{3} = mvnrnd([0;0;1],0.2*eye(3),sz(1)*sz(2));
y = zeros([sz 3]);

for k=1:K
    y = y + bsxfun(@times,z(:,:,k),reshape(yi{k},[sz 3]));
end

%% 

opts = struct('plot',2,'N',N, 'common_beta',1);
[theta,alpha,beta,cl,p]=mrf_sgd(y,K,opts);
figure(3)
imagesc(cl)