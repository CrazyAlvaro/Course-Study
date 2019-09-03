import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats

xs = np.linspace(-6, 6, 300)
normal = stats.norm.pdf(xs)
plt.plot(xs, normal)

# A distribution which is not symmetric is called skewed
start = '2012-01-01'
end = '2015-01-01'

pricing = get_pricing('SPY', fields='price', start_date=start, end_date=end)
returns = pricing.pct_change()[1:]

print 'Skew:', stats.skew(returns)
print 'Mean:', np.mean(returns)
print 'Median:', np.median(returns)

plt.hist(returns, 30)

# Kurtosis: measure the shape of the deviation from the mean, normal distribution has kurtosis of 3

plt.show()
