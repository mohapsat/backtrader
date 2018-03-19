# https://www.coinsheet.org/coin/july-29-2017

# When is there a buy recommendation?
    # When you see 9 consecutive closes “lower” than the close 4 bars prior.
    # An ideal buy is when the low of bars 6 and 7 in the count are exceeded by the low of bars 8 or 9.

# When is there a sell recommendation?
    # When you see 9 consecutive closes “higher” than the close 4 candles prior.
    # An ideal sell is when when the the high of bars 6 and 7 in the count are exceeded by the high of bars 8 or 9.See the example below of a buy recommendation for ETHUSD on GDAX.


import backtrader as bt
from datetime import datetime


class numberIndicatorStrategy(bt.Strategy):

    params = (
        ('num_closes', 9),
        ('num_prior_closes', 4),
    )


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))


    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # self.log('Close, %.2f' % self.dataclose[0])

        if not self.position:
            if self.dataclose[0] < self.dataclose[-3]:
                if self.dataclose[-1] < self.dataclose[-4]:
                    if self.dataclose[2] < self.dataclose[-5]:
                        if self.dataclose[3] < self.dataclose[-6]:
                            if self.dataclose[4] < self.dataclose[-7]:
                                if self.dataclose[5] < self.dataclose[-8]:
                                    if self.dataclose[6] < self.dataclose[-9]:
                                        if self.dataclose[7] < self.dataclose[-10]:
                                            if self.dataclose[8] < self.dataclose[-11]:
                                                self.buy()
                                                self.log('BUY CREATE, %.2f' % self.dataclose[0])
        else:
            if self.dataclose[0] > self.dataclose[-3]:
                if self.dataclose[-1] > self.dataclose[-4]:
                    if self.dataclose[2] > self.dataclose[-5]:
                        if self.dataclose[3] > self.dataclose[-6]:
                            if self.dataclose[4] > self.dataclose[-7]:
                                if self.dataclose[5] > self.dataclose[-8]:
                                    if self.dataclose[6] > self.dataclose[-9]:
                                        if self.dataclose[7] > self.dataclose[-10]:
                                            if self.dataclose[8] > self.dataclose[-11]:
                                                self.sell()
                                                self.log('SELL CREATE, %.2f' % self.dataclose[0])

#starting cash
startCash = 10000

# create a new instance of cerebro
cerebro = bt.Cerebro()

# Add our strategy to cerebro
cerebro.addstrategy(numberIndicatorStrategy)

data = bt.feeds.YahooFinanceData(
    dataname='SFLY',
    fromdate=datetime(2016, 1, 1),
    todate=datetime(2018, 1, 1),
    # buffered=True
)

# add data to cerebro
cerebro.adddata(data)

# run cerebro
cerebro.run()

# get final portfolio value
finalPortVal = cerebro.broker.getvalue()
pnl = finalPortVal - startCash

# Print final portfolio value
print('final portfolio value = %2d' % finalPortVal)
print('PnL = %2d' % pnl)

# plot
cerebro.plot()
