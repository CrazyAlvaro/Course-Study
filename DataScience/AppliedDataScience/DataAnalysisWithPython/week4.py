import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.DataFrame()
lm = LinearRegression()
########################################
# Linear Regression
########################################
# Y is target/dependent variable
X = df[['highway_mpg']]
# X is predicator/independent variable
Y = df['price']

lm.fit(X,Y)
Yhat = lm.predict(X)

########################################
# Module 4: Model Development
########################################

# intercept
lm.intercept_
##########
# slope
##########
lm.coef_

import seaborn as sns

##########
# regression plot
##########
sns.regplot(x="highway-mpg", y="price", data=df)
plt.ylim(0,)

plt.figure(figsize=(12,10))
sns.residplot(df["highway-mpg"], df["price"])
# randomly spread around X, linear realtionship
# Not, non-linear relationship

##########
# distribution plot
##########
# Compare actual price with predicted price
Yhat = lm.predict(df["price"])
ax1 = sns.distplot(df['price'], hist=False, color='r', label='Actual Value')
sns.distplot(Yhat, hist=False, color='b', label='Fitted Values', ax=ax1)


########################################
# 3 Polynomial Regression and Pipelines
########################################
def PlotPolly(model, independent_variable, dependent_variable, Name):
  x_new = np.linspace(15, 55, 100)
  y_new = model(x_new)

  plt.plot(independent_variable, dependent_variable, '.', x_new, y_new, '-')
  plt.title('Polynomial Fit with Matplotlib for Price ~ Length')
  ax = plt.gca()
  ax.set_facecolor((0.898, 0.898, 0.898))
  # fig = plt.gcf()
  plt.gcf()
  plt.xlabel(Name)
  plt.ylabel('Price of Cars')

  plt.show()
  plt.close()

x = df['highway']
y = df['price']

# a polynomial of the 3rd order
f = np.polyfit(x, y, 3)
p = np.poly1d(f)

##########
# Pipeline
##########
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

Z = df['highway-mpg']
Input = [('scale', StandardScaler()), ('model', LinearRegression())]

pipe=Pipeline(Input)

pipe.fit(Z, y)

########################################
# 4 Measures for In-Sample Evaluation
########################################
# 量化描述模型的好坏

# - R^2/R-squared: the coefficient of determination, is a measure to indicate how close the data is to the fitted regression line.
# - Mean Squared Error (MSE): The value of the R-squared is the percentage of variation of the response variable(y) that is explained by a linear model

# R-squared
lm.fit(X, Y)
lm.score(X, Y)

# MSE
from sklearn.metrics import mean_squared_error
mse = mean_squared_error(df['price'], Yhat)




