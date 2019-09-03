from quantopian.pipeline.data import morningstar
from quantopian.pipeline.filters.morningstar import IsPrimaryShare
from quantopian.pipeline.filters.morningstar import Q1500US

# Filter for primary share equities. IsPrimarySHare is a built-in filter
primary_share = IsPrimaryShare()

# Equities listed as common stock (as opposed to, say, preferred stock).
# 'ST00000001' indicates common stock
common_stock = morningstar.share_class_reference.security_type.latest.eq('ST00000001')

# Non-depositary receipts. Recall that the ~ operator inverts filters,
# turning Trues into Falses and vice versa
not_depositary = ~morningstar.share_class_reference.is_depositary_receipt.latest

# Equities not trading over-the-counter.
not_otc = ~morningstar.share_class_reference.exchange_id.latest.startswith('OTC')

# Not when-issued equites.
not_wi = ~morningstar.share_class-reference.symbol.latest.endswith('.WI')

# Equities without LP in their name, .matches does a match using a regular expression
not_lp_name = ~morningstar.company_reference.standard_name.latest.matches('.* L[. ]?P.?$')

# Equities with a null value in the limited_partnership Morningstar fundamental field.
not_lp_balance_sheet = morningstar.balance_sheet.limited_partnership.latest.isnull()

# Equities whose most recent Morningstar market cap is not null have fundamental data
# and therefore are not ETFs
have_market_cap = morningstar.valuation.market_cap.latest.notnull()

# combining filters for stocks that pass all of our previous filters.
tradeable_stocks = (
    primary_share
    & common_stock
    & not_depositary
    & not_otc
    & not_wi
    & not_lp_name
    & not_lp_balance_sheet
    & have_market_cap
)


def make_pipeline():
    # base_universe = AverageDollarVolume(window_length=20, mask=tradeable_stocks).percentile_between(70,100)
    base_universe = Q1500US()

    # 10-day close price average.
    mean_10 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=10, mask=base_universe)

    # 30-day close price average.
    mean_30 = SimpleMovingAverage(inputs=[USEquityPricing.close], window_length=30, mask=base_universe)

    # Normalize price difference, and top positive is likely to short and bottom negative is likely to long
    percent_difference = (mean_10 - mean_30) / mean_30

    # Create a filter to select securities to short
    shorts = percent_difference.top(25)

    # Create a filter to select securities to long
    longs = percent_difference.bottom(25)

    # Filter for the securities that we want to trade
    securities_to_trade = (shorts | longs)

    return Pipeline(
        columns={
            'long': longs,
            'shorts': shorts
        },
        screen=securities_to_trade
    )

# Then just running this pipeline
result = run_pipeline(make_pipeline(), '2015-05-05', '2015-05-05')
result.head()
