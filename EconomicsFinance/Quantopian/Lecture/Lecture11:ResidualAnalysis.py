# Residuals: difference between a model's prediction and the observed values

import numpy as np
import pandas as pd
from statsmodels import regression
import statsmodels.api as sm
import statsmodels.stats.diagnostic as smd
import scipy.stats as stats
import matplotlib.pyplot as plt
import math

# plot the observed values and the prediction values
# plot the Residuals and analyze the patter, random symmetric distribution means good fit

# Heteroscedasticity: data is non-constant variance

# Statistical Methods for Detecting Heteroscedasticity: the Breusch-Pagan hypothesis test

# Adjusting for Heteroscedasticity
# 1 Differences Analysis
# 2 Logarithmic Transformation
# 3 Box-Cox Transformation

# Autocorrelation: A series is autocorrelated when it is correlated with a delayed version of itself.

# in finance, stock prices are usually autocorrelated, while stock returns are independent from one day to the next.

# Example
