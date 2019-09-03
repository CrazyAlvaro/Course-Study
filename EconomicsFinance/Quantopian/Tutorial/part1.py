
'''

'''
def initialize(context):
    context.message = 'hello'

    context.aapl = sid(24)  # sid never change
    context.spy = sid(8554)

    schedule_function(open_positions, date_rules.week_start(), time_rules.market_open())
    schedule_function(close_positions, date_rules.week_end(), time_rules.market_close(minutes=30))
    schedule_function(record_vars, date_rules.every_day(), time_rules.market_close())

def open_positions(context, data):
    order_target_percent(context.spy, 0.10)

def close_positions(context, data):
    order_target_percent(context.spy, 0)

def record_vars(context, data):

    long_count = 0
    short_count = 0

    # context.portfolio
    for position in context.portfolio.positions.itervalues():
        if position.amount > 0:
            long_count += 1
        if position.amount < 0:
            short_count += 1

    # Plot the counts
    record(num_long=long_count, num_short=short_count)

'''
called once at the END of each minute
'''
def handle_data(context, data):
    print context.message
    print context.aapl

    '''
    order_target_percent(sid(24), 0.50)  # long
    order_target_percent(sid(24), -0.50)  # short
    '''


    ### NOTE data API

    # retrieve the most recent value of a given fields for a given asset
    data.current(sid(24), 'price')
    data.current([sid(24), sid(8554)], ['low', 'high'])

    # if a asset can be trade
    data.can_trade(sid(24))

    # return a pandas Series containing the price history

    # Get the 10-day trailing price history of AAPL in the form of a Series.
    hist = data.history(sid(24), 'price', 10, '1d')  # note, 9 days plus current day

    # Mean price over the last 10 days.
    mean_price = hist.mean()

    data.history(sid(8554), 'volume', 11, '1d')[:-1].mean() # last 10 complete days

    # Get the last 5 minutes of volume data for each security in our list.
    hist = data.history([sid(24), sid(8554), sid(5061)], 'volume', 5, '1m')

    # Calculate the mean volume for each security in our DataFrame.
    mean_volumes = hist.mean(axis=0)

    ### NOTE end data API

    if data.can_trade(context.aapl):
        order_target_percent(context.aapl, 0.60)

    if data.can_trade(context.spy):
        order_target_percent(context.spy, -0.40)
