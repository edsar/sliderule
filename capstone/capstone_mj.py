#
# capstone_mj-Setup.py
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
