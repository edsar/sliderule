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
setwd("~/sliderule/statistics_project2/statistics project 2")
data <- read.dta('data/us_job_market_discrimination.dta')

# Use inference function provide by DataCamp
load(url("http://assets.datacamp.com/course/dasi/inference.Rdata"))

# clean data
data$call <- as.logical(data$call)

# subset for comparison
black <- subset(data, data$race=="b")
white <- subset(data, data$race=="w")

# 1.What test is appropriate for this problem? Does CLT apply
# check condition: samples are independent (assume yes)
# check condition: 10% population (total population of black/white applicants in country is >10x of sample)

# check condition: success and failure cases >10 each (yes)
nrow(black)
nrow(white)
# same number of rows: 2435

# 2.What are the null and alternate hypotheses?
# H0 = there is no difference between callback rates on resumes from blacks vs. whites 
# HA = there is a difference between callback rates
#
# Conclustion: There is a significant difference in callback rates, reject null
#
# TODO: Contract t.test() with inference()

t.test(black$call, white$call, alternative = "less", mu = 0, var.equal = TRUE)
t.test(black$call, white$call, alternative = "less", mu = 0)

# 3.Compute margin of error, confidence interval, and p-value.
#
# Conclusion: At 95% CI, callback rate to black applicants is lower by 23.08 to 35.18%
#
# TODO: Can we do multiple tests and use p-adjust to deal with FWER and FDR? 

inference(black$call, white$call, est = "proportion", type = "ci", conflevel = 0.95, boot_method = "perc", method = "theoretical", success = TRUE)

# 4.Discuss statistical significance.
#
# Alternative hypothesis supported that there is a difference in callback rates at 95% CI
#
# Conclusion: 
#
# TODO: Can we do multiple tests and use p-adjust to deal with FWER and FDR?

inference(black$call, white$call, est = "proportion", type = "ht", conflevel = 0.95, boot_method = "perc", method = "theoretical", alternative = "less", success = TRUE, null = 0)


