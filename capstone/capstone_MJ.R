
library(broom) # used to neatly pass model results (model chaining/iteration)
library(forecast) #consider using plot.ly for interactive forecast
library(plyr)
library(dummies)
library(nortest)
library(glmnet) # http://web.stanford.edu/~hastie/glmnet/glmnet_alpha.html
library(caret)
library(Amelia) # missing value viz
library(stats)
library(lmtest)
library(pROC)

#
#
# 1.DATASET/QUESTIONS -> 2.FEATURES -> 3.ALGORITHM -> 4.EVALUATION (rinse/repeat) 
#
#

sales <- read.csv("https://www.dropbox.com/s/yxgij2mtsou0lf0/mj-sales-transformed.csv?dl=1")
violations <- read.csv("https://www.dropbox.com/s/euwbe6mciu9oaw9/mj-violations-transformed.csv?dl=1")
applicants <- read.csv("https://www.dropbox.com/s/hw3ci1l8w55wwxw/all_applicants.csv?dl=1")

# for merging, match join column name
applicants$License_Number <- applicants$License.

# what's missing?
missmap(applicants, main = "Applicants: Missing values vs observed")
missmap(sales, main = "Sales: Missing values vs observed")
missmap(violations, main = "Violations: Missing values vs observed")

# format currency fields
# TODO some cells have () (negative) and -
sales$Total_Sales <- as.numeric(gsub("\\$","", gsub("\\,","", sales$Total_Sales))) 
# TODO some cells have () (negative) and -
sales$Excise_Tax_Due <- as.numeric(gsub("\\$","", gsub("\\,","", sales$Excise_Tax_Due))) 
# calculate a tax rate (not always 25%)
sales$tax_rate <- sales$Excise_Tax_Due / sales$Total_Sales

# use applicants and sum sales and violations
# to get: license_number | total_sales | total_violations
# TODO: Do I need to scale features?

# TODO no count??
# aggviolations <- aggregate(violations, by=list(violations$License_Number), FUN=count)

# then merge on license_number
# applicants_with_sales <- merge(applicants, aggsales, by="License_Number")

# use applicants and aggregate sales
sales_only <- sales[,c(2,4,5,8)]
aggsales <- aggregate(sales_only, by=list(sales_only$License_Number), FUN=sum)
# BUG BUG aggsales$License_Number not correct!
# why does the following line put join column in Group.1?
# aggsales[aggsales$Group.1==413287,]
# HACK *replacing* value in License_Number with Group.1
aggsales$License_Number <- aggsales$Group.1

# use applicants and aggregate sales and violations
aggviolations <- count(violations, c('License_Number'))
# NOTE: some businesses use same license to operate different business types (processor, retailer) with diff't tax treatment
# rename count frequency to something meaningful
names(aggviolations)[names(aggviolations)=='freq'] <- "violation_count"

# do a left join to merge aggregate sales and violations to license number
applicants <- merge(applicants, aggsales, by='License_Number', all.x=TRUE) #left join
applicants <- merge(applicants, aggviolations, by='License_Number', all.x=TRUE) #left join

# check the merge!
str(applicants) # Total_Sales and violation_count should be added

# state missing values assumptions:
#  sales - business has not made money or is not reporting, so setting NAs in Total_Sales, Excise_Tax_Due and tax_rate to 0
#  violations - innocence assumed, so setting to 0
applicants$Total_Sales[is.na(applicants$Total_Sales)] <- 0
applicants$Excise_Tax_Due[is.na(applicants$Excise_Tax_Due)] <- 0
applicants$tax_rate[is.na(applicants$tax_rate)] <- 0
applicants$violation_count[is.na(applicants$violation_count)] <- 0

# look at the distribution to test for normality
# plot(density(applicants$Total_Sales)) # Error in plot.new() : figure margins too large
ad.test(applicants$Total_Sales)
cvm.test(applicants$Total_Sales)
lillie.test(applicants$Total_Sales)
pearson.test(applicants$Total_Sales)
# sf.test(applicants$Total_Sales) # sample size must be between 5 and 5000
# low p-values, so NOT normally distributed!
# tested with: ad.test(rnorm(100, mean = 5, sd = 3));runif(100, min = 2, max = 4)

# NOT TODO: try to stratify into normal distributions or (assuming non-normal distribution)
# try equivalent tools for non-normal distributions: http://www.isixsigma.com/tools-templates/normality/dealing-non-normal-data-strategies-and-tools/

kruskal.test(list(applicants$violation_count, applicants$Total_Sales))
kruskal.test(list(applicants$Total_Sales, applicants$violation_count)) #same!

# look at the violation_count distribution to test for normality
plot(density(applicants$violation_count))
plot(density(applicants$Total_Sales))

# shapiro.test(applicants$violation_count) # limited to 5000!?
qqnorm(applicants$violation_count)
qqline(applicants$violation_count, col = 2)
ad.test(applicants$violation_count)
cvm.test(applicants$violation_count)
lillie.test(applicants$violation_count)
pearson.test(applicants$violation_count)
# sf.test(applicants$violation_count) # limited to 5000!?

