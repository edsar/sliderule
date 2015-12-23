#
# Statistics Project 3 - Evaluate readmissions rates report 
#

# use some libraries etc
library(stats)
library(lsr)
load(url("http://assets.datacamp.com/course/dasi/inference.Rdata"))

setwd("~/sliderule/statistics_project3/statistics project 3")
hospital <- read.csv("clean_hospital_read_df.csv")

# TO TEST ASSERTION: Rate of readmissions in trendiing down with increasing number of discharges#
#
# TRY: Looking for inverse (negative correlation) between #discharges and #readmissions
# 
# RESULTS: 
#   1) with #readmissions as a prectior of #discharges, significance with so-so R-squared with positive correlation
#   2) with #discharges as a predictor, significance with so-so R-squared with smaller positive correction
#
summary(lm(hospital$Number.of.Discharges~hospital$Number.of.Readmissions))

# add scatterplot, graphs to explore data (outliers, missing values, big relationships)
plot(hospital$Number.of.Discharges, hospital$Number.of.Readmissions)


summary(lm(hospital$Number.of.Readmissions~hospital$Number.of.Discharges))

# In hospitals/facilities with number of discharges < 100, mean excess readmission rate is 1.023 and 63% have excess readmission rate greater than 1
# In hospitals/facilities with number of discharges > 1000, mean excess readmission rate is 0.978 and 44% have excess readmission rate greater than 1
small <- subset(hospital, hospital$Number.of.Discharges < 100)
plot(small$Number.of.Discharges, small$Number.of.Readmissions)
mean(small$Excess.Readmission.Ratio, na.rm = TRUE)
# 1.022618
nrow(subset(small,small$Excess.Readmission.Ratio > 1))/nrow(small)
# 0.5918046 (less than 63% asserted)

large <- subset(hospital, hospital$Number.of.Discharges > 1000)
plot(large$Number.of.Discharges, large$Number.of.Readmissions)

# add small/large flag variable, plot both with color

mean(large$Excess.Readmission.Ratio, na.rm = TRUE)
# 0.9783354
nrow(subset(large,large$Excess.Readmission.Ratio > 1))/nrow(large)
# 0.4449244

# ASSERTION:  There is a significant correlation between hospital capacity (number of discharges) and readmission rates.
# VALIDATION: Found ~.62 adjusted R^2
summary(lm(hospital$Number.of.Discharges~hospital$Number.of.Readmissions))

# Smaller hospitals/facilities may be lacking necessary resources to ensure quality care and prevent complications that lead to readmissions
# TODO find out what is separating lines
# TODO model dummy vars and interaction terms


# Setup an appropriate hypothesis test.
# H0 : there is no difference in excess readmission ratio between small and large hospitals
# HA : there is a significant difference in excess readmission ratio between small and large hospitals

# Compute and report the observed significance value (or p-value).
# Report statistical significance for α = .01.
# inference(small$Excess.Readmission.Ratio, large$Excess.Readmission.Ratio, type = "ht",
#           est = "mean", method = "theoretical", alternative = "greater", boot_method = "perc",
#           conflevel = 0.99, null = 0)

t.test(small$Excess.Readmission.Ratio, large$Excess.Readmission.Ratio, alternative = "two.sided", mu = 0)

# Discuss statistical significance and practical significance
# At large enough sample sizes, significance will be found with even small differences
# Is there practical meaning to the significant difference?

# Look at differences by $State
# TODO Look at F-stat and p-value to evaluate model fit  
summary(lm(hospital$Number.of.Discharges~hospital$State)) #low R
summary(lm(hospital$Number.of.Readmissions~hospital$State)) #low R


# TODO Look at $Measure.Name
summary(lm(hospital$Number.of.Discharges~hospital$Measure.Name)) #low R
summary(lm(hospital$Number.of.Readmissions~hospital$Measure.Name)) #low R

# TODO eta^2 for ANOVA


# TODO omega^2 for ANOVA


# TODO what about effect size?

