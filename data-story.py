import pandas as pd
import json
from ggplot import *

# title:   Telling stories about WA state marijuana business
# author:  Ed Sarausad         
# date:    11/8/2015
# desc:    Looking at a unique dataset acquired via public record request, explore the nature of marijuana license applicants    

# datafiles
# 1108
csv_1108_url = "https://www.dropbox.com/s/ouju327c34szoog/FlaggedCompanyUpdate1108.csv?dl=1"
# Combined with WA secretary of state and refresh of data from public record request
csv_comb_url = "https://www.dropbox.com/s/o6ezbptdmm31xoj/MarijunaApplicantsCombined.csv?dl=1"
# json_url = "https://www.dropbox.com/s/dr61wv22kop1znq/FlaggedCompanyUpdate1108.json?dl=1"

#
# Read it in
#
mj_biz_df = pd.read_csv(csv_comb_url)

#
# Explore
#
mj_biz_df.columns
# Index([u'Tradename', u'LicenseNo', u'UBI', u'StreetAddress', u'Suite', u'City',
#       u'State', u'County', u'ZipCode', u'MailAddress', u'MailSuite',
#       u'MailCity', u'MailState', u'MailZipCode', u'PrivDesc',
#       u'PrivilegeStatus', u'ReasonAction', u'StatusDate', u'DayPhone',
#       u'NightPhone', u'OwnerName', u'Email'],
#       dtype='object')

mj_biz_df.describe() #not too useful without meaningful numeric data yet!
#           LicenseNo           UBI       ZipCode   MailZipCode
# count    3848.000000  3.848000e+03  3.848000e+03  3.848000e+03
# mean   414197.219595  6.029087e+15  9.665543e+08  9.451521e+08
# std     14947.984118  1.158027e+14  1.372540e+08  1.933074e+08
# min     59974.000000  0.000000e+00  0.000000e+00  9.800100e+04
# 25%    412902.000000  6.033338e+15  9.824883e+08  9.811308e+08
# 50%    415688.000000  6.033520e+15  9.857728e+08  9.833891e+08
# 75%    416610.250000  6.033585e+15  9.885900e+08  9.868296e+08
# max    420130.000000  6.035314e+15  9.988000e+08  9.980100e+08

mj_biz_df.info()
# <class 'pandas.core.frame.DataFrame'>
# Int64Index: 3848 entries, 2343 to 2488
# Data columns (total 22 columns):
# Tradename          3848 non-null object
# LicenseNo          3848 non-null int64
# UBI                3848 non-null int64
# StreetAddress      3848 non-null object
# Suite              3848 non-null object
# City               3848 non-null object
# State              3848 non-null object
# County             3845 non-null object
# ZipCode            3848 non-null int64
# MailAddress        3848 non-null object
# MailSuite          3848 non-null object
# MailCity           3848 non-null object
# MailState          3848 non-null object
# MailZipCode        3848 non-null int64
# PrivDesc           3848 non-null object
# PrivilegeStatus    3848 non-null object
# ReasonAction       3848 non-null object
# StatusDate         3848 non-null object
# DayPhone           3848 non-null object
# NightPhone         3848 non-null object
# OwnerName          3844 non-null object
# Email              3807 non-null object
# dtypes: int64(4), object(18)
# memory usage: 691.4+ KB
#
# TODO Cleaning : remove dupes
#

#
# Find interesting businesses mentioned in the news - TODO: what would we do with this?
#
busted_names = ["Green City Collective".upper(), "Purple Haze".upper(), "Emerald Leaves".upper(), \
                "Mary Mart".upper(), "Dockside Cannabis".upper(), "Evergreen Cannabis".upper(), \
                "Cannablyss".upper(), "Cascade Kropz".upper(), "Clear Choice Cannabis".upper(), \
                "Royal's Cannabis".upper(), "Token Herb".upper(), "Sweet Greens Northwest".upper(), \
                "Green Lady". upper(), "TJ's Cannabis Buds, Edibles, Oils & More".upper(), \
                "4us Retail".upper(), "Bud Hut".upper(), "Theorem".upper(), "American Mary".upper()]

# 
# busted_names_df = pd.DataFrame.from_records(busted_names)
# busted_matches_df = mj_biz_df.select(lamba x:  

