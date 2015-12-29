
#
# Stats in R examples:
#

# http://www.r-tutor.com/elementary-statistics/hypothesis-testing/two-tailed-test-population-proportion
#
# 1. Calculate test statistic
#
pbar = 

# http://www.r-tutor.com/elementary-statistics/hypothesis-testing/two-tailed-test-population-mean-unknown-variance
#
# Suppose the mean weight of King Penguins found in an Antarctic colony last year was 15.4 kg. 
# In a sample of 35 penguins same time this year in the same colony, the mean penguin weight is 14.6 kg. 
# Assume the sample standard deviation is 2.5 kg. At .05 significance level, can we reject the null hypothesis 
# that the mean penguin weight does not differ from last year?
#
# 1. Calculate test statistic
xbar = 14.6            # sample mean 
mu0 = 15.4             # hypothesized value 
s = 2.5                # sample standard deviation 
n = 35                 # sample size 
t = (xbar-mu0)/(s/sqrt(n)) 
t                      # test statistic
# [1] -1.893146

# 2a. Calculate critical value
alpha = .05 
t.half.alpha = qt(1-alpha/2, df=n-1) 
c(-t.half.alpha, t.half.alpha) 
# [1] -2.032245  2.032245
# Conclusion: cannot reject null since test statistic lies within critical value interval

# 2b. Apply pt to compute 2-tailed p-value of t-stat  
pval = 2*pt(t, df=n-1)  # lower tail 
pval                      # two−tailed p−value
# [1] 0.06687552
# Conclusion: cannot reject null since pval > significance level

http://www.r-tutor.com/elementary-statistics/hypothesis-testing/two-tailed-test-population-proportion