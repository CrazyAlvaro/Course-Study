import pandas as pd
import matplotlib.pyplot as plt

def get_mean_volume(symbol):
    """Return the mean volume for stock indicated by symbol.

    Note: Data for a stock is stored in file: data/<symbol>.csv
    """
    df = pd.read_csv("data/{}.csv".format(symbol))  # read in data
    return df['Volume'].mean()


def test_run():
    """Function called by Test Run."""
    for symbol in ['AAPL', 'IBM']:
        print "Mean Volume"
        print symbol, get_mean_volume(symbol)

def test_run_plot():
    df = pd.read_csv("data/IBM.csv")
    # print df['Adj Close']
    print df['High'].plot()
    df[['Close', 'Adj Close']].plot()  # plot two columns
    plt.show() # must be called to show plots


if __name__ == "__main__":
    test_run()
