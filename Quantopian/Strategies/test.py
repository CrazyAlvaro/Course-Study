import numpy as np
import matplotlib.pyplot as plt

n = 10
xs = np.random.randn(n).cumsum()
print xs, '\n'
i = np.argmax(np.maximum.accumulate(xs) - xs) # end of the period
print np.maximum.accumulate(xs), '\n'
print np.maximum.accumulate(xs) - xs, '\n'
print i, '\n'
j = np.argmax(xs[:i]) # start of period
print j

plt.plot(xs)
plt.plot([i, j], [xs[i], xs[j]], 'o', color='Red', markersize=10)
