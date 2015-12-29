#
# Statistics Project 2
#
# You will perform a statistical analysis to establish whether race has a significant impact on the rate of callbacks for resumes.

# Parameter of interest:  difference in callback rates in the population at large between black and white applicants
# Point estimate:         difference in callback rates in the sample of black and white applicants

# Answer the following questions in this notebook below and submit to your Github account. 
# 1.What test is appropriate for this problem? Does CLT apply
# 2.What are the null and alternate hypotheses?
# 3.Compute margin of error, confidence interval, and p-value.
# 4.Discuss statistical significance.
#
# Resources: 
# http://www.stat.columbia.edu/~martin/W2024/R2.pdf
# https://stat.ethz.ch/R-manual/R-devel/library/stats/html/p.adjust.html
#
#

library(stats)
library(foreign)

# load the data
# setwd("~/sliderule/statistics_project2/statistics project 2")
setwd("~/apps/sliderule/statistics_project2/statistics project 2")
data <- read.dta('data/us_job_market_discrimination.dta')

# We're going to use the inference() function provided by DataCamp
load(url("http://assets.datacamp.com/course/dasi/inference.Rdata"))

# 1.What test is appropriate for this problem? Does CLT apply
# check condition: samples are independent (assume yes)
# check condition: 10% population (total population of black/white applicants in country is >10x of sample)
# check condition: success and failure cases >10 each (yes)

# Transform the data
data$call <- as.logical(data$call)
# Create subsets for comparison between blacks and whites
black <- subset(data, data$race=="b")
white <- subset(data, data$race=="w")
nrow(black)
nrow(white)
# same number of rows: 2435

# 2.What are the null and alternate hypotheses?
# H0 = there is no difference between callback rates on resumes from blacks vs. whites 
# HA = there is a difference between callback rates
#
# Conclusion: There is a significant difference in callback rates, so we reject the null
#
# Contrast t.test() with prop.test()
t.test(x=black$call, y=white$call, alternative = "two.sided", mu = 0, var.equal = TRUE)
# why does result differ when x & y switched?
t.test(black$call, white$call, alternative = "two.sided", mu = 0, var.equal = FALSE)
#
# Test for normality - how do we test for normality?
#
# Here we are testing for normality, but are these acceptable/interpretable results?
qqnorm(black$call)
qqline(black$call)

qqnorm(white$call)
qqline(white$call)
# 
# What exactly is t.test() measuring? numeric data
# Is prop.test() more appropriate? YES, measuring call back logical (Y/N) across populations
#
# from ?prop.test(): 
# - If p is NULL and there is more than one group, the null tested is that the proportions in each group are the same.
# - correct: a logical indicating whether Yates' continuity correction should be applied where possible.
#
table(data$race, data$call)
prop.test(table(data$race, data$call), alternative = "two.sided", conf.level = 0.95, correct = FALSE)
#
# The 95% confidence interval estimate of the difference between "non-call" back rate of
# black to white applicants is (0.01677773, 0.04728798)
# In other words, at 95% CI black applicants 1.68% to 4.73% greater
#

# 3.Compute margin of error, confidence interval, and p-value.
#
# http://www.r-tutor.com/elementary-statistics/interval-estimation/interval-estimate-population-proportion
#
# 
call.response = na.omit(data$call)
n = length(call.response); n
# [1] 4870
k = sum(data$race=="b" & data$call); k
# [1] 2435
pbar = k/n; pbar
# [1] 0.03223819
SE = sqrt(pbar*(1-pbar)/n); SE
# [1] 0.002531076
MOE = qnorm(.975)*SE; MOE
# [1] 0.004960817
pbar + c(-MOE,MOE)
# [1] 0.02727738 0.03719901


# inference(black$call, white$call, est = "proportion", type = "ci", conflevel = 0.95, boot_method = "perc", method = "theoretical", success = TRUE)

# 4.Discuss statistical significance.
#
# Alternative hypothesis supported that there is a difference in callback rates at 95% CI
#

# We use the z-score test statistic assuming normality
inference(y=black$call, x=white$call, est = "proportion", type = "ht", conflevel = 0.95, boot_method = "perc", method = "theoretical", alternative = "twosided", success = TRUE, null = 0)
# TODO: Why are inference() results different from prop.test()?


