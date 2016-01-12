library(broom) # used to neatly pass model results (model chaining/iteration)
library(forecast) #consider using plot.ly for interactive forecast

sales <- read.csv("https://www.dropbox.com/s/yxgij2mtsou0lf0/mj-sales-transformed.csv?dl=1")
violations <- read.csv("https://www.dropbox.com/s/euwbe6mciu9oaw9/mj-violations-transformed.csv?dl=1")
applicants <- read.csv("https://www.dropbox.com/s/hw3ci1l8w55wwxw/all_applicants.csv?dl=1")
applicants$License_Number <- applicants$License.

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

# inference and t-test?
load(url("http://assets.datacamp.com/course/dasi/inference.Rdata"))
tt=t.test()

