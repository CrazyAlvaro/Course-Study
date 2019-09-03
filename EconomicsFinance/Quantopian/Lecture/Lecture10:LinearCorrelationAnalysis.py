# Correlation is simply a normalized form of covariance.
# 线性相关读

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

X = np.random.rand(50)
Y = 2 * X + np.random.normal(0, 0.1, 50)

print np.cov(X, Y)[0, 1]

print np.corrcoef(X,Y)[0, 1]

# How is this useful in finance

# Determining related assets

start = '2013-01-01'
end = '2015-01-01'
bench = get_pricing('SPY', fields='price', start_date=start, end_date=end)
lrcx_price = get_pricing('LRCX', fields='price', start_date=start, end_date=end)
aapl_price = get_pricing('AAPL', fields='price', start_date=start, end_date=end)

print 'Correlation coefficients'
print 'LRXC and AAPL', np.corrcoef(lrcx_price, aapl_price)[0, 1]
print 'LRXC and SPY', np.corrcoef(lrcx_price, bench)[0, 1]
print 'LRXC and SPY', np.corrcoef(bench, aapl_price)[0, 1]

# Constructing a portfolio of uncorrelated assets

# Limitations:
# Significance: correlation varies on time periods

# Non-Linear Relationships:

# 1: delayed affaction
# 2: a variable may related to the rate of change of another
# Both are Non-Linear
