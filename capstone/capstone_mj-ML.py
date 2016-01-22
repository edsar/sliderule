#
# capstone_mj-ML.py
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
import sys
import numpy as np
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import cross_validation
from sklearn.metrics import accuracy_score
from sklearn.learning_curve import learning_curve
from sklearn.svm import SVC
from sklearn import linear_model
from __future__ import division
sys.path.append("C:\Users\edsar\Documents\sliderule\capstone")
from featureformat import featureFormat, targetFeatureSplit, createDataDict

# ****** read in transformed applicants *****
applicants = pd.read_csv("https://www.dropbox.com/s/s168am9a1iknwi8/applicants_transformed.csv?dl=1")

# partition training/test 50/50, consider 60/20/20?
# work on training only (including CV, don't touch test)

# features_list = ["violator", "violation_count", "Total_Sales"] #other features?
# data_dict = createDataDict(applicants, "License_Number")
# print data_dict
# data = featureFormat(data_dict, features_list)
# labels, features = targetFeatureSplit(data)

# use violator as label, so drop from df
# features = applicants.drop("violator", axis=1)
features = applicants[["violator", "violation_count", "Excise_Tax_Due", "tax_rate", "type:medical", "type:processor", "type:producer", "type:retailer"]] # some logarithms are infinity due to negative original value?
# features = applicants[["violation_count", "Total_Sales", "Excise_Tax_Due", "tax_rate", "type:medical", "type:processor", "type:producer", "type:retailer"]] # some logarithms are infinity due to negative original value?
# features = applicants[["violation_count", "Total_Sales", "Excise_Tax_Due", "tax_rate", "type:medical", "type:processor", "type:producer", "type:retailer", "log_Total_Sales", "log_Excise_Tax_Due"]] # NaN?
# labels = applicants["violator"] # boolean
labels = applicants["Total_Sales"]

# to make labels ints, do this
#labels = map(lambda x: 1 if x else 0, labels)
#labels = applicants["violator"]


features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, labels, test_size=0.3, random_state=42) 

# question: Can businesses be plotted into an interesting 2x2? (scatterplot, unsup clustering/classification, PCA?)
# question: How do violations impact sales? (survival analysis) *interpretive, yield odds of dying from illness, dropout rates* (LOW-PRI)
# question: Are there features that predict violations? (regression/classification) *more iterations of predictive model*

clf = tree.DecisionTreeClassifier(max_depth=None)
clf.fit(features_train, labels_train) 
pred = clf.predict(features_test)
print "DecisionTreeClassifier accuracy : ", accuracy_score(pred, labels_test)
# 1.0? #label is boolean, does that matter?

clf = RandomForestClassifier()
clf.fit(features_train, labels_train) 
pred = clf.predict(features_test)
print "RandomForestClassifier accuracy : ", accuracy_score(pred, labels_test)
# 1.0?

clf = ExtraTreesClassifier()
clf.fit(features_train, labels_train) 
pred = clf.predict(features_test)
print "ExtraTreesClassifier accuracy : ", accuracy_score(pred, labels_test)

clf = AdaBoostClassifier()
clf.fit(features_train, labels_train) 
pred = clf.predict(features_test)
print "AdaBoostClassifier accuracy : ", accuracy_score(pred, labels_test)
# 1.0?

clf = GaussianNB()
clf.fit(features_train, labels_train) 
pred = clf.predict(features_test)
print "GaussianNB accuracy : ", accuracy_score(pred, labels_test)

clf = linear_model.LogisticRegression()
clf.fit(features_train, labels_train) 
pred = clf.predict(features_test)
print "LogisticRegression accuracy : ", accuracy_score(pred, labels_test)

# question: Does the learning model exhibit bias or variance?
# question: Are there outliers/anomalies that we shouldn't ignore?


# modeling risk (for de-marketing)
# question:  Which businesses are likely to be charged with severe violations? (prediction) *more iterations of predictive model*


# modeling opportunity (for increased banking relationship)
# question:  Which businesses have positively forecasted sales? (R probably better-- forecast package) *not super interesting in aggregate, maybe at individual level*
# question:  What will be total revenue quarter by quarter or region
