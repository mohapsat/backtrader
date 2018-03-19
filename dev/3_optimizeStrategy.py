# dev/3_optimizeStrategy.py

# Optimization is the process of testing different values for each parameter of strategy to see
# which configuration provides the best returns


# REF:
# https://backtest-rookies.com/2017/06/26/optimize-strategies-backtrader/

# 11_optimize.py

# Instead of calling addstrategy to add a stratey class to Cerebro, the call is made to optstrategy,
# and instead of passing a value a range of values is passed.


import backtrader as bt
from datetime import datetime


class firstStrategy(bt.Strategy):
    params = (
        ('period', 21),
    )

    def __init__(self):
        self.startcash = self.broker.getvalue()
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.period)

    def next(self):
        if not self.position:
            if self.rsi < 30:
                self.buy(size=100)
        else:
            if self.rsi > 70:
                self.sell(size=100)

# Variable for our starting cash
startcash = 10000

# Create an instance of cerebro
cerebro = bt.Cerebro(optreturn=False)

# Add our strategy
cerebro.optstrategy(firstStrategy, period=range(14, 15))


# Get Apple data from Yahoo Finance.
data = bt.feeds.YahooFinanceData(
    dataname='AAPL',
    fromdate=datetime(2016, 1, 1),
    todate=datetime(2017, 1, 1),
    buffered=True
)

# Add the data to Cerebro
cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(startcash)

# Run over everything
opt_runs = cerebro.run()

# Generate results list
final_results_list = []
for run in opt_runs:
    for strategy in run:
        value = round(strategy.broker.get_value(), 2)
        PnL = round(value - startcash, 2)
        period = strategy.params.period
        final_results_list.append([period, PnL])

# Sort Results List
by_period = sorted(final_results_list, key=lambda x: x[0])
by_PnL = sorted(final_results_list, key=lambda x: x[1], reverse=True)

# Print results
print('Results: Ordered by period:')
for result in by_period:
    print('Period: {}, PnL: {}'.format(result[0], result[1]))
print('Results: Ordered by Profit:')
for result in by_PnL:
    print('Period: {}, PnL: {}'.format(result[0], result[1]))