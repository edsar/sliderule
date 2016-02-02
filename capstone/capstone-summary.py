import pandas as pd
import sys
import numpy as np
from __future__ import division
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
from sklearn.learning_curve import validation_curve
import matplotlib.pyplot as plt
from sklearn import svm, datasets
from sklearn.metrics import roc_curve, auc
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import label_binarize
from sklearn.multiclass import OneVsRestClassifier
from sklearn.cross_validation import StratifiedKFold
from scipy import interp
import datetime
import statsmodels.api as sm
import pylab as pl

# applicants = pd.read_csv("https://www.dropbox.com/s/8qnv7cx96xar1oc/applicants_transformed_scrubbed.csv?dl=1")

#aged
#6mo
# applicants = pd.read_csv("https://www.dropbox.com/s/35us6fp8nfcl4pr/aged_lt_6mo.csv?dl=1") #6mo
# applicants = pd.read_csv("https://www.dropbox.com/s/ul4qdmqrcgn03fe/aged_6-12mo.csv?dl=1") #6-12mo
# applicants = pd.read_csv("https://www.dropbox.com/s/li5bes2f7yrc9a1/aged_12-24mo.csv?dl=1") #12-24mo
applicants = pd.read_csv("https://www.dropbox.com/s/nw6x2j40l3hsep5/aged_gt_24mo.csv?dl=1") #24+mo

applicants["Total Sales"] = applicants["Total Sales"].str.replace(',','')
applicants["Total Sales"] = applicants["Total Sales"].astype('float')
applicants["Excise Tax Due"] = applicants["Excise Tax Due"].str.replace(',','')
applicants["Excise Tax Due"] = applicants["Excise Tax Due"].astype('float')
applicants["violator"] = applicants["Violation Count"] > 0

#applicants["Total Sales"].describe()
#applicants["Total Sales"].head(25)

features = applicants[["Total Sales", "Excise Tax Due", "Tax Rate", "Type:Medical", "Type:Processor", "Type:Producer", "Type:Retailer"]] 
labels = applicants["violator"]

features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, labels, test_size=0.3) 

##########
########## Decision Tree

clf = tree.DecisionTreeClassifier(max_depth=None)
clf.fit(features_train, labels_train) 
pred = clf.predict(features_test)
acc = accuracy_score(pred, labels_test)
print "DecisionTreeClassifier accuracy : " , acc


X = features
y = labels

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=0)

# The model by itself
y_pred = clf.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_pred)

plt.figure(1)
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr, label='DecisionTree acc: ' + repr(acc))
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC curve - Runners')
plt.legend(loc='best')
plt.show()

######### Random Forest

clf = RandomForestClassifier()
clf.fit(features_train, labels_train) 
pred = clf.predict(features_test)
acc = accuracy_score(pred, labels_test)

print "RandomForestClassifier accuracy : ", acc

X = features
y = labels

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=0)

# The model by itself
y_pred = clf.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_pred)

plt.figure(1)
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr, label='RandomForest acc: ' + repr(acc))
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC curve - Runners')
plt.legend(loc='best')
plt.show()

############### AdaBoost

clf = AdaBoostClassifier()
clf.fit(features_train, labels_train) 
pred = clf.predict(features_test)
acc = accuracy_score(pred, labels_test)

print "AdaBoostClassifier accuracy : ", acc

X = features
y = labels

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=0)

# The model by itself
y_pred = clf.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_pred)

plt.figure(1)
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr, label='AdaBoost acc: ' + repr(acc))
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC curve - Runners')
plt.legend(loc='best')
plt.show()

###########Gaussian NB

clf = GaussianNB()
clf.fit(features_train, labels_train) 
pred = clf.predict(features_test)
acc = accuracy_score(pred, labels_test)

print "GaussianNB accuracy : ", acc

X = features
y = labels

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=0)

# The model by itself
y_pred = clf.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_pred)

plt.figure(1)
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr, label='GaussianNB acc:' + repr(acc))
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC curve - Runners')
plt.legend(loc='best')
plt.show()

######Logistic Regression

clf = linear_model.LogisticRegression()
clf.fit(features_train, labels_train) 
pred = clf.predict(features_test)
clf = linear_model.LogisticRegression()
clf.fit(features_train, labels_train) 
pred = clf.predict(features_test)
acc = accuracy_score(pred, labels_test)

print "LogisticRegression accuracy : ", acc

X = features
y = labels

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.3, random_state=0)

# The model by itself
y_pred = clf.predict_proba(X_test)[:, 1]
fpr, tpr, _ = roc_curve(y_test, y_pred)

plt.figure(1)
plt.plot([0, 1], [0, 1], 'k--')
plt.plot(fpr, tpr, label='Logit acc: ' + repr(acc))
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC curve - Runners')
plt.legend(loc='best')
plt.show()