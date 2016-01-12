library(broom) # used to neatly pass model results (model chaining/iteration)
library(plyr)
library(dummies)

sales <- read.csv("https://www.dropbox.com/s/yxgij2mtsou0lf0/mj-sales-transformed.csv?dl=1")
violations <- read.csv("https://www.dropbox.com/s/euwbe6mciu9oaw9/mj-violations-transformed.csv?dl=1")
applicants <- read.csv("https://www.dropbox.com/s/hw3ci1l8w55wwxw/all_applicants.csv?dl=1")
applicants$License_Number <- applicants$License.

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


# **** export data to work in Python/sklearn *****

# TODO use inference() and t-test to infer risk/sales growth from larger population of similar businesses? 
load(url("http://assets.datacamp.com/course/dasi/inference.Rdata"))
#inference()
#tt=t.test(applicants$)



