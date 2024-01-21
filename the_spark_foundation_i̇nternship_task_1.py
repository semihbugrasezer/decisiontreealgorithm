# -*- coding: utf-8 -*-
"""The Spark Foundation İnternship Task 1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1t9bOCecituqrP6FmavzzFj409BtO3Gts

# Prediction using Decision Tree Algorithm (Level - Intermediate) The Spark Foundation

**Semih Bugra Sezer **
"""

# Importing libraries in Python
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import preprocessing
import pandas as pd

# Loading the iris dataset
iris = pd.read_csv('/content/Iris.csv')

# Attribute values
A = iris.iloc[:, :-1]

# Target values
b = iris.iloc[:, -1]

# Label Encoder
le = preprocessing.LabelEncoder()
b = le.fit_transform(b)

print(A.head())
print(b)

A.info()

A.describe()

"""**Visualizing Iris Data**"""

plt.scatter(iris['SepalLengthCm'],iris['SepalWidthCm'])
plt.show()

#Using Seaborn lib to visualized 2 features based on target variable.

sns.set_style('whitegrid')
sns.FacetGrid(iris, hue = 'Species') \
   .map(plt.scatter, 'SepalLengthCm','SepalWidthCm') \
   .add_legend()

plt.show()

#Pair plot gives the relationship b/w all features distribution with each other..

sns.pairplot(iris.drop(['Id'],axis=1), hue='Species')
plt.show()

"""**Exploring Some New Features**"""

#Just trying to explore some new feature using the given data...

iris['Sepal_diff'] = iris['SepalLengthCm']-iris['SepalWidthCm']
iris['petal_diff'] = iris['PetalLengthCm']-iris['PetalWidthCm']
iris

#Analysed new feature to get some more infomation apart form existing ones...

sns.set_style('whitegrid')
sns.FacetGrid(iris, hue='Species') \
    .map(plt.scatter, 'Sepal_diff', 'petal_diff') \
    .add_legend()
plt.show()


sns.set_style('whitegrid')
sns.FacetGrid(iris, hue='Species') \
    .map(sns.histplot, 'petal_diff') \
    .add_legend()
plt.show()

iris['Sepal_petal_len_diff'] = iris['SepalLengthCm']-iris['PetalLengthCm']
iris['Sepal_petal_width_diff'] = iris['SepalWidthCm']-iris['PetalWidthCm']
iris

sns.set_style('whitegrid')
sns.FacetGrid(iris, hue='Species') \
    .map(plt.scatter, 'Sepal_petal_len_diff', 'Sepal_petal_width_diff') \
    .add_legend()
plt.show()

sns.set_style('whitegrid')
sns.FacetGrid(iris, hue='Species') \
    .map(sns.histplot, 'PetalLengthCm') \
    .add_legend()
plt.show()

iris['Sepal_petal_len_wid_diff'] = iris['SepalLengthCm']-iris['PetalWidthCm']
iris['Sepal_petal_wid_len_diff'] = iris['SepalWidthCm']-iris['PetalLengthCm']
iris

sns.set_style('whitegrid')
sns.FacetGrid(iris, hue='Species') \
    .map(plt.scatter, 'Sepal_petal_wid_len_diff', 'Sepal_petal_len_wid_diff') \
    .add_legend()
plt.show()

sns.set_style('whitegrid')
sns.FacetGrid(iris, hue='Species') \
    .map(sns.histplot, 'Sepal_petal_wid_len_diff') \
    .add_legend()
plt.show()

sns.pairplot(iris[['Species', 'Sepal_diff', 'petal_diff', 'Sepal_petal_len_diff',\
       'Sepal_petal_width_diff', 'Sepal_petal_len_wid_diff',\
       'Sepal_petal_wid_len_diff']], hue='Species')
plt.show()

#Droping Id column as it is of no use in classifing the class labels..

iris.drop(['Id'],axis=1,inplace=True)

