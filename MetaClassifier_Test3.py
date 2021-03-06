# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 18:12:32 2016

@author: Yannis Mentekidis

Tests problem accuracy and precision for different classifiers
"""


""" Load Libraries """
# pandas and numpy
import pandas as pd
import numpy as np

#preprocessing
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

#classifiers
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import MetaClassifier_Class as mclf

#plotting
import matplotlib.pyplot as plt
font = {'family' : 'normal',
        'size' : 22}
plt.rc('font', **font)


""" Define shuffling function """
def shuffle_in_unison_inplace(a, b):
    shuf = np.random.permutation(a.index)
    a=a.reindex(shuf)
    b=b.reindex(shuf)
    return (a,b)



""" Load Data """
X = pd.read_csv('data/source-code-metrics_train.csv', ';')
y = pd.read_csv('data/bugs_train.csv', ';')
X.set_index('classid', inplace=True)
y.set_index('classid', inplace=True)

Xtst = pd.read_csv('data/source-code-metrics_test.csv', ';')
Xtst.set_index('classid', inplace=True)

ytst = pd.read_csv('data/bugs_test.csv', ';')
ytst.set_index('classid', inplace=True)

""" Create Metaclassifier Scheme """

"""
Create ensemble of classifiers
"""

#unbiased classifiers
knn1 = KNeighborsClassifier(n_neighbors=12, metric='chebyshev')
knn2 = KNeighborsClassifier(n_neighbors=9, metric='canberra')
giniTree_unbiased = tree.DecisionTreeClassifier(criterion='gini')
entropyTree_unbiased = tree.DecisionTreeClassifier(criterion='entropy')
svm_unbiased = make_pipeline(StandardScaler(), SVC(kernel='rbf'))
gnb = GaussianNB()
giniRfc = RandomForestClassifier(n_estimators=100, min_samples_split=2, n_jobs=-1)
entropyRfc = RandomForestClassifier(n_estimators=100, min_samples_split=2, n_jobs=-1, criterion='entropy')
log_reg_unb = make_pipeline(StandardScaler(), LogisticRegression(class_weight={0:1, 1:1}, C=0.5))

#biased classifiers
cw = {0:1, 1:10}
giniTree = tree.DecisionTreeClassifier(criterion='gini', class_weight=cw, min_samples_split=30)
entropyTree = tree.DecisionTreeClassifier(criterion='entropy', class_weight=cw, min_samples_split=30)
svm = make_pipeline(StandardScaler(), SVC(kernel='rbf', class_weight={0:1, 1:4}))
giniRfc_bias = RandomForestClassifier(n_estimators=100, min_samples_split=2, n_jobs=-1, class_weight=cw )
entropyRfc_bias = RandomForestClassifier(n_estimators=100, min_samples_split=2, n_jobs=-1, class_weight=cw, criterion='entropy')
log_reg_bias = make_pipeline(StandardScaler(), LogisticRegression(class_weight={0:1, 1:4}, C=0.5))

ens1 = [knn1, knn2, entropyTree, entropyRfc, svm, entropyRfc_bias]


ensemble = ens1
"""
Create aggregator
"""
#aggregator = tree.DecisionTreeClassifier(criterion='entropy', class_weight={0:1, 1:2})
#aggregator  = KNeighborsClassifier(n_neighbors=(len(ensemble)-1), metric='hamming')
aggregator = SVC(kernel='rbf', class_weight={0:1, 1:1})
clf1 = mclf.MetaClassifier(ensemble, aggregator, useSMOTE=True)

""" Create other classifiers for the problem """
#
clf2 = KNeighborsClassifier(n_neighbors=12, metric='chebyshev')
clf3 = tree.DecisionTreeClassifier(criterion='entropy', class_weight={0:1, 1:2})
clf4 = GaussianNB()
clf5 = make_pipeline(StandardScaler(), SVC(kernel='rbf', class_weight={0:1, 1:2}))

classifiers = [clf1, clf2, clf3, clf4, clf5]
classifier_names = ['Metaclassifier','kNN', 'Decision Tree', 'Gaussian NB', 'SVM']

""" SMOTE initial dataset X """
from unbalanced_dataset import SMOTE
X = X.as_matrix()
y = y.as_matrix().ravel()
bugs = sum(y)
ratio = float(len(y)-bugs)/bugs
smote = SMOTE(ratio=ratio, verbose=False, kind='borderline1')

""" Train and test to report accuracy and precision """
accuracy_peragg=[]
prec_peragg=[]

for classifier, clf_name in zip(classifiers, classifier_names):
    tries = 30
    accuracy = []
    prec=[]
    
    print "Classifier", clf_name
    for i in range(tries):
        
        print "\tTraining %d of %d" %(i+1, tries)
        
        #Train with X, predict on Xtst
        classifier.fit(X, y)
        
        H = classifier.predict(Xtst.as_matrix())

        from sklearn.metrics import accuracy_score, recall_score
        
        acc = accuracy_score(ytst, H)
        precision = recall_score(ytst, H)
        
        
        accuracy.append(acc)
        prec.append(precision)
        
    accuracy_peragg.append(accuracy)
    prec_peragg.append(prec)

print np.mean(accuracy_peragg[0]) 
print np.mean(prec_peragg[0])
 
plt.figure(1)
plt.boxplot(accuracy_peragg)
plt.xticks(range(1, len(classifier_names)+1), classifier_names)
plt.title('Accuracy of classifiers')
plt.ylabel('Accuracy')
#plt.xlabel('Classifer')
plt.axis([0, len(classifier_names)+1, 0, 1])

plt.figure(2)
plt.boxplot(prec_peragg)
plt.xticks(range(1, len(classifier_names)+1), classifier_names)
plt.title('Precision of classifiers')
plt.ylabel('Precision')
#plt.xlabel('Classifier')
plt.axis([0, len(classifier_names)+1, 0, 1])
plt.show()
