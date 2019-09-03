from quantopian.pipeline.data.builtin import USEquityPricing
from quantopian.pipeline.factors import AverageDollarVolume, SimpleMovingAverage
from quantopian.pipeline import CustomFactor, Pipeline
import numpy

def make_pipeline():
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30)

    percent_difference = (mean_close_10 - mean_close_30 / mean_close_30)

    dollar_volume = AverageDollarVolume(window_length=30)

    high_dollar_volume = (dollar_volume > 10000000)

    low_dollar_volume = ~high_dollar_volume

    latest_close = USEquityPricing.close.latest


    # Lesson 6
    top_high_dollar_volume = dollar_volume.percentile_between(90,100)
    latest_close = USEquityPricing.close.latest
    above_20 = latest_close > 20

    is_tradeable = top_high_dollar_volume & above_20

    # Lesson 7 Masking: Add filter in factors

    # Passing the high_dollar_volume filter, reduce only partial of the stocks
    mean_close_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10, mask=high_dollar_volume)
    mean_close_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=high_dollar_volume)

    # Lesson 9 Datasets, BoundColumns
    # NOTE: Datasets and BoundColumns do not hold actual data. They don't perform the
    # computation until the pipeline is run.

    # dtype of a BoundColumn determines whether the computation is a factor(float), a filter(bool), or a classifier(string, int).



    return Pipeline(
        # Here we combining factors
        columns={
            '10_day_mean_close': mean_close_10,
            'latest_close_price': latest_close,
            'high_dollar_volume': high_dollar_volume
        },

        # This select only high_dollar_volume is 'true'
        # screen=high_dollar_volume
        screen=is_tradeable
    )


# Lesson 10
class StdDev(CustomFactor):
    def compute(self, today, asset_ids, out, values):
        # Calculates the column-wise standard deviation, ignoring NaNs
        out[:] = numpy.nanstd(values, axis=0)


def make_pipeline():
    std_dev = StdDev(inputs=[USEquityPricing.close], window_length=5)

    return Pipeline(
        columns={
            'std_dev': std_dev
        }
    )

def make_pipeline():
    ten_day_momentum = Momentum(window_length=10)
    twenty_day_momentum = Momentum(window_length=20)

    positive_momentum = ((ten_day_momentum > 1) & (twenty_day_momentum > 1))

    std_dev = StdDev(inputs=[USEquityPricing.close], window_length=5)

    return Pipeline(
        columns={
            'std_dev': std_dev,
            'ten_day_momentum': ten_day_momentum,
            'twenty_day_momentum': twenty_day_momentum
        },
        screen=positive_momentum
    )
