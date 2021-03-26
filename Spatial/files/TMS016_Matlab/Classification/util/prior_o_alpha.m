function prior_alpha = prior_o_alpha(prior_alpha, in_alpha)

% Internal function that change between parametrization [p_1,p_2, ...]
% and [alpha_1, alpha_2, ...] wgere p_i = exp(alpha_i) / sum(exp(alpha_j))
% alpha_1 = 0
%
    if in_alpha
        alpha = prior_alpha;
        prior = zeros(length(alpha),1);
        sum_exp = sum(exp(alpha));
        for i = 1:length(prior)
            prior(i) = exp(alpha(i))/sum_exp;
        end
        prior_alpha = prior;
    else
        prior = prior_alpha;
        alpha = zeros(length(prior),1);
        sum_exp = 1/prior(1);
        for i = 2:length(prior)
            alpha(i) = log(prior(i) * sum_exp);
        end
        prior_alpha = alpha;

    end

