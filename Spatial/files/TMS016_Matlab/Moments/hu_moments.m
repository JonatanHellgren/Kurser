function m = hu_moments(x)
% m = hu_moments(x) computes the seven Hu moments for the image x.
% Inputs:
%  x : the image (mxn matrix).
% Outputs:
% m : a vector with the seven moments.
%
% David Bolin (david.bolin@chalmers.se) 2018

eta02 = central_moment(x,0,2,1);
eta03 = central_moment(x,0,3,1);

eta20 = central_moment(x,2,0,1);
eta30 = central_moment(x,3,0,1);

eta11 = central_moment(x,1,1,1);
eta21 = central_moment(x,2,1,1);
eta12 = central_moment(x,1,2,1);

m(1) = eta20 + eta02;
m(2) = (eta20 - eta02)^2 - 4*eta11^2;
m(3) = (eta30-3*eta12)^2 + (3*eta21-eta03)^2;
m(4) = (eta30+eta12)^2 + (eta21+eta03)^2;
m(5) = (eta30-3*eta12)*(eta30+eta12)*((eta30+eta12)^2 - 3*(eta21+eta03)^2)+...
       (3*eta21-eta03)*(eta21+eta03)*(3*(eta30+eta12)^2 - (eta21+eta03)^2);
m(6) = (eta20-eta02)*((eta30+eta12)^2 - (eta21+eta03)^2)+...
       4*eta11*(eta30+eta12)*(eta21+eta03);
m(7) = (3*eta21-eta03)*(eta30+eta12)*((eta30+eta12)^2-3*(eta21+eta03)^2) -...
       (eta30-3*eta12)*(eta21+eta03)*(3*(eta30+eta12)^2-(eta21+eta03)^2);



