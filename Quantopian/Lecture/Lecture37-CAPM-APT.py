import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels import regression
import matplotlib.pyplot as plt

# Idiosyncratic: company specific risk
# systematic risk: market wide

# company specific 风险可以通过portfolio减少，但是系统性风险没办法，只能以减少绝对收入来tradeoff

# E[Return] = Risk-Free Rate of Return + Risk Premium

# Risk Premium of Asset = beta * (Market Risk Premium)

######################################################################
##
##      Capital Asset Pricing Model
##
######################################################################
start_date = '2014-01-01'
end_date = '2014-12-31'

# choose stock
R = get_pricing('AAPL', fields='price', start_date=start_date, end_date=end_date).pct_change()[1:]

# risk-free proxy, Treasury Bill
R_F = get_pricing('BIL', fields='price', start_date=start_date, end_date=end_date).pct_change()[1:]

# find it's beta against market
M = get_pricing('SPY', fields='price', start_date=start_date, end_date=end_date).pct_change()[1:]

# absolute return compares to Market return
AAPL_results = regression.linear_model.OLS(R-R_F, sm.add_constant(M)).fit()
AAPL_beta = AAPL_results.params[1]

M.plot()
R.plot()
R_F.plot()
plt.xlabel('Time')
plt.ylabel('Daily Percent Return')
plt.legend();

AAPL_results.summary()

# E[Ri]=RF+β(E[RM]−RF)
predictions = R_F + AAPL_beta*(M - R_F) # CAPM equation

predictions.plot()
R.plot(color='Y')
plt.legend(['Prediction', 'Actual Return'])

plt.xlabel('Time')
plt.ylabel('Daily Percent Return')

######################################################################
#
# CAPM Assumptions
# 1 investors are able to trade without delay or cost, everyone is able to browwor or lend money at the risk-free rate
# 2 investors are all 'mean-variance optimizers', they demand the highest return for a given level of risk
#
######################################################################

from scipy import optimize
import cvxopt as opt
from cvxopt import blas, solvers

np.random.seed(123)

# Turn off progress printing
sovlers.options['show_progress'] = False

# Number of assets
n_assets = 4

# Number of observations
n_obs = 2000

## Generating random returns for our 4 securities
return_vec = np.random.randn(n_assets, n_obs)  # 4 * 2000 matrix

def rand_weights(n):
    '''
    Produces n random weights that sum to 1
    '''
    k = np.random.rand(n)
    return k / sum(k)

def random_portfolio(returns):
    '''
    Returns the mean and standard deviation of returns for a random portfolio
    '''
    # returns (4, 2000)
    p = np.asmatrix(np.mean(returns, axis=1))  # 0 vertical, 1 horizontal   P (4, )
    w = np.asmatrix(rand_weights(returns.shape[0])) # W (4, )

    # returns (4, 2000), 对角线是variance，off对角线是相关系数，每一行是一个变量的变化情况
    C = np.asmatrix(np.cov(returns)) # C (4, 4)

    mu = w * p.T
    sigma = np.sqrt(w * C * w.T)

    # This recursion reduces ourliers to keep plots pretty
    if sigma > 2:
        return random_portfolio(returns)
    return mu, sigma


#####################
#
#  Don't understand this function
#
#####################
def optimal_portfolios(returns):
    n = len(returns)
    returns = np.asmatrix(returns)

    N = 100000

    # Creating a list of returns to optimize the risk for
    mus = [100**5.0 * t/N - 1.0) for t in range(N)]

    # Convert to cvxopt matrices
    S = opt.matrix(np.cov(returns))
    pbar = opt.matrix(np.mean(returns, axis=1))

    # Create constraint matrices
    G = -opt.matrix(np.eye(n))
    h = opt.matrix(0.0, (n, 1))
    A = opt.matrix(1.0, (1, n))
    b = opt.matrix(1.0)

    # Calculate efficient frontier weights using quadratic programming
    portfolios = [solvers.qp(mu*S, -pbar, G, h, A, b)['x'] for mu in mus]

    ## Calculate the risk and returns of the frontier
    returns = [blas.dot(pbar, x) for x in portfolios]
    risks = [np.sqrt(blas.dot(x, S*x)) for x in portfolios]

    return returns, risks

n_portfolios = 50000

# np.column_stack: Stack a sequence of 1-D arrays as columns into a 2-D array.  (1,2,3) and (4,5,6) -> ([1, 4], [2, 5], [3, 6])
# similar: vstack, hstack: stack a sequence of arrays vertically and horizontally
means, stds = np.column_stack([random_portfolio(return_vec) for x in range(n_portfolios)])

returns, risks = optimal_portfolios(return_vec)

plt.plot(stds, means, 'o', markersize=2, color='navy')
plt.xlabel('Risk')
plt.ylabel('Return')
plt.title('Mean and Standard Deviation of Returns of Randomly Generated Portfolios')

plt.plot(risks, returns, '-', markersize=3, color='red')
plt.legend(['Portfolios', 'Efficient Frontier'])

# Capital Allocations Line(CAL), the slope of the CAL is the Sharpe ratio

