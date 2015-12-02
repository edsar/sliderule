import pandas as pd
import scipy as sc
from scipy import stats
from math import sqrt
import numpy as nm


df = pd.read_csv("~\Documents\sliderule\statistics_project1\statistics project 1\data\human_body_temperature.csv")

# Is the distribution of body temperatures normal?

sc.stats.mstats.normaltest(df["temperature"])
# NormaltestResult(statistic=2.7038014333192031, pvalue=0.2587479863488254)
# ANSWER: Above tests null that distribution is normal, so YES it's normal
# http://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.stats.mstats.normaltest.html


# Is the true population mean really 98.6 degrees F?
# Bring out the one sample hypothesis test! In this situation, is it approriate to apply a z-test or a t-test? How will the result be different?
stats.ttest_1samp(df["temperature"], 98.6)
# n > 30, samples are independent
# Ttest_1sampResult(statistic=-5.4548232923645195, pvalue=2.4106320415561276e-07)
# ANSWER: No, reject null 

# At what temperature should we consider someone's temperature to be "abnormal"?
# Start by computing the margin of error and confidence interval.

# SE = Mu / sqrt (n)
# 0.046784246832957226
# SE = nm.var(df["temperature"])/sqrt(df["temperature"].count())
# 0.046784246832957226

SE = stats.sem(df["temperature"])
SE
# 0.064304416837891024

# lower bound 95% CI
nm.mean(df["temperature"]) - 2 * SE
# 98.120621935554993

# upper bound 95% CI
nm.mean(df["temperature"]) + 2 * SE
# 98.377839602906562


# Is there a significant difference between males and females in normal temperature?
# Set up and solve for a two sample hypothesis testing.
male = df[df["gender"]=="M"]
female = df[df["gender"]=="F"]

# H0 = No significant difference between males and females in normal temp
# HA = There is significant difference

stats.ttest_ind(male["temperature"], female["temperature"])
# Ttest_indResult(statistic=-2.2854345381656103, pvalue=0.023931883122395609)




