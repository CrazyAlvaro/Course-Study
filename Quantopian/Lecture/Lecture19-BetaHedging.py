# Factor model Y = a + beta-1 * X-1 + beta-2 * X-2 ...

# Often beta means beta to S&P500

# Import libraries
import numpy as np
from statsmodels import regression
import statsmodels.api as sm
import matplotlib.pyplot as plt
import math

# Get data for the specified period and stocks
start = '2014-01-01'
end = '2015-01-01'
asset = get_pricing('TSLA', fields='price', start_date=start, end_date=end)
benchmark = get_pricing('SPY', fields='price', start_date=start, end_date=end)

# We have to take the percent changes to get to returns
# Get rid of the first (0th) element because it is NAN
r_a = asset.pct_change()[1:]
r_b = benchmark.pct_change()[1:]

# Let's plot them just for fun
r_a.plot()
r_b.plot()
plt.ylabel("Daily Return")
plt.legend();


# Let's define everything in familiar regression terms
X = r_b.values # Get just the values, ignore the timestamps
Y = r_a.values

def linreg(x,y):
    # We add a constant so that we can also fit an intercept (alpha) to the model
    # This just adds a column of 1s to our data
    x = sm.add_constant(x)
    model = regression.linear_model.OLS(y,x).fit()
    # Remove the constant now that we're done
    x = x[:, 1]
    return model.params[0], model.params[1]

alpha, beta = linreg(X,Y)
print 'alpha: ' + str(alpha)
print 'beta: ' + str(beta)

X2 = np.linspace(X.min(), X.max(), 100)
Y_hat = X2 * beta + alpha

plt.scatter(X, Y, alpha=0.3) # Plot the raw data
plt.xlabel("SPY Daily Return")
plt.ylabel("TSLA Daily Return")

 # Add the regression line, colored in red
plt.plot(X2, Y_hat, 'r', alpha=0.9)

# alpha: 0.00108062811902
# beta: 1.92705010047

# 所以这个是TSLA和SPY的价格变化的 线性回归拟合 beta就是价格变化的相关系数

# Risk Exposure
# High beta means HIGH risk, 相关性大的话会随着市场的波动对收益产生很大的影响

# as it means that the strategy is agnostic to market conditions.
# It will make money equally well in a crash as it will during a bull market.

########################################################################
##
##  目的就是要把和市场走势有关系的 beta全部尽可能去掉，只留下绝对收益 alpha
##  这样不管市场牛还是熊，我都能赚钱，而且回撤率能够保持的很低
##
########################################################################a

# Risk Management
# The process of reducing exposure to other factors

# Hedging: 对冲就是做空SPY来 去除大盘的走势影响

# Beta = 0, strategy is market neutral

# 现实情况是 beta 是会随着事件改变的，而且很难去预测，所以很难做到market neutral

# Implementing hedging

# Construct a portfolio with beta hedging
portfolio = -1*beta*r_b + r_a
portfolio.name = "TSLA + Hedge"

# Plot the returns of the portfolio as well as the asset by itself
portfolio.plot(alpha=0.9)
r_b.plot(alpha=0.5);
r_a.plot(alpha=0.5);
plt.ylabel("Daily Return")
plt.legend()

# 计算 原来和对冲后的 收益率 与 标准差（risk）
print "means: ", portfolio.mean(), r_a.mean()
print "volatilities: ", portfolio.std(), r_a.std()

# means:  0.00108062811902 0.00202262496904
# volatilities:  0.0272298767724 0.0304875405804

# 降低 beta 的同时alpha 也会降低, 但是只要volatile变小，就可以通过加 杠杆（leverage） 的方式提升收益率

########################################################################
##
##  High beta 虽然牛市赚的更多，但是熊市亏的也多，长期来看收益率不好，Graham也提到这点
##  所以才需要有 safety margin，为了目的就是要减少 回撤率，降低风险，而不是一味追求收益
##
########################################################################

# Other type of hedging

# Pairs Trading: two stock reducing industry affect

# Long Short Equity: long short a lot of random ranking securities, assumed let's say 100 long and 100 short
# result total beat 1 - 1 = 0
