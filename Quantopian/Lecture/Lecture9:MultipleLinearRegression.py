import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

from statsmodels import regression

# use Ordinary Least-Squares(OLS)

# Construct a simple linear curve of 1, 2, 3, ...
X1 = np.arange(100)

# Make a parabola and add X1 to it, this is X2
X2 = np.array([i ** 2 for i in range(100)]) + X1

Y = X1 + X2

plt.plot(X1, label='X1')
plt.plot(X2, label='X2')
plt.plot(Y, label='Y')
plt.legend()

X = sm.add_constant( np.column_stack( (X1, X2) ) )

# Run the model
results = regression.linear_model.OLS(Y, X).fit()

print 'Beta_0:', results.params[0]
print 'Beta_0:', results.params[1]
print 'Beta_0:', results.params[2]

# plt.show()
