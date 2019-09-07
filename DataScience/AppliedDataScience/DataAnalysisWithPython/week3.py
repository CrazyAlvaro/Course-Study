#### week 3 ####
# pivot table: 数据透视表
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

########################################
# 2 Analyzing Individual Feature Patterns using Visualization
########################################
df = pd.DataFrame()
sns.regplot(x="engine-size", y="price", data=df)
plt.ylim(0,)

# continuous numerical variables
# Positive/Negative linear relationship

# Categorical variable
sns.boxplot(x="body-style", y="price", data=df)

########################################
#  3 Descriptive Statistical Analysis 
########################################
# Descriptive Statistical Analysis
df.describe()  # include=['object'] #categorical data

########################################
# 4 Basics of Grouping
########################################
df['drive-wheels'].value_counts().to_frame()
grouped_test1 = df.groupby(['drive-wheels'], as_index=False).mean()

# drive-wheels, body-style both categorical data
grouped_test1.pivot(index='drive-wheels', columns='body-style')

# Two dimensional matrix
grouped_pivot = grouped_test1.pivot(index='drive-wheels',columns='body-style')

# Plot using heatmap
plt.pcolor(grouped_pivot, cmap="RdBu")
plt.colorbar()

fig, ax = plt.subplots()
im = ax.pcolor(grouped_pivot, cmap="RdBu")

# label names 
row_labels = grouped_pivot.columns.levels[1]
col_labels = grouped_pivot.index

# move ticks and labels to the center
ax.set_xticks(np.arange(grouped_pivot.shape[1]) + 0.5, minor=False)
ax.set_xticks(np.arange(grouped_pivot.shape[0]) + 0.5, minor=False)

# insert labels
ax.set_xtickslabels(row_labels, minor=False)
ax.set_ytickslabels(col_labels, minor=False)

# rotate label if too long
plt.xticks(rotation=90)

fig.colorbar(im)
plt.show()

# Visualization is very important

########################################
# 5 Correlation and Causation
########################################

# Correlations: the extent of independence between variables
# Causation: the relationship between cause and effect between two variables

# P-Value: the probability value that the correlation between these two variables
#          is statistically significant. 两组数据相关性统计显著性的概率大小

# By convention, when the
#   p-value is  <  0.001: we say there is strong evidence that the correlation is significant.
#   the p-value is  <  0.05: there is moderate evidence that the correlation is significant.
#   the p-value is  <  0.1: there is weak evidence that the correlation is significant.
#   the p-value is  >  0.1: there is no evidence that the correlation is significant.

from scipy import stats

pearson_coef, p_value = stats.pearsonr(df['wheel-base'], df['price'])

########################################
# 6 ANOVA: Analysis of Variance
########################################

# Test whether there are significant differeence between the means of two or more groups
# F-test score: ANOVA assumes the means of all groups are the same, F-test score represent actual means deviation
# P-value: tells how statistically significant is our calculated score value

f_val, p_val = stats.f_oneway()