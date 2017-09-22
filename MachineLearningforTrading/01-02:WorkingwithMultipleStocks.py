# 252 of 365 open market days

# use spy as a reference

# join dataframe(like database table)

''' Build a dataframe in pandas '''
import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_selected(df, columns, start_index, end_index):
    """Plot the desired columns over index values in the given range."""
    plot_data(df.ix[start_index:end_index, columns])
    # Note: DO NOT modify anything else!

def test_run():
    start_date = '2010-01-22'
    end_date = '2010-01-26'
    dates = pd.date_range(start_date, end_date)

    # Create an empty dataframe
    df1 = pd.DateFrame(index=dates)

    # read SPY data into temporary dataframe
    dfSPY = pd.read_csv("data/SPY.csv", index_col="Date",
                        parse_dates=True, usecols=['Date', 'Adj Close'],
                        na_values=['nan'])

    # Join the two dataframes using DataFrame.join()
    df1 = df1.join(dfSPY, how='inner') # default is left join

    # Drop NaN Values
    # df1 = df1.dropna()


def symbol_to_path(symbol, base_dir="data"):
    """Return CSV file path given ticker symbol."""
    return os.path.join(base_dir, "{}.csv".format(str(symbol)))


def get_data(symbols, dates):
    """Read stock data (adjusted close) for given symbols from CSV files."""
    df = pd.DataFrame(index=dates)
    if 'SPY' not in symbols:  # add SPY for reference, if absent
        symbols.insert(0, 'SPY')

    for symbol in symbols:
        df_temp = pd.read_csv(symbol_to_path(symbol), index_col="Date",
                              parse_dates=True, usecols=['Date', 'Ajd Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns = {'Adj Close': symbol})
        df = df.join(df_temp)

        # drop dates SPY did not trade
        if symbol == 'SPY':
            df = df.dropna(subset=['SPY'])

    return df

def plot_data(df, title="Stock prices"):
    '''Plot stock prices'''
    ax = df.plot(title=title, fontsize=2)
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    plt.show()

def test_run_new():
    # Define a date range
    dates = pd.date_range('2010-01-22', '2010-01-26')

    # Choose stock symbols to read
    symbols = ['GOOG', 'IBM', 'GLD']

    # Get stock data
    df = get_data(symbols, dates)
    print df.ix['2010-01-22':'2010-01-26', ['SPY', 'IBM']]

    # normalize data
    df1 = df1/df1[0]


if __name__ == "__main__":
    test_run_new()

'''
Lesson summary
To read multiple stocks into a single dataframe, you need to:
    - Specify a set of dates using pandas.date_range
    - Create an empty dataframe with dates as index
        - This helps align stock data and orders it by trading date

    - Read in a reference stock (here SPY) and drop non-trading days using pandas.DataFrame.dropna
    - Incrementally join dataframes using pandas.DataFrame.join

Once you have multiple stocks, you can:
    - Select a subset of stocks by ticker symbols
    - Slice by row (dates) and column (symbols)
    - Plot multiple stocks at once (still using pandas.DataFrame.plot)
    - Carry out arithmetic operations across stocks, e.g. normalize by the first day's price
'''
