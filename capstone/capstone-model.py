import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pylab as pl
from sklearn.cross_validation import train_test_split

# Title:     Derisking Marijuana Business - model
# Author:    Ed Sarausad
# Overview: 
#
# This summary script loads clean data and sets up the modeling for the analysis.
# The goal of the analysis is to build a model to predict risk as defined by the likelihood to commit a business violation.
# This risk assessment comprises an important part of the bank's decision to extend credit or even bank a business period.
#

# First we load prepared data, for applicants 
applicants = pd.read_csv("https://www.dropbox.com/s/vm6qvkqjl8qvxoc/applicants_aged_small.csv?dl=1", index_col=False)
applicants.reset_index(drop=True)
applicants.set_index('License_Number')

# For applicants (businesses), add an outcome variable, violator.
applicants["violator"] = applicants["violation_count"] > 0

# Next we load prepared data, for violations 
violations = pd.read_csv("https://www.dropbox.com/s/euwbe6mciu9oaw9/mj-violations-transformed.csv?dl=1", index_col=False)
violations.reset_index(drop=True)
violations.set_index('License_Number')
violations = violations.drop_duplicates(['License_Number','Visit_Date','Penalty_Type', 'Case_No','WAC_Code','Violation_Type'])


# We add details from the applicants to the violation records
violations_details = pd.merge(violations, applicants, left_on='License_Number', right_on='License_Number', how='inner', copy=False)

# Remove any duplicates
violations_details = violations_details.drop_duplicates(['License_Number','Visit_Date','Penalty_Type', 'Case_No','WAC_Code','Violation_Type'])

#violations_details.to_csv("violations_details.csv")
#violations_details = pd.read_csv("violations_details.csv")

# We then control for time by taking a window of data we will set aside as the test set to represent "the future"
# In a perfect world, this "future window of time" would be 1-2 years but we only have a 2-year period of data, since the 
# market for legalized marijuana has just been started in the past year with applicants applying right before then.
# So given our limited dataset, our window will be a short 3-month timeframe

# Here we transform the visit date column to a datetime data type
def convertDate ( dateObj ):
    date = datetime.datetime.strptime(str(dateObj),"%x")
    return date
violations_details["Visited_Date"] = violations_details["Visit_Date"].apply(convertDate)

# Sort the violations in descending order by date (visit date, we don't know the date of actual violation)
violations_details = violations_details.sort(["Visited_Date"], ascending=False)

# Then take the "future" timeframe and set aside that part as the test set
# future_window = 90 # 90 days = 3 months

future_window = 3 # 90 days = 3 months
window_begin = violations_details.head(1)["Visited_Date"] - datetime.timedelta(days = future_window * 30)
# window_range = pd.date_range(window_begin.iloc[0].date(), periods=future_window, freq='D')
window_range = pd.date_range(window_begin.iloc[0].date(), periods=future_window, freq='M')


###
# window_end = violations_details.head(1)["Visited_Date"]
# window_range = pd.date_range(window_begin, window_end) # ERR: Cannot convert input to Timestamp

# # Filter out the future window data and save to test_violations
# violations_details.set_index("Visited_Date")
# test_violations = violations_details.ix[window_begin:window_end]
# test_violations = violations_details[(violations_details["Visited_Date"] >= window_begin) & (violations_details["Visited_Date"] <= window_end)] # ERR: Series lengths must match to compare
# test_violations = violations_details.query(window_end <= violations_details["Visited_Date"] <= window_begin) # ERR: Series lengths must match to compare

# # TODO handle borderline dates
# def is_in_window (date, startdate, enddate):
#     return date > startdate & date < enddate

window_begin.iloc[0].date() in window_range

train_violations = violations_details["Visited_Date"].apply(
test_violations = violations_details[is_in_future_window]


features = applicants[[""Total Sales", "Excise Tax Due", "Tax Rate", "Type:Medical", "Type:Processor", "Type:Producer", "Type:Retailer"]] 
labels = applicants["violator"]
features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, labels, test_size=0.3) 



