#
# Statistics Project 1
#
# Ed Sarausad
# 12/6/2015
#
# TODO: Consider use of FWER, FDR, and associated solutions
#
library(stats)
library(utils)
library(nortest)

# User inference function provide by DataCamp
load(url("http://assets.datacamp.com/course/dasi/inference.Rdata"))
setwd("~/sliderule/statistics_project1/statistics project 1")

df <- read.csv("data/human_body_temperature.csv")

qqnorm(df$temperature)
qqline(df$temperature)

# 1.Is the distribution of body temperatures normal? .Remember that this is a condition for the CLT, and hence the statistical tests we are using, to apply. 
#
# First, we'll run tests of null that distribution is normal using normality package, nortest
# NOTE: Doing multiple tests and checking for FWER, FDR etc does not apply since it's the same data and same question (normality)
#
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

# 2.Is the true population mean really 98.6 degrees
# Bring out the one sample hypothesis test! In this situation, is it approriate to apply a z-test or a t-test? How will the result be different?
inference(df$temperature, est = "mean", method = "theoretical", type = "ci", conflevel = 0.95, boot_method = "perc")
# At 95% CI, 98.6 does not fall within the CI

# 3.At what temperature should we consider someone's temperature to be "abnormal"?.Start by computing the margin of error and confidence interval.
# According to this sample, an abnormal temperature at 99% CI would be less than 98.0836 or greater than 98.4149
inference(df$temperature, est = "mean", method = "theoretical", type = "ci", conflevel = 0.99, boot_method = "perc")

# 4.Is there a significant difference between males and females in normal temperature?.Set up and solve for a two sample hypothesis testing.
# H0 : There is no difference between male and female normal temperatures
# HA : There is significant different between male and female normal temperatures
male <- subset(df, df$gender=="M")
female <- subset(df, df$gender=="F")
#inference(male, female, est = "proportion", method = "theoretical", type = "ht", conflevel = 0.95, boot_method="perc", alternative = "twosided")
# Pooled T-test
t.test(female$temperature, male$temperature, mu=0, var.equal = TRUE)
t.test(female$temperature, male$temperature, mu=0)

# Using a two-sided test
t.test(male$temperature, female$temperature, mu=0, var.equal = TRUE)
t.test(male$temperature, female$temperature, mu=0)

