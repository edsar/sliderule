library(stats)
library(utils)
library(nortest)

setwd("~/sliderule/statistics_project1/statistics project 1")

df <- read.csv("data/human_body_temperature.csv")

qqnorm(df$temperature)

# run tests of null that distribution is normal
ad.test(df$temperature)
# A = 0.5201, p-value = 0.1829

cvm.test(df$temperature)
# W = 0.081952, p-value = 0.1937

lillie.test(df$temperature)
# D = 0.064727, p-value = 0.2009

pearson.test(df$temperature)
# P = 30.154, p-value = 0.002647
# reject null?

sf.test(df$temperature)
# W = 0.98379, p-value = 0.1113
