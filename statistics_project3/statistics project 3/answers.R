#
# Statistics Project 3 - Evaluate readmissions rates report 
#

# use some libraries etc
library(stats)
library(lsr)
library(data.table)
library(ggplot2)
library(dplyr)

# https://rstudio-pubs-static.s3.amazonaws.com/23230_b2e9b87251a2488da0fba51325e26040.html
load(url("http://assets.datacamp.com/course/dasi/inference.Rdata"))

setwd("~/apps/sliderule/statistics_project3/statistics project 3")
hospital <- read.csv("clean_hospital_read_df.csv")

# add scatterplot, graphs to explore data (outliers, missing values, big relationships)
plot(hospital$Number.of.Discharges, hospital$Number.of.Readmissions)

# try subsetting by hospital size (based on suggested feature, #discharges)
small <- subset(hospital, hospital$Number.of.Discharges < 100)
large <- subset(hospital, hospital$Number.of.Discharges > 1000)
med <- subset(hospital, hospital$Number.of.Discharges < 1000 & hospital$Number.of.Discharges > 100 )
xlarge <- subset(hospital, hospital$Number.of.Discharges > 2000)

# BASIC THEME
theme.chart <- 
  theme(legend.position = "none") +
  theme(plot.title = element_text(size=26, family="Trebuchet MS", face="bold", hjust=0, color="#666666")) +
  theme(axis.title = element_text(size=18, family="Trebuchet MS", face="bold", color="#666666")) +
  theme(axis.title.y = element_text(angle=0)) 

# SCATTERPLOT THEME
theme.chart_SCATTER <- theme.chart +
  theme(axis.title.x = element_text(hjust=0, vjust=-.5))

# HISTOGRAM THEME
theme.chart_HIST <- theme.chart +
  theme(axis.title.x = element_text(hjust=0, vjust=-.5))

# SMALL MULTIPLE THEME
theme.chart_SMALLM <- theme.chart +
  theme(panel.grid.minor = element_blank()) +
  theme(strip.text.x = element_text(size=16, family="Trebuchet MS", face="bold", color="#666666"))  

# plot small hospitals discharges to readmissions
ggplot(data=small, aes(x=Number.of.Discharges, y=Number.of.Readmissions)) +
  geom_point(alpha=.4, size=4, color="#9ecae1") +
  ggtitle("Discharges vs Readmissions (small hospitals)") +
  labs(x="Discharges", y="Readmissions") +
  theme.chart_SCATTER

# plot med hospitals discharges to readmissions
ggplot(data=med, aes(x=Number.of.Discharges, y=Number.of.Readmissions)) +
  geom_point(alpha=.4, size=4, color="#9ecae1") +
  ggtitle("Discharges vs Readmissions (med hospitals)") +
  labs(x="Discharges", y="Readmissions") +
  theme.chart_SCATTER

# plot large hospitals discharges to readmissions
ggplot(data=large, aes(x=Number.of.Discharges, y=Number.of.Readmissions)) +
  geom_point(alpha=.4, size=4, color="#9ecae1") +
  ggtitle("Discharges vs Readmissions (large hospitals)") +
  labs(x="Discharges", y="Readmissions") +
  theme.chart_SCATTER

# plot xlarge hospitals discharges to readmissions
ggplot(data=xlarge, aes(x=Number.of.Discharges, y=Number.of.Readmissions)) +
  geom_point(alpha=.4, size=4, color="#9ecae1") +
  ggtitle("Discharges vs Readmissions (xlarge hospitals)") +
  labs(x="Discharges", y="Readmissions") +
  theme.chart_SCATTER

# look at expected vs predicated readmission across all hospitals
ggplot(data=hospital, aes(x=Expected.Readmission.Rate, y=Predicted.Readmission.Rate)) +
  geom_point(alpha=.4, size=4, color="#9ecae1") +
  ggtitle("Expected Readmissions vs Predicted Readmissions") +
  labs(x="Expected Readmissions", y="Predicted Readmissions") +
  theme.chart_SCATTER

# distribution of readmissions
ggplot(data=hospital, aes(x=Number.of.Discharges)) +
  geom_histogram(fill="#9ecae1") +  
  ggtitle("Histogram of Readmissions") +
  labs(x="Readmissions", y="Count\nof Records") +
  theme.chart_HIST

# distribution of discharges
ggplot(data=hospital, aes(x=Number.of.Discharges)) +
  geom_histogram(fill="#9ecae1") +  
  ggtitle("Histogram of Discharges") +
  labs(x="Discharges", y="Count\nof Records") +
  theme.chart_HIST

# distribution of smaller discharges (0..75)
hospital %>%
  filter(Number.of.Discharges >0 & Number.of.Discharges <75) %>%
  ggplot(aes(x= as.factor(Number.of.Discharges))) +
  geom_bar(fill="#9ecae1") +
  labs(x="Discharges") +
  theme.chart

