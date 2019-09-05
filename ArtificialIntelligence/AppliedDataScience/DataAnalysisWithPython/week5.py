####################
# Ridge Regression
####################

# Ridge(alpha=1)
# Use cross_validation to prevent overfitting/underfitting

# Alpha, hyperparameters

####################
# Grid Search
####################
# scikit-learn has a means automatically iterate through hyperparameters
# Use VALIDATION data to select

# alpha, normalization
parameters=[{'alpha': [1,10,100], 'normalize':[True, False]}]

####################
# Lab
####################
import pandas as pd
import numpy as np

path = ''
df = pd.read_csv(path)
df = df._get_numeric_data()

y_data = df['price']
x_data = df.drop('price', axis=1)
# Plotting libraries
# ! pip install ipywidgets

########################################
# Train and Testing 
########################################
# Data split to train, test
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, random_state=0)

from sklearn.linear_model import LinearRegression 
lre=LinearRegression()

# Cross Validataion: cross_val_score
from sklearn.model_selection import cross_val_score
Rcross = cross_val_score(lre, x_data['horsepower'], y_data, cv=4)

from sklearn.model_selection import cross_val_predict
yhat = cross_val_score(lre, x_data['horsepower'], y_data, cv=4)

########################################
# Overfitting, Underfitting and Model Selection 
########################################
from sklearn.preprocessing import PolynomialFeatures
pr=PolynomialFeatures(degree=5)
x_train_pr = pr.fit_transform(x_train[['horsepower']])
x_test_pr = pr.fit_transform(x_test[['horsepower']])

# try different order avoid overfitting
order=[1,2,3,4]

########################################
# Ridge regression
########################################
# 本质上是添加一个Hyper parameter防止过拟合
from sklearn.linear_model import Ridge
RidgeModel =Ridge(alpha=0.1)
RidgeModel.fit(x_train_pr, y_train)
yhat = RidgeModel.predict(x_test_pr)

########################################
# Grid Search
########################################
# 本质上是一种自带最优化选择参数的模型

from sklearn.model_selection import GridSearchCV
parameters=[{'alpha': [0.001, 0.01,1,10]}]
GridRidge  = Ridge()

# pass parameters, cv
Grid1=GridSearchCV(GridRidge, parameters, cv=4)
Grid1.fit(x_data[['horsepower', 'curb-weight']], y_data)

BestRR=Grid1.best_estimator_
BestRR.score(x_test[['horsepower', 'curb-weight']], y_test)