import numpy as np

np.random.seed(121)

X = np.random.randint(100, size=20)
X = np.sort(X)
print 'X: %s' %(X)

mu = np.mean(X)
print 'Mean of X:', mu

# Range
print 'Range of X: %s' %(np.ptp(X))

# Mean Absolute Deviation(MAD)
abs_dispersion = [np.abs(mu - x) for x in X]
MAD = np.sum(abs_dispersion)/len(abs_dispersion)
print 'Mean absolute deviation of X:', MAD

# Variance and standard deviation
print 'Variance of X:', np.var(X)
print 'Standard deviation of X:', np.std(X)

# Chebyshev's inequality
k = 1.25
dist = k*np.std(X)
l = [x for x in X if abs(x - mu) <= dist]
print 'Observations within', k, 'stds of mean:', 1
print 'Confirming that', float(len(l))/len(X), '>', 1 - 1/k**2

# Semivariance and semideviation
# only count the observations that fall below the mean
lows = [e for e in X if e <= mu]

semivar = np.sum( (lows - mu) ** 2 ) / len(lows)

print 'Semivariance of X:', semivar
print 'Semideviation of X:', np.sqrt(semivar)

# target semivariance, target semideviation, replace mu with customize value
