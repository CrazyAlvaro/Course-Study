# Arithmetic mean

import scipy.stats as stats
import numpy as np

x1 = [1, 2, 2, 3, 4, 5, 5, 7]
x2 = x1 + [100]

np.mean(x1)

# Median
np.median(x1)

# Mode
# most frequent occurence

stats.mode(x1)[0][0]

start = '2014-01-01'
end = '2015-01-01'
pricing = get_pricing('SPY', fields = 'price', start_date=start, end_date=end)
returns = pricing.pct_change()[1:]
print 'Mode of returns:', mode(returns)

hist, bins = np.histogram(returns, 20)
maxfreq = max(hist)

# find all bins thit with frequency maxfreq, then print the intervals corresponding to them
print 'Mode of bins:', [(bins[i], bins[i+1]) for i,j in enumerate(hist) if j == maxfreq]

# Geometric mean
stats.gmean(x1)

# harmonic mean
stats.hmean(x1)
