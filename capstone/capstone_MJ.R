library(broom) # used to neatly pass model results (model chaining/iteration)


sales <- read.csv("https://www.dropbox.com/s/yxgij2mtsou0lf0/mj-sales-transformed.csv?dl=1")
violations <- read.csv("https://www.dropbox.com/s/euwbe6mciu9oaw9/mj-violations-transformed.csv?dl=1")
applicants <- read.csv("https://www.dropbox.com/s/hw3ci1l8w55wwxw/all_applicants.csv?dl=1")

# why does this not come to a flat 25% rate for all?
sales$tax_rate <- as.numeric(sales$Excise_Tax_Due) / as.numeric(sales$Total_Sales)

# use applicants and sum sales and violations


# inference and t-test?
load(url("http://assets.datacamp.com/course/dasi/inference.Rdata"))
tt=t.test()

# regression, clustering