# readmissions by state
ggplot(data=hospital, aes(x=Number.of.Readmissions)) +
  geom_histogram(fill="#9ecae1") +
  ggtitle("Histogram of Readmissions\nby State") +
  labs(x="Readmissions", y="Count\nof Records") +
  facet_wrap(~State) +
  theme.chart_SMALLM

# readmissions by procedures
ggplot(data=hospital, aes(x=Number.of.Readmissions)) +
  geom_histogram(fill="#9ecae1") +
  ggtitle("Histogram of Readmissions\nby Procedure") +
  labs(x="Readmissions", y="Count\nof Records") +
  facet_wrap(~Measure.Name) +
  theme.chart_SMALLM


# TO TEST ASSERTION: Rate of readmissions in trending down with increasing number of discharges#
#
# TRY: Looking for inverse (negative correlation) between #discharges and #readmissions
# 
# RESULTS: 
#   1) with #readmissions as a prectior of #discharges, significance with so-so R-squared with positive correlation
#   2) with #discharges as a predictor, significance with so-so R-squared with smaller positive correction
#



summary(lm(hospital$Number.of.Discharges~hospital$Number.of.Readmissions))
summary(lm(hospital$Number.of.Readmissions~hospital$Number.of.Discharges))

# In hospitals/facilities with number of discharges < 100, mean excess readmission rate is 1.023 and 63% have excess readmission rate greater than 1
# In hospitals/facilities with number of discharges > 1000, mean excess readmission rate is 0.978 and 44% have excess readmission rate greater than 1

# fit1 = lm(hospital$Number.of.Discharges~hospital$Number.of.Readmissions)
# summary(fit1)
# res.fit1 = resid(fit1)
# plot(hospital$Number.of.Readmissions, res.fit1, 
#      ylab="Residuals", xlab="Number of Readmissions", main="Number of Discharges") 
# abline(0, 0)                  

# TO TEST ASSERTION: In hospitals/facilities with number of discharges < 100, mean excess readmission rate is 1.023 and 63% have excess readmission rate greater than 1
# TO TEST ASSERTION: In hospitals/facilities with number of discharges > 1000, mean excess readmission rate is 0.978 and 44% have excess readmission rate greater than 1
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
aov.1 = aov(Number.of.Discharges~Number.of.Readmissions, data=data.table(hospital))
summary(aov.1)
print(model.tables(aov.1,"means"), digits=3)
boxplot(Number.of.Discharges~Number.of.Readmissions, data=hospital)
# TODO why does this look so strange?

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

# Look at differences procedure called $Measure.Name
summary(lm(hospital$Number.of.Discharges~hospital$Measure.Name)) #low R
summary(lm(hospital$Number.of.Readmissions~hospital$Measure.Name)) #low R

# Look at AOV 
aov <- aov(Excess.Readmission.Ratio~Number.of.Discharges*Number.of.Readmissions*State*Measure.Name, data=hospital)
aov

# TODO: Can I use Tukey HSD to tell which groups differ?
# tuk <- TukeyHSD(aov)
# tuk
# Warning messages:
#   1: In replications(paste("~", xx), data = mf) :
#   non-factors ignored: Number.of.Discharges
# 2: In replications(paste("~", xx), data = mf) :
#   non-factors ignored: Number.of.Readmissions
# 3: In replications(paste("~", xx), data = mf) :
#   non-factors ignored: Number.of.Discharges, Number.of.Readmissions
# 4: In replications(paste("~", xx), data = mf) :
#   non-factors ignored: Number.of.Discharges, State
# 5: In replications(paste("~", xx), data = mf) :
#   non-factors ignored: Number.of.Readmissions, State
# 6: In replications(paste("~", xx), data = mf) :
#   non-factors ignored: Number.of.Discharges, Measure.Name
# 7: In replications(paste("~", xx), data = mf) :
#   non-factors ignored: Number.of.Readmissions, Measure.Name
# 8: In replications(paste("~", xx), data = mf) :
#   non-factors ignored: Number.of.Discharges, Number.of.Readmissions, State
# 9: In replications(paste("~", xx), data = mf) :
#   non-factors ignored: Number.of.Discharges, Number.of.Readmissions, Measure.Name
# 10: In replications(paste("~", xx), data = mf) :
#   non-factors ignored: Number.of.Discharges, State, Measure.Name
# 11: In replications(paste("~", xx), data = mf) :
#   non-factors ignored: Number.of.Readmissions, State, Measure.Name
# 12: In replications(paste("~", xx), data = mf) :
#   non-factors ignored: Number.of.Discharges, Number.of.Readmissions, State, Measure.Name
