
#
# Datasets: 
#   Washington marijuana applicants from 11/03/2015 ~1800 records
#   Washington marijuana business violations 11/2015 ~500 records
#   Washington marijuana business sales and tax revenue 11/2015 ~7000 records
#
# Labels:
#   Licensed applicants who have been suspended (penalty type=suspension)
#

import pandas as pd
from sklearn import tree
from sklearn.naive_bayes import GaussianNB 
from __future__ import division

# load data
sales = pd.read_csv("https://www.dropbox.com/s/yxgij2mtsou0lf0/mj-sales-transformed.csv?dl=1")
violations = pd.read_csv("https://www.dropbox.com/s/euwbe6mciu9oaw9/mj-violations-transformed.csv?dl=1")

# combine data
applicants_file = "https://www.dropbox.com/s/6guyvoo6a28d6vx/MarijuanaApplicants11032015.xls?dl=1"
producers = pd.read_excel(applicants_file, sheetname="Producers 11-04-15")
producers["type"] = "producer"

processors = pd.read_excel(applicants_file, sheetname="Processors 11-04-15")
processors["type"] = "processor"

retailers = pd.read_excel(applicants_file, sheetname="Retailers 11-04-15")
retailers["type"] = "retailer"

medicals = pd.read_excel(applicants_file, sheetname="Medical Endorsements 11-04-15")
medicals["type"] = "medical"

all_dfs = [producers, processors, retailers, medicals]
all_applicants = pd.concat(all_dfs)

# use applicants file and sum sales and violations in new columns
from re import sub
from decimal import Decimal
sales['Total_Sales_Num'] = Decimal(sub(r'[^\d.]', '', sales['Total_Sales'])) 
by_license = sales.groupby("License_Number")
by_license = violations.groupby("License_Number").count()

# transform data
# question: Are there anomalies that we should clean up? (outlier detection) - with plots, not extensive since low # fields
# question: Do you take out and how many do you take out? - sliding scale based on predictive quality of model (extremes of bell curve RMSE)


# explore data -- picking up where Tableau left off
# question: What % of companies have violations?, have businesses enter evenly? 
violaters = pd.DataFrame(violations.groupby(['License_Number']).count())
print "There are ",len(violations.index), " total violations."
print "There are ", len(violaters.index), " unique violaters."
print "There are ", len(all_applicants.index), " applicants."
print len(violaters.index)/len(all_applicants.index) *100 , " % violators out of total applicant pool."
# answer: <4%


<<<<<<< HEAD
# partition training/test 50/50, consider 60/20/20?
# work on training only (including CV, don't touch test)
from sklearn import cross_validation
features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(


=======
>>>>>>> origin/master
# question: Can businesses be plotted into an interesting 2x2? (scatterplot, unsup clustering/classification, PCA?)
# question: How do violations impact sales? (survival analysis) *interpretive, yield odds of dying from illness, dropout rates* (LOW-PRI)
# question: Are there features that predict violations? (regression/classification) *more iterations of predictive model*


# explore data
# question: Does the learning model exhibit bias or variance?
# question: Are there outliers/anomalies that we shouldn't ignore?


# modeling risk (for de-marketing)
# question:  Which businesses are likely to be charged with severe violations? (prediction) *more iterations of predictive model*


# modeling opportunity (for increased banking relationship)
# question:  Which businesses have positively forecasted sales? (R probably better-- forecast package)
# question:  What will be total revenue quarter by quarter or region
