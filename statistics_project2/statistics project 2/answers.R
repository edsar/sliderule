library(stats)
library(foreign)

setwd("~/sliderule/statistics_project2/statistics project 2")

data <- read.dta('data/us_job_market_discrimination.dta')

black <- data[data$race=="b",]
white <- data[data$race=="w",]

t.test(black$call, white$call)

# 
# Welch Two Sample t-test
# 
# data:  black$call and white$call
# t = -4.1147, df = 4711.6, p-value = 3.943e-05
# alternative hypothesis: true difference in means is not equal to 0
# 95 percent confidence interval:
#   -0.04729503 -0.01677067
# sample estimates:
#   mean of x  mean of y 
# 0.06447639 0.09650924 
#
