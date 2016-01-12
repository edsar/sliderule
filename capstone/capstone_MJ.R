library(broom) # used to neatly pass model results (model chaining/iteration)
<<<<<<< HEAD
library(forecast) #consider using plot.ly for interactive forecast
=======
library(plyr)
library(dummies)
>>>>>>> origin/master

sales <- read.csv("https://www.dropbox.com/s/yxgij2mtsou0lf0/mj-sales-transformed.csv?dl=1")
violations <- read.csv("https://www.dropbox.com/s/euwbe6mciu9oaw9/mj-violations-transformed.csv?dl=1")
applicants <- read.csv("https://www.dropbox.com/s/hw3ci1l8w55wwxw/all_applicants.csv?dl=1")
applicants$License_Number <- applicants$License.

<<<<<<< HEAD
# why does this not come to a flat 25% rate for all? because as.numeric converts the value incorrectly?!
sales$Total_Sales <- as.numeric(gsub("\\$","", gsub("\\,","", sales$Total_Sales))) 
sales$Excise_Tax_Due <- as.numeric(gsub("\\$","", gsub("\\,","", sales$Excise_Tax_Due))) 
sales$tax_rate <- sales$Excise_Tax_Due / sales$Total_Sales

# use applicants and sum sales and violations
# to get: license_number | total_sales | total_violations
# TODO: Do I need to scale features?

# get some aggregates first
salesonly <- sales[,c(2,4)]
aggsales <- aggregate(salesonly, by=list(sales$License_Number), FUN=sum)

# TODO no count??
# aggviolations <- aggregate(violations, by=list(violations$License_Number), FUN=count)

# then merge on license_number
applicants_with_sales <- merge(applicants, aggsales, by="License_Number")
=======
# format currency fields
sales$Total_Sales <- as.numeric(gsub("\\$","",(gsub("\\,","",sales$Total_Sales))))
sales$Excise_Tax_Due <- as.numeric(gsub("\\$","",(gsub("\\,","",sales$Excise_Tax_Due))))
sales$tax_rate <- as.numeric(sales$Excise_Tax_Due) / as.numeric(sales$Total_Sales)

# use applicants and aggregate sales and violations
sales_only <- sales[,c(2,4)]
aggsales <- aggregate(sales_only, by=list(sales_only$License_Number), FUN="sum")
aggviolations <- count(violations, c('License_Number'))
names(aggviolations)[names(aggviolations)=='freq'] <- "violation_count"
applicants <- merge(applicants, aggsales, by='License_Number') #inner join -> TODO left join
applicants <- merge(applicants, aggviolations, by='License_Number') #inner join -> TODO left join
str(applicants) # Total_Sales and violation_count should be added

# is there a correlation between sales and violations? overall? in certain segments?
summary(lm(applicants$violation_count ~ applicants$Total_Sales))


# TODO add dummy variables for Suspended and Cancelled


# TODO add dummary variables for each business Type: Producer, Processor, Retailer, Medical
>>>>>>> origin/master


# **** export data to work in Python/sklearn *****

# TODO use inference() and t-test to infer risk/sales growth from larger population of similar businesses? 
load(url("http://assets.datacamp.com/course/dasi/inference.Rdata"))
#inference()
#tt=t.test(applicants$)