def maximize_sharpe_ratio(return_vec, risk_free_rate):
    '''
    Finds the CAPM optimal portfolio from the efficient frontier
    by optimizing the Sharpe ratio
    '''
    def find_sharpe(weights):
        means = [np.mean(asset) for asset in return_vec]

        numerator = sum(weights[m] * means[m] for m in range(len(means))) - risk_free_rate

        weight = np.array(weights)

        denominator = np.sqrt(weights.T.dot(np.corrcoef(return_vec).dot(weights)))

        return numerator/denominator

    guess = np.ones(len(return_vec)) / len(return_vec)

    def objective(weights):
        return -find_sharpe(weights)

    # Set up equality constrained
    cons = {'type': 'eq', 'fun': lambda x: np.sum(np.abs(x)) -1 }

    # Set up bound for individual weights
    bnds = [(0, 1)] * len(return_vec)

    resulet = optimize.minimize(objective, guess, constraints=cons, bounds=bnds, method='SLSQP', options={'disp': False})

    return results

rist_free_rate = np.mean(R_F)

results = maximize_sharpe_ratio(return_vec, risk_free_rate)

# Applying the optimal weights to each asset to get build portfolio
optimal_mean = sum(results.x[i] * np.mean(return_vec[i]) for i in range(len(results.x)))
optimal_std = np.sqrt(results.x.T.dot(np.corrcoef(return_vec).dot(results.x)))

# Plot fo all possible portfolios
plt.plot(stds, means, 'o', markersize=2, color'navy')
plt.ylabel('Return')
plt.xlabel('Risk')

# Line from the risk-free rate to the optimal portfolio
eqn_of_the_line = lambda x : ( (optimal_mean - risk_free_rate) / optimal_std ) * x + risk_free_rate

xrange = np.linspace(0., 1., num=11)

plt.plot(xrange, [eqn_of_the_line(x) for x in xrange], color='red', linestyle='-', linewidth=2)

# optimal protfolio
plt.plt([optimal_std], [optimal_mean], marker='o', markersize=12, color='navy')
plt.legend(['Portfolios', 'Capital Allocation Line', 'Optimal Portfolio'])

# Capital Market Line is CAL throught market portfolio


######################################################################
#
#  Arbitrage Pricing Theory
#
######################################################################
from quantopian.pipeline import Pipeline
from quantopian.pipeline.data import Fundamentals
from quantopian.pipeline.factors import Returns, Latest
from quantopian.pipeline.filters import Q1500US
from quantopian.research import run_pipeline
from quantopian.pipeline.classifiers.fundamentals import Sector
import itertools

def make_pipeline():

    pipe = Pipeline()

    # Add our factors to the pipeline
    purchase_of_biz = Latest([Fundamentals.purchase_of_business])
    pipe.add(purchase_of_biz, 'purchase_of_business')

    RD = Latest([Fundamentals.research_and_development])
    pipe.add(RD, 'RD')

    operating_cash_flow = Latest([Fundamentals.operating_cash_flow])
    pipe.add(operating_cash_flow, 'operating_cash_flow')

    # Create factor rankings and add to pipeline
    purchase_of_biz_rank = purchase_of_biz.rank()
    RD_rank = RD.rank()
    operating_cash_flow_rank = operating_cash_flow.rank()

    pipe.add(purchase_of_biz_rank, 'purchase_of_biz_rank')
    pipe.add(RD_rank, 'RD_rank')
    pipe.add(operating_cash_flow_rank, 'operating_cash_flow_rank')

    most_biz_bought = purchase_of_biz_rank.top(1000)
    least_biz_bought = purchase_of_biz_rank.bottom(1000)

    most_RD = RD_rank.top(1000)
    least_RD = RD_rank.bottom(1000)

    most_cash = operating_cash_flow_rank.top(1000)
    least_cash = operating_cash_flow_rank.bottom(1000)

    pipe.add(most_biz_bought, 'most_biz_bought')
    pipe.add(least_biz_bought, 'least_biz_bought')

    pipe.add(most_RD, 'most_RD')
    pipe.add(least_RD, 'least_RD')

    pipe.add(most_cash, 'most_cash')
    pipe.add(least_cash, 'least_cash')

    # We also get daily returns
    returns = Returns(window_length=2)

    # and sector types
    sectors = Sector()

    pipe.add(returns, "Returns")

    # We will focus on technology stocks in the Q1500
    pipe.set_screen(
        (Q1500US() & sectors.eq(311)) &
        most_biz_bought | least_biz_bought |
        most_RD | least_RD |
        most_cash | least_cash
    )

    return pipe

pipe = make_pipeline()
results = run_pipeline(pipe, start_date, end_date)

results.head()

most_biz_bought = results[results.most_biz_bought]['Returns'].groupby(level=0).mean()
least_biz_bought = results[results.least_biz_bought]['Returns'].groupby(level=0).mean()

most_RD = results[results.most_RD]['Returns'].groupby(level=0).mean()
least_RD = results[results.least_RD]['Returns'].groupby(level=0).mean()

most_cash = results[results.most_cash]['Returns'].groupby(level=0).mean()
least_cash = results[results.least_cash]['Returns'].groupby(level=0).mean()

# Calculating our factor return streams
# go long the assets on top and short the ones in the bottom
biz_purchase_portfolio = most_biz_bought - least_biz_bought
RD_portfolio = most_RD - least_RD
cash_flow_portfolio = most_cash - least_cash