# look for anomalies in the data
summary(applicants$ReasonAction) # most applications PENDING, not APPROVED
summary(applicants$State.1) # 13 out of WA state businesses
summary(applicants$type) # PROCESSOR and RETAILER most prevalent

# TODO add dummy variables for Suspended/Cancelled/Destruction, since not all violations are severe
#  - join applicants with violations and set dummy variable when violations$Penalty_Type %in% 
#     c('Suspension', 'Cancellation of License', 'Destruction of harvestable plants')

# add dummy variables for each business Type: Producer, Processor, Retailer, Medical
# type.dummies <- dummy('type', applicants, sep=":")
applicants <- dummy.data.frame(names='type', applicants, sep=":")

# TODO add variables for high-risk counties or cities
applicants$violator <- applicants$violation_count > 0
applicants$log_Total_Sales <- log(applicants$Total_Sales)
applicants$log_Excise_Tax_Due <- log(applicants$Excise_Tax_Due)

# is there a correlation between sales and violations? overall? in certain segments?
# overall
summary(lm(applicants$violation_count ~ applicants$Total_Sales)) # low R
summary(glm(applicants$violation_count ~ applicants$Total_Sales)) # ???

# logit regression for predicting a violator
train <- applicants[1:4130,]
test <- applicants[4131:5903,]
model <- glm(violator ~ Total_Sales + Excise_Tax_Due + PrivDesc,family=binomial(link='logit'),data=train)
summary(model) # significant: sales, tax, retailer type
# model evaluation
varImp(model)
pred = predict(model, newdata=test)
accuracy <- table(pred, test[,"violator"])
sum(diag(accuracy))/sum(accuracy)
## [1] 0.02
pred = predict(model, newdata=test)
confusionMatrix(data=pred, test$violator)

model <- glm(violator ~ Total_Sales + Excise_Tax_Due + ReasonAction,family=binomial(link='logit'),data=train)
summary(model) # significant: pending, withdrawn

model <- glm(violator ~ Total_Sales + Excise_Tax_Due + PrivilegeStatus,family=binomial(link='logit'),data=train)
summary(model) # slightly significant: issued

model <- glm(violator ~ Total_Sales + Excise_Tax_Due + tax_rate,family=binomial(link='logit'),data=train)
summary(model) # 

# **** export data to work in Python/sklearn *****
write.csv(applicants, "applicants_transformed.csv")
write.csv(aggsales, "sales_by_license.csv")
write.csv(aggviolations, "violations_by_license.csv")

# use inference() and t-test to infer risk/sales growth from larger population of similar businesses? 
# load(url("http://assets.datacamp.com/course/dasi/inference.Rdata"))
#inference()
#tt=t.test()

# **** read data back in as aged (handling time) *****
applicants_lt6 <- read.csv("https://www.dropbox.com/s/35us6fp8nfcl4pr/aged_lt_6mo.csv?dl=1")
applicants_612 <- read.csv("https://www.dropbox.com/s/ul4qdmqrcgn03fe/aged_6-12mo.csv?dl=1")
applicants_1224 <- read.csv("https://www.dropbox.com/s/li5bes2f7yrc9a1/aged_12-24mo.csv?dl=1")
applicants_gt24 <- read.csv("https://www.dropbox.com/s/nw6x2j40l3hsep5/aged_gt_24mo.csv?dl=1")

df <- applicants_lt6
# train with 70% of data
split <- round(nrow(df) * .7)
train <- df[1:split,]
test <- df[split:nrow(df),]
df$Total.Sales <- as.numeric(gsub("\\$","", gsub("\\,","", df$Total.Sales))) 
df$Excise.Tax.Due <- as.numeric(gsub("\\$","", gsub("\\,","", df$Excise.Tax.Due)))
df$Violator <- df$Violation_Count > 0
model <- glm(Violator ~ Total.Sales + Excise.Tax.Due + Priv.Desc,family=binomial(link='logit'),data=train)
summary(model) # significant: sales, tax, retailer type

# # using caret to get stratified random data in training/test sets
# set.seed(42)
# # need to convert logical to factor to remove RMSE error
# applicants_lt6$Violator <- as.factor(applicants_lt6$Violator)
# applicants_lt6$Total.Sales <- as.numeric(levels(applicants_lt6$Total.Sales))
# inTraining <- createDataPartition(applicants_lt6$Violator, p = 0.7, list=FALSE)
# training <- applicants_lt6[ inTraining, ]
# testing <- applicants_lt6[ -inTraining, ]

# tuning

# fitControl <- trainControl(## 10-fold CV
#   method = "repeatedcv",
#   number = 10,
#   ## repeated ten times
#   repeats = 10)

# fit model
logitFit <- train(Violator ~ Total.Sales + Excise.Tax.Due 
                  + Priv.Desc + Reason.Action + Privilege.Status + Tax.Rate, 
                 data = training,
                 method = "glm",
                 family = "binomial")

# since estimates characterize predictor/response on log-odds scale, we use exp to calculate odds ratio for each predictor
exp(coef(logitFit$finalModel))

predict(logitFit, newdata=testing, type="prob")

