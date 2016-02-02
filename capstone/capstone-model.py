import pandas as pd
import datetime
import matplotlib.pyplot as plt
import pylab as pl


# Title:     Derisking Marijuana Modeling
# Author:    Ed Sarausad
# Overview: 
#
# This summary script loads clean data and sets up the modeling for the analysis.
# The goal of the analysis is to build a model to predict risk as defined by the likelihood to commit a business violation.
# This risk assessment comprises an important part of the bank's decision to extend credit or even bank a business period.
#

# First we load prepared data. 
# TODO How was the data prepared?
# The unit of analysis is the business applicant identified by a license number.
#

applicants = pd.read_csv("https://www.dropbox.com/s/d1jwebq4nt5eg87/applicants_aged.csv?dl=1")

# We then control for time by taking a window of data we will set aside as the test set to represent "the future"
# In a perfect world, this "future window of time" would be 1-2 years but we only have a 2-year period of data, since the 
# market for legalized marijuana has just been started in the past year with applicants applying right before then.
# So our window will be a short 3-month timeframe

timeframe = 90 # 90 days = 3 months




