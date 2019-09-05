########################################
# Lecture
########################################

# LESS IS MORE

# Matplotlib: Backend Layer, Artist Layer, Scripting Layer

# Pandas has built-in matplotlib, call plot() function

########################################
# Lab
########################################
import numpy as np
import pandas as pd

df_can = pd.read_excel('link')

# index/columns to list
df_can.columns.tolist()

# Data shape
df_can.shape

# axis = 1 represents columns
df_can.drop(['AREA','REG', 'DEV', 'Type', 'Coverage'], axis=1, inplace=True)

df_can.rename(columns={'OdName': 'Country'})
df_can.describe()

# df.loc['label']
# df.iloc['index']

df_can.loc['Japan', [1980, 1981]]
df_can.iloc[87,[3,4]]

# Convert columns to string
df_can.columns = list(map(str, df_can.columns))

########################################
# Visualizing Data using Matplotlib
########################################
# using the inline backend
# %matplotlib inline

import matplotlib as mpl
import matplotlib.pyplot as plt

print(plt.style.available)
mpl.style.use(['ggplot'])

years = list(map(str, range(1980,2004)))
haiti = df_can.loc['Haiti', years]
haiti.index = haiti.index.map(int)
haiti.plot(kind='line')

plt.title('Immigration from Haiti')
plt.ylabel('Number of Immigrants')
plt.xlabel('Years')
plt.text('x_index', 'y_index', 'text to show')

plt.show()

# NOTE: 1 dimensional data from dataframe is Series, which multi is Dataframe
top_5 = df_can.sort_values(by='Total', ascending=False).head(5).T
top_5.index = top_5.index.map(int)
top_5.plot(kind='line', figsize=(14,8))