# Exploring distribution plot for all features
for i in iris.columns:
    if i == 'Species':
        continue
    sns.set_style('whitegrid')
    sns.displot(iris, x=i, hue='Species', kind='kde', fill=True)
    plt.show()

"""**Building Classification Model**"""

from sklearn import tree
import graphviz
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split, cross_val_score

X = iris[['SepalLengthCm', 'SepalWidthCm','PetalLengthCm', 'PetalWidthCm','Sepal_petal_wid_len_diff','Sepal_petal_width_diff']]
y = iris['Species']


#Before training the model we have split our data into Actual Train and Actual Test Dataset for training and validating purpose...

Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, y, test_size=0.30, random_state=42)

#spliting data into validation train and validation test
Xt, Xcv, Yt, Ycv = train_test_split(Xtrain, Ytrain, test_size=0.10, random_state=42)

'''Now we have create a Decision tree classifier and trained it with training dataset.'''


Iris_clf = DecisionTreeClassifier(criterion='gini',min_samples_split=2)
Iris_clf.fit(Xt, Yt)

#Visualized the Tree which is formed on train dataset

tree.plot_tree(Iris_clf)

#Visualizing Decision Tree using graphviz library

dot_data = tree.export_graphviz(Iris_clf, out_file=None)

graph = graphviz.Source(dot_data)
graph

# As our model has been trained....
#Now we can validate our Decision tree using cross validation method to get the accuracy or performance score of our model.

print('Accuracy score is:',cross_val_score(Iris_clf, Xt, Yt, cv=3, scoring='accuracy').mean())

#Checking validation test data on our trained model and getting performance metrices

from sklearn.metrics import multilabel_confusion_matrix, accuracy_score

Y_hat = Iris_clf.predict(Xcv)


print('Accuracy score for validation test data is:',accuracy_score(Ycv, Y_hat))
multilabel_confusion_matrix(Ycv , Y_hat)

#Checking our model performance on actual unseen test data..
YT_hat = Iris_clf.predict(Xtest)
YT_hat

print('Model Accuracy Score on totally unseen data(Xtest) is:',accuracy_score(Ytest, YT_hat)*100,'%')
multilabel_confusion_matrix(Ytest , YT_hat)

'''Training model on Actual train data... '''
Iris_Fclf = DecisionTreeClassifier(criterion='gini',min_samples_split=2)
Iris_Fclf.fit(Xtrain, Ytrain)

#Visualize tree structure..
tree.plot_tree(Iris_Fclf)

#Final Decision tree build for deploying in real world cases....

dot_data = tree.export_graphviz(Iris_Fclf, out_file=None)
graph = graphviz.Source(dot_data)
graph

#Checking the performance of model on Actual Test data...

YT_Fhat = Iris_Fclf.predict(Xtest)
YT_Fhat

print('Model Accuracy Score on totally unseen data(Xtest) is:',accuracy_score(Ytest, YT_Fhat)*100,'%')
multilabel_confusion_matrix(Ytest , YT_Fhat)

#Testing for New points except from Dataset

Test_point = [[5.4,3.0,4.5,1.5,-1.5,1.5],
             [6.5,2.8,4.6,1.5,-1.8,1.3],
             [5.1,2.5,3.0,1.1,-0.5,1.4],
             [5.1,3.3,1.7,0.5,1.6,2.8],
             [6.0,2.7,5.1,1.6,-2.4,1.1],
             [6.0,2.2,5.0,1.5,-2.8,0.7]]

print(Iris_Fclf.predict(Test_point))

"""**Let us visualize the Decision Tree to understand it better.**"""

# Import necessary libraries for graph viz
from sklearn.tree import export_graphviz
from io import StringIO
from IPython.display import Image
import pydotplus

# Visualize the graph
dot_data = StringIO()
export_graphviz(Iris_Fclf, out_file=dot_data, feature_names=X.columns,
                filled=True, rounded=True,
                special_characters=True)

graph = pydotplus.graph_from_dot_data(dot_data.getvalue())
Image(graph.create_png())