# Note: Source JSON is malformed 
# ValueError: arrays must all be same length
# df2 = pd.read_json(json_url)
# df == df2

#
#  Recent news indicates that cities are having to regulate the number of marijuana businesses in their city.
#  Where are businesses located?
#
# mj_biz_df.sort("County", ascending=False, inplace=True)
# mj_biz_df.groupby("County").count()
# mj_biz_df[["County", "Tradename"]]
# mj_biz_df.unstack("County")
#groupby("County").count().

# Some exploratory plots!
#
ggplot(aes(x="County"), data=mj_biz_df) + geom_bar() # too many x values!
ggplot(aes(x="City"), data=mj_biz_df) + geom_bar() # waaaay too many x values!

# mj_biz_df["ZipCode"].apply(str)
# ggplot(aes(x="ZipCode"), data=mj_biz_df) + geom_bar()

#
# Slice the data down to top10s
#

#
# Top 10 Counties
#
top10counties = pd.DataFrame(mj_biz_df[["County"]].stack().value_counts()[:10])
# KING         487
# SPOKANE      387
# SNOHOMISH    314
# THURSTON     250
# WHATCOM      206
# PIERCE       201
# OKANOGAN     174
# GRANT        139
# CLARK        127
# YAKIMA       117
ggplot(aes(x=), data=top10counties) + geom_bar()


#
# Top 10 Cities
#
top10cities = pd.DataFrame(mj_biz_df[["City"]].stack().value_counts()[:10])
# SEATTLE                     268
# SPOKANE                     138
# TACOMA                      138
# BELLINGHAM                  108
# OLYMPIA                      95
# ARLINGTON                    92
# VANCOUVER                    70
# SPOKANE VALLEY               70
# SHELTON                      62
# ELLENSBURG                   62


#
# Top 10 Zips
#
top10zips = pd.DataFrame(mj_biz_df[["ZipCode"]].stack().value_counts()[:10])
# 993440000    30
# 990040000    27
# 988550000    26
# 982260000    25
# 988480000    22
# 984090000    22
# 985840000    21
# 989260000    19
# 992120000    19
# 985772917    19

# Plot 'em!
# TODO: How can gglot handle these top10 datastructures
top10counties.plot(kind='bar')
top10cities.plot(kind='bar')
top10zips.plot(kind='bar')

#
#  Can the owner names tell us anything about their gender? Are business owners mostly male or female? 
#
#  Attribution: https://stephenholiday.com/articles/2011/gender-prediction-with-python/ (stephen.holiday@gmail.com)
mj_biz_df[["OwnerName"]].stack().value_counts()[:20]
#
# First we'll look at the most common business owner names looking for kingpins

# RODRIGUEZ,  JUAN                     8
# TOKELAND GROWING, LLC                6
# SPINNING HEADS, INC.                 6
# GENSYS ONE CORPORATION               6
# THE BUD CLUB, LLC                    6
# ALIS GROUP, LLC                      6
# NW BAKERY SERVICES, LLC              6
# BIDWELL,  ROBIN  LUELL               6
# MOMMA CHAN LLC                       6
# VERT CORPORATION                     6
# HYDRO EMPIRE LLC                     6
# CASCADE CROPS, LLC                   6
# HARMONY FARMS LLC                    6
# THE GREEN GREEN GRASS OF HOME LLC    6
# MNS - PNP, LLC                       6
# AGAPE RESEARCH WA, LLC               6
# CANNASOL FARMS INCORPORATED          6
# PATRIOT MEDS LLC                     6
# FRENCHMAN COULEE LLC                 6
# WOODPEG, INC                         6


#
#  Sometimes email domains can reveal insights about the business owner. What is the distribution of these email domains?
#
mj_biz_df["mail domain"] = mj_biz_df["Email"].str.split("@")
mj_biz_df["mail domain"]

#
#  The federal government publishes a list of High-Intensity Drug Trafficking Area (HIDTA). How many of these businesses
#  are located in HIDTA counties?
#
hidta_df = pd.read_csv("https://www.dropbox.com/s/7zhmi5h3ysgfjdx/HIDTA.csv?dl=1")
# hidta_df.lookup(hidta_df["State"=="Washington"], hidta_df["HIDTA Counties"])
# hidta_counties = hidta_df["State"=="Washington"]
hidta_df[hidta_df.State=="Washington"]
