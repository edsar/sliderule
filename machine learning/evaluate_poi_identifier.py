#!/usr/bin/python


"""
    Starter code for the evaluation mini-project.
    Start by copying your trained/tested POI identifier from
    that which you built in the validation mini-project.

    This is the second step toward building your POI identifier!

    Start by loading/formatting the data...
"""

import pickle
import sys
sys.path.append("/Users/Ed/apps/ud120-projects/tools/")
from feature_format import featureFormat, targetFeatureSplit
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn import cross_validation
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

data_dict = pickle.load(open("/Users/Ed/apps/ud120-projects/final_project/final_project_dataset.pkl", "r") )

### first element is our labels, any added elements are predictor
### features. Keep this the same for the mini-project, but you'll
### have a different feature list when you do the final project.
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)

labels, features = targetFeatureSplit(data)

features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(features, labels, test_size=0.3, random_state=42) 

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features_train, labels_train)

print accuracy_score(clf.predict(features_test), labels_test)
print confusion_matrix(features_test, labels_test)
print precision_score(features_test, labels_test)
print recall_score(features_test, labels_test)

### it's all yours from here forward!  

predictions = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1] 
true_labels = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